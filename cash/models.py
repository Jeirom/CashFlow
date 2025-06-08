from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from users.models import User


class Status(models.Model):
    """
    🚦 Status
    ----------------------------------------------------------------------
    Хранит бизнес-контекст записи ДДС (Cash-Flow).

    Примеры:
        • «Бизнес»   – корпоративные операции
        • «Личное»   – личные траты / пополнения
        • «Налоги»   – расчёты с казной

    Особенности:
        • `name` уникален на уровне БД.
        • Используется как FK в модели CashFlow для аналитики.
    """

    name = models.CharField("Название статуса", max_length=100, unique=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]

    def __str__(self) -> str:
        """Отображает статус красивой строкой в админке / shell."""
        return self.name


class Type(models.Model):
    """
    💳 Type
    ----------------------------------------------------------------------
    Отражает направление движения денег.

    Стандартный набор:
        • «Пополнение» – inflow
        • «Списание»   – outflow
        • «Перемещение» – внутри счёта

    Особенности:
        • `name` уникален.
        • Родитель для Category (One-To-Many).
    """

    name = models.CharField("Название типа", max_length=100, unique=True)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """
    🗂 Category
    ----------------------------------------------------------------------
    Логическое разбиение операций по направлениям затрат/доходов.

    Пример иерархии:
        Type = «Списание»
            └── Category = «Маркетинг»
                ├── Subcategory = «SEO»
                └── Subcategory = «SMM»

    Поля:
        • `name`      – человекочитаемое имя категории
        • `type` (FK) – гарантирует, что категория «привязана» к конкретному
                        направлению движения (Pop/Spend и т.д.).
    """

    name = models.CharField("Название категории", max_length=100)
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Тип",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["type__name", "name"]
        unique_together = ("name", "type")

    def __str__(self) -> str:
        return f"{self.name} ({self.type.name})"


class Subcategory(models.Model):
    """
    🏷 Subcategory
    ----------------------------------------------------------------------
    Самый «тонкий» уровень классификации.

    • Наследует бизнес-контекст через FK на Category → Type.
    • Используется для более детального бюджета, аналитики и отчётов.
    """

    STATUS: list[tuple[str, str]] = [
        ("Пополнение", "Popolneniye"),
        ("Списание", "Spisaniye"),
    ]
    name = models.CharField("Название подкатегории", max_length=100)
    type = models.CharField(verbose_name="Тип", choices=STATUS)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["category__name", "name"]
        unique_together = ("name", "category")

    def __str__(self) -> str:
        return f"{self.name} ({self.category.name})"


class CashFlow(models.Model):
    """
    💰 CashFlow
    ----------------------------------------------------------------------
    Главная звезда шоу – фактическая финансовая операция.

    Бизнес-правила:
        1. Category → Type: категория обязана принадлежать выбранному типу.
        2. Subcategory → Category: подкатегория обязана принадлежать категории.
        3. `date_created` не может быть в будущем (ну камон).

    Жизненный цикл:
        • При вызове `save()` выполняется `full_clean()` — 🚫 грязных данных
          в базе быть не должно.
        • Автоматические метки `created_at` / `updated_at` помогают следить
          за изменениями.

    Форма отображения:
        >>> print(cashflow)
        2025-05-14 | Пополнение | Зарплата | Аванс | 120 000.00 ₽
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(verbose_name="Дата операции")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        "Сумма (₽)",
        max_digits=1000,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    comment = models.TextField("Комментарий", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания записи", auto_now_add=True)
    updated_at = models.DateTimeField("Дата последнего изменения", auto_now=True)

    class Meta:
        verbose_name = "Движение денежных средств"
        verbose_name_plural = "Движения денежных средств"
        ordering = ["-date_created"]

    def __str__(self) -> str:
        """Читабельное представление для админки и shell."""
        return (
            f"{self.date_created.isoformat()} | "
            f"{self.type.name} | {self.category.name} | "
            f"{self.subcategory.name} | {self.amount} ₽"
        )

    # ------------------------------------------------------------------ #
    #                           В А Л И Д А Ц И Я                        #
    # ------------------------------------------------------------------ #
    def clean(self) -> None:
        """
        Проверяет бизнес-инварианты экземпляра перед сохранением.

        Raises
        ------
        ValidationError
            Если нарушено одно из правил:
            • Категория ↔ Тип
            • Подкатегория ↔ Категория
            • Дата операции в будущем
        """
        super().clean()

        # 1. Категория должна соответствовать типу
        if self.category and self.type and self.category.type_id != self.type_id:
            raise ValidationError(
                {
                    "category": (
                        f"Категория «{self.category.name}» не соответствует типу "
                        f"«{self.type.name}»."
                    )
                }
            )

        # 2. Подкатегория должна соответствовать категории
        if (
            self.subcategory
            and self.category
            and self.subcategory.category_id != self.category_id
        ):
            raise ValidationError(
                {
                    "subcategory": (
                        f"Подкатегория «{self.subcategory.name}» не относится "
                        f"к категории «{self.category.name}»."
                    )
                }
            )

        # 3. Дата операции не может быть в будущем
        today = timezone.localdate()
        if self.date_created and self.date_created > today:
            raise ValidationError(
                {"date_created": "Дата операции не должна превышать текущую дату."}
            )

    def save(self, *args, **kwargs) -> None:
        """
        Переопределяем `save`, чтобы **никогда** не сохранять модель,
        минуя валидацию (`full_clean`).

        Примечание:
            Если нужно массово грузить данные без проверок (например, миграция
            из 1С), используйте `CashFlow.objects.bulk_create(..., validate=False)`
            либо отключайте проверки явно (не рекомендуется).
        """
        self.full_clean()
        super().save(*args, **kwargs)
