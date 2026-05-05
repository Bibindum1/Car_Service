from django.core.validators import MinValueValidator
from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="vehicles")
    vin = models.CharField(max_length=17, unique=True)
    plate_number = models.CharField(max_length=20, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(blank=True, null=True)
    mileage = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"


class Service(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="services")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="services")
    date = models.DateField()
    description = models.TextField()
    initial_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text="Минимальная цена - 500 ₽"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["vehicle", "date"], name="unique_service_vehicle_date")
        ]

    def __str__(self):
        return f"{self.vehicle} {self.date}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="orders")
    date = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vehicle} {self.date}"