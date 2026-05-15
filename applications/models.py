from django.db import models
from django.conf import settings


PAYMENT_CHOICES = [
    ('cash', 'Наличные'),
    ('card', 'Карта'),
]

STATUS_CHOICES = [
    ('new', 'Новая'),
    ('done', 'Завершена'),
]


class Application(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )

    course_name = models.CharField(
        max_length=200,
        verbose_name="Название услуги"
    )

    start_date = models.DateField(
        verbose_name="Дата записи"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name="Способ оплаты"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон"
    )

    email = models.EmailField(
        verbose_name="Электронная почта"
    )

    car_model = models.CharField(
        max_length=100,
        verbose_name="Модель автомобиля"
    )

    description_problem = models.TextField(
        verbose_name="Описание проблемы"
    )

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"