from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from vehicle.models import Vehicle


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="services")
    vehicle = models.ForeignKey("vehicle.Vehicle", on_delete=models.CASCADE, related_name="services", blank=True)
    date = models.DateField()
    description = models.TextField()
    initial_price = models.DecimalField(
        max_digits=10,
        validators=[MinValueValidator(500.00)],
        help_text="Минимальная цена - 500 ₽",
        decimal_places=2,
    )
    image = models.ImageField(upload_to='products/', null=True)

    class Meta:
        verbose_name_plural = "Услуги"
        verbose_name = "Услуга"
        constraints = [
            models.UniqueConstraint(
                fields=["vehicle", "date", "description"],
                name="unique_service_vehicle_date_desc"
            )
        ]

    def __str__(self):
        return f"{self.vehicle} {self.date}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('accepted', 'Принята'),
        ('in_progress', 'В работе'),
        ('waiting_parts', 'Ожидание деталей'),
        ('done', 'Готово'),
        ('cancelled', 'Отменено'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )


    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    description = models.TextField()

    service = models.ForeignKey(
        "Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )



    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Заказы"
        verbose_name = "Заказ"

    def __str__(self):
        return f"{self.name} - {self.vehicle}"
