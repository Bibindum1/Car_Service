from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("id", "username", "full_name", "email", "phone", "role", "is_staff", "is_active")
    list_display_links = ("id", "username")
    search_fields = ("username", "full_name", "email", "phone")
    list_filter = ("role", "is_staff", "is_active", "is_superuser")
    ordering = ("id",)
    readonly_fields = ("last_login", "date_joined")
    list_per_page = 20
    save_on_top = True

    fieldsets = (
        ("Авторизация", {"fields": ("username", "password")}),
        ("Личная информация", {"fields": ("full_name", "email", "phone", "avatar")}),
        ("Роль в автосервисе", {"fields": ("role",)}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = ((None, {"classes": ("wide",),
                             "fields": ("username", "full_name", "email", "phone", "role", "password1", "password2",
                                        "is_staff", "is_active")}),)
