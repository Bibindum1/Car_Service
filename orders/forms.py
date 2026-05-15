from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget

from .models import Service, Order


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "name",
            "phone",
            "email",
            "car_model",
            "description",
            "service"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.fields.values():
            f.widget.attrs.update({'class': 'form-control'})

class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "image": ImageUploaderWidget(),
        }