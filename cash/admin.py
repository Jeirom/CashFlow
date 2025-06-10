from django.contrib import admin
from cash.models import Status, Type, Category, Subcategory, CashFlow


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type",)
    search_fields = ("name",)
    ordering = ("type__name", "name")
    raw_id_fields = ("type",)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "type")
    list_filter = ("category__type",)
    search_fields = ("name",)
    ordering = ("category__name", "name")
    raw_id_fields = ("category",)


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = (
        "date_created",
        "user",
        "amount",
        "type",
        "category",
        "subcategory",
        "status",
    )
    list_filter = ("type", "category", "subcategory", "status", "date_created")
    search_fields = ("comment", "user__email")
    raw_id_fields = ("user", "type", "category", "subcategory", "status")
    date_hierarchy = "date_created"
    ordering = ("-date_created",)
