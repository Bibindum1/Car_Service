from django.contrib import admin
from django.db import models
from image_uploader_widget.widgets import ImageUploaderWidget

from .forms import ServiceAdminForm
from .models import Service, Order


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm

    formfield_overrides = {
        models.ImageField: {"widget": ImageUploaderWidget()},
    }

    list_display = (
        "service_id",
        "vehicle",
        "user",
        "date",
        "initial_price",
    )

    list_display_links = (
        "service_id",
        "vehicle",
    )

    search_fields = (
        "vehicle__vin",
        "vehicle__plate_number",
        "vehicle__brand",
        "vehicle__model",
        "user__username",
        "user__full_name",
        "description",
    )

    list_filter = (
        "date",
        "vehicle__brand",
        "vehicle__model",
    )

    readonly_fields = (
        "service_id",
    )

    ordering = ("-date",)

    list_per_page = 15

    save_on_top = True

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "user",
                "vehicle",
                "date",
            )
        }),
        ("Изображение", {
            "fields": (
                "image",
            )
        }),
    )
