from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CLIENT = "client"
    ROLE_MASTER = "master"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = [
        (ROLE_CLIENT, "Клиент"),
        (ROLE_MASTER, "Мастер"),
        (ROLE_ADMIN, "Администратор"),
    ]

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_CLIENT,
        verbose_name="Роль",
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    @property
    def is_client(self):
        return self.role == self.ROLE_CLIENT

    @property
    def is_master(self):
        return self.role == self.ROLE_MASTER

    @property
    def is_service_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    @property
    def can_manage_orders(self):
        return self.is_staff or self.is_master or self.is_service_admin

    def __str__(self):
        return self.full_name or self.username
