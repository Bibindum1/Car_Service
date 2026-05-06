from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("Vehicle_id", "brand", "model", "plate_number", "vin", "year", "mileage", "customer")
    search_fields = (
        "vin",
        "plate_number",
        "brand",
        "model",
        "customer__last_name",
        "customer__first_name",
    )
    ordering = ("brand", "model")

