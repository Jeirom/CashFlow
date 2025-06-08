from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class CashFlowRecord(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def clean(self):
        # Валидация связей: подкатегория должна соответствовать категории
        if self.subcategory and self.subcategory.category != self.category:
            raise ValidationError(_('Подкатегория не связана с выбранной категорией.'))

        # Валидация: категория должна соответствовать типу
        if self.category and self.category.type != self.type:
            raise ValidationError(_('Категория не соответствует выбранному типу.'))

    def save(self, *args, **kwargs):
        self.full_clean()  # вызываем clean для проверки перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date_created.date()} - {self.amount} руб."
