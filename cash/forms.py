from django import forms
from .models import CashFlow, Subcategory, Category


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ['date_created', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date'}),
        }

