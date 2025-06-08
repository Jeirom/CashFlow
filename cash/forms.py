from django import forms
from .models import CashFlowRecord

class CashFlowRecordForm(forms.ModelForm):
    class Meta:
        model = CashFlowRecord
        fields = ['date_created', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date_created': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        type_ = cleaned_data.get('type')

        # Проверка: подкатегория должна соответствовать категории
        if subcategory and category and subcategory.category != category:
            self.add_error('subcategory', 'Подкатегория не связана с выбранной категорией.')

        # Проверка: категория должна соответствовать типу
        if category and type_ and category.type != type_:
            self.add_error('category', 'Категория не соответствует выбранному типу.')