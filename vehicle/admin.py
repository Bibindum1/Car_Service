from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle_id",
        "brand",
        "model"
    )
    list_display_links = (
        "vehicle_id",
        "brand",
    )

    search_fields = (
        "vin",
        "plate_number",
        "brand",
        "model",
        "owner__username",
        "owner__full_name",
        "owner__phone",
    )

    list_filter = (
        "brand",
        "model",
        "year",
    )

    readonly_fields = (
        "vehicle_id",
    )

    ordering = (
        "brand",
        "model",
    )

    list_per_page = 20

    save_on_top = True

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "owner",
                "brand",
                "model",
                "year",
                "color",
            )
        }),

        ("Регистрационные данные", {
            "fields": (
                "plate_number",
                "vin",
            )
        }),


        ("Служебная информация", {
            "fields": (
                "vehicle_id",
            ),
            "classes": ("collapse",),
        }),
    )
