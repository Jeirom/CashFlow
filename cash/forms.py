from django import forms
from .models import CashFlow, Subcategory, Category, Status, Type


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = [
            "date_created",
            "status",
            "type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]
        widgets = {
            "date_created": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "date_created": "Дата создания",
            "status": "Статус операции",
            "type": "Тип движения",
            "category": "Категория",
            "subcategory": "Подкатегория",
            "amount": "Сумма",
            "comment": "Комментарий",
        }


class CashFlowUpdateForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ['date_created', 'comment']  # Только эти два поля будут в форме

        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'date_created': 'Дата операции',
            'comment': 'Комментарий',
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        labels = {
            "name": "Название статуса",
        }

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ["name"]
        labels = {
            "name": "Название типа",
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "type"]
        labels = {
            "name": "Название категории",
            "type": "Тип",
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].required = True

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ["name", "type", "category"]
        labels = {
            "name": "Название подкатегории",
            "type": "Тип",
            "category": "Категория",
        }
