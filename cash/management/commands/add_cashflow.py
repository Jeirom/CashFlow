from django.core.management.base import BaseCommand, CommandError
from cash.models import Status, Type, Category, Subcategory
from django.db import transaction

class Command(BaseCommand):
    help = (
        "Инициализирует справочники ДДС: статусы, типы, категории и подкатегории.\n"
        "Использование: python manage.py init_cashflow_data"
    )

    DEFAULT_STATUSES = [
        "Бизнес",
        "Личное",
        "Налог",
    ]

    DEFAULT_TYPES = [
        "Пополнение",
        "Списание",
    ]

    # структура: {тип: {категория: [подкатегории...]}}
    DEFAULT_CATEGORIES = {
        "Пополнение": {
            "Инвестиции": ["Вложения", "Дивиденды"],
            "Возврат": ["Клиенты", "Поставщики"],
        },
        "Списание": {
            "Инфраструктура": ["VPS", "Proxy"],
            "Маркетинг": ["Farpost", "Avito"],
        },
    }

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.MIGRATE_HEADING("Запуск инициализации справочников ДДС")
        )
        try:
            # 1) Статусы
            for name in self.DEFAULT_STATUSES:
                obj, created = Status.objects.get_or_create(name=name)
                verb = "Создан" if created else "Найден"
                self.stdout.write(f"{verb} статус: {name}")

            # 2) Типы
            for name in self.DEFAULT_TYPES:
                obj, created = Type.objects.get_or_create(name=name)
                verb = "Создан" if created else "Найден"
                self.stdout.write(f"{verb} тип: {name}")

            # 3) Категории и подкатегории
            for type_name, cats in self.DEFAULT_CATEGORIES.items():
                # Получаем или создаем тип
                typ, _ = Type.objects.get_or_create(name=type_name)
                for cat_name, subcats in cats.items():
                    # Создаем категорию с FK на тип
                    cat, created_cat = Category.objects.get_or_create(
                        name=cat_name,
                        type=typ
                    )
                    verb_cat = "Создана" if created_cat else "Найдена"
                    self.stdout.write(
                        f"{verb_cat} категория '{cat_name}' для типа '{type_name}'"
                    )

                    # Создаем подкатегории с типом (используем поле type)
                    for sub_name in subcats:
                        sub, created_sub = Subcategory.objects.get_or_create(
                            name=sub_name,
                            category=cat,
                            type=type_name  # Передаем тип как строку
                        )
                        verb_sub = "Создана" if created_sub else "Найдена"
                        self.stdout.write(
                            f"    {verb_sub} подкатегория '{sub_name}' в категории '{cat_name}'"
                        )

        except Exception as e:
            raise CommandError(f"Ошибка инициализации: {e}")

        self.stdout.write(
            self.style.SUCCESS("Справочники ДДС успешно инициализированы"))