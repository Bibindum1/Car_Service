from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from vehicle.models import Vehicle


class Service(models.Model):
    title = models.CharField(max_length=50)
    service_id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=100)
    initial_price = models.DecimalField(
        max_digits=10,
        validators=[MinValueValidator(Decimal('500.00'))],
        help_text="Минимальная цена - 500 ₽",
        decimal_places=2,
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Услуги"
        verbose_name = "Услуга"

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('accepted', 'Принята'),
        ('in_progress', 'В работе'),
        ('waiting_parts', 'Ожидание деталей'),
        ('done', 'Готово'),
        ('cancelled', 'Отменено'),
    ]

    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Клиент",
    )
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус",
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="Автомобиль")
    description = models.TextField(verbose_name="Описание проблемы")
    service = models.ForeignKey(
        "Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Услуга",
    )
    appointment_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата и время записи",
        help_text="Время, на которое клиент записан в сервис.",
    )
    master = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_orders",
        verbose_name="Мастер",
        limit_choices_to={"role__in": ["master", "admin"]},
    )
    master_comment = models.TextField(
        blank=True,
        verbose_name="Комментарий мастера",
        help_text="Диагностика, выполненные работы и рекомендации.",
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Заказы"
        verbose_name = "Заказ"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.vehicle}"
