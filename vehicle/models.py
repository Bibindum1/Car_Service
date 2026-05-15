from django.db import models


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    vin = models.CharField(max_length=17, unique=True)
    plate_number = models.CharField(max_length=20, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(blank=True, null=True)
    mileage = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name_plural = "Автомобили"
        verbose_name = "Автомобиль"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"
