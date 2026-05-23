from django.contrib import admin
from django.utils.html import format_html

from .models import Service, Order


# =========================
# ORDER ADMIN
# =========================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # Колонки в списке
    list_display = (
        "order_id",
        "client_name",
        "vehicle_info",
        "service_info",
        "colored_status",
        "created_at",
    )

    # Кликабельные поля
    list_display_links = (
        "order_id",
        "client_name",
    )

    # Фильтры справа
    list_filter = (
        "status",
        "created_at",
        "vehicle__brand",
    )

    # Поиск
    search_fields = (
        "name",
        "phone",
        "email",
        "description",
        "vehicle__brand",
        "vehicle__model",
        "vehicle__plate_number",
        "user__username",
    )

    # Сортировка
    ordering = (
        "-created_at",
    )

    # Только чтение
    readonly_fields = (
        "created_at",
    )

    # Поля редактирования
    fieldsets = (

        ("Информация о клиенте", {
            "fields": (
                "user",
                "name",
                "phone",
                "email",
            )
        }),

        ("Автомобиль", {
            "fields": (
                "vehicle",
            )
        }),

        ("Заказ", {
            "fields": (
                "service",
                "description",
                "status",
            )
        }),

        ("Дата", {
            "fields": (
                "created_at",
            )
        }),
    )

    # Количество на странице
    list_per_page = 20

    # Оптимизация
    list_select_related = (
        "user",
        "vehicle",
        "service",
    )

    # Actions
    actions = [
        "mark_as_accepted",
        "mark_as_in_progress",
        "mark_as_done",
        "mark_as_cancelled",
    ]

    # =========================
    # КРАСИВЫЕ ПОЛЯ
    # =========================

    @admin.display(description="Клиент")
    def client_name(self, obj):
        return obj.name

    @admin.display(description="Автомобиль")
    def vehicle_info(self, obj):
        return f"{obj.vehicle.brand} {obj.vehicle.model}"

    @admin.display(description="Услуга")
    def service_info(self, obj):

        if obj.service:
            return f"#{obj.service.service_id}"

        return "Без услуги"

    @admin.display(description="Статус")
    def colored_status(self, obj):

        colors = {
            "new": "#3498db",
            "accepted": "#f39c12",
            "in_progress": "#9b59b6",
            "waiting_parts": "#e67e22",
            "done": "#27ae60",
            "cancelled": "#e74c3c",
        }

        names = {
            "new": "Новая",
            "accepted": "Принята",
            "in_progress": "В работе",
            "waiting_parts": "Ожидание деталей",
            "done": "Готово",
            "cancelled": "Отменено",
        }

        color = colors.get(obj.status, "#999")

        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            names.get(obj.status)
        )

    # =========================
    # ACTIONS
    # =========================

    @admin.action(description="Пометить как 'Принята'")
    def mark_as_accepted(self, request, queryset):
        queryset.update(status="accepted")

    @admin.action(description="Пометить как 'В работе'")
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status="in_progress")

    @admin.action(description="Пометить как 'Готово'")
    def mark_as_done(self, request, queryset):
        queryset.update(status="done")

    @admin.action(description="Пометить как 'Отменено'")
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="cancelled")


# =========================
# SERVICE ADMIN
# =========================

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        "service_id",
        "vehicle",
        "user",
        "date",
        "initial_price",
        "orders_count",
    )

    list_display_links = (
        "service_id",
        "vehicle",
    )

    search_fields = (
        "vehicle__brand",
        "vehicle__model",
        "description",
        "user__username",
    )

    list_filter = (
        "date",
        "vehicle__brand",
    )

    ordering = (
        "-service_id",
    )

    list_per_page = 20

    readonly_fields = ()

    fieldsets = (

        ("Основная информация", {
            "fields": (
                "user",
                "vehicle",
                "date",
            )
        }),

        ("Описание", {
            "fields": (
                "description",
            )
        }),

        ("Цена", {
            "fields": (
                "initial_price",
            )
        }),

        ("Изображение", {
            "fields": (
                "image",
            )
        }),
    )

    @admin.display(description="Заказов")
    def orders_count(self, obj):
        return obj.orders.count()