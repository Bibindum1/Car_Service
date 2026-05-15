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
        # "customer",
        "date",
        "initial_price",
        "description",
    )

    search_fields = (
        "vehicle__vin",
        "vehicle__plate_number",
        "vehicle__brand",
        "vehicle__model",
        # "customer__last_name",
        # "customer__first_name",
        "description",
    )

    list_filter = (
        "date",
        "vehicle__brand",
        "vehicle__model",
        # "customer",
    )

    ordering = ("-date",)

    readonly_fields = ("service_id",)

    fieldsets = (
        ("Основная информация", {
            "fields": ("vehicle", "date", "image")
        }),
        ("Данные услуги", {
            "fields": ("initial_price", "description")
        }),
        ("Служебные поля", {
            "fields": ("service_id",),
            "classes": ("collapse",),
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_id",
        "name",
        "phone",
        "email",
        "car_model",
        "service",
        "status",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "car_model",
    )

    list_filter = (
        "status",
        "service",
    )

    ordering = ("-order_id",)

    readonly_fields = ("order_id",)

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "name",
                "phone",
                "email",
                "car_model",
                "description",
                "service",
                "status",
            )
        }),
        ("Служебные поля", {
            "fields": ("order_id",),
            "classes": ("collapse",),
        }),
    )
