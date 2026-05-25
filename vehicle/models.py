from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from users.models import CustomUser


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    vin = models.CharField(
        max_length=17,
        unique=True,
        validators=[MinLengthValidator(17)])
    plate_number = models.CharField(max_length=20, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900)])

    color = models.CharField(max_length=30, blank=True)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Автомобили"
        verbose_name = "Автомобиль"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"
