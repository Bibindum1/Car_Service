from django import forms
from .models import Service, Order


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"