from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_active")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active",)
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональные данные", {"fields": ("first_name", "last_name", "phone")}),
        ("Дополнительно", {"fields": ("is_active", "token")}),
    )
    readonly_fields = ("email",)
