from django.contrib import admin
from .models import Service, Order

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("service_id", "vehicle", "customer", "date", "initial_price", "description")
    search_fields = (
        "vehicle__vin",
        "vehicle__plate_number",
        "vehicle__brand",
        "vehicle__model",
        "customer__last_name",
        "customer__first_name",
        "description",
    )
    ordering = ("-date",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "vehicle", "customer", "date", "status")
    search_fields = (
        "vehicle__vin",
        "vehicle__plate_number",
        "vehicle__brand",
        "vehicle__model",
        "customer__last_name",
        "customer__first_name",
    )
    ordering = ("-date",)