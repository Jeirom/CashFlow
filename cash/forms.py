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


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ["name"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "type"]


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ["name", "type", "category"]
