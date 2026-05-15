from django import forms
from .models import Application

#test

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = (
            'course_name',
            'phone',
            'email',
            'car_model',
            'description_problem',
            'start_date',
            'payment_method'
        )

        labels = {
            'course_name': 'Название услуги',
            'phone': 'Телефон',
            'email': 'Электронная почта',
            'car_model': 'Модель автомобиля',
            'description_problem': 'Описание проблемы',
            'start_date': 'Дата записи',
            'payment_method': 'Способ оплаты',
        }