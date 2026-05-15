from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle_id",
        "brand",
        "model",
        "plate_number",
        "vin",
        "year",
        "mileage",
        #"CustomUser",
    )

    search_fields = (
        "vin",
        "plate_number",
        "brand",
        "model",
        "services__user__full_name"
    )

    list_filter = (
        "brand",
        "model",
        "year",
        #"user",
    )

    ordering = ("brand", "model")

    readonly_fields = ("vehicle_id",)

    fieldsets = (
        ("Основная информация", {
            "fields": ("brand", "model", "year")
        }),
        ("Идентификаторы", {
            "fields": ("plate_number", "vin")
        }),
        ("Эксплуатация", {
            "fields": ("mileage",)
        }),
        ("Служебные поля", {
            "fields": ("vehicle_id",),
            "classes": ("collapse",),
        }),
    )