from django.core.validators import MinValueValidator
from django.db import models


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey("user.Customer", on_delete=models.CASCADE, related_name="services")
    vehicle = models.ForeignKey("vehicle.Vehicle", on_delete=models.CASCADE, related_name="services")
    date = models.DateField()
    description = models.TextField()
    initial_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text="Минимальная цена - 500 ₽"
    )

    class Meta:
        verbose_name_plural = "Услуги"
        verbose_name = "Услуга"
        constraints = [
            models.UniqueConstraint(fields=["vehicle", "date"], name="unique_service_vehicle_date")
        ]

    def __str__(self):
        return f"{self.vehicle} {self.date}"

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey("user.Customer", on_delete=models.CASCADE, related_name="orders")
    vehicle = models.ForeignKey("vehicle.Vehicle", on_delete=models.CASCADE, related_name="orders")
    date = models.DateField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Заказы"
        verbose_name = "Заказ"

    def __str__(self):
        return f"{self.vehicle} {self.date}"