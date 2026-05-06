from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("customer_id", "last_name", "first_name", "phone", "email", "address")
    search_fields = ("last_name", "first_name", "phone", "email", "address")
    ordering = ("last_name", "first_name")