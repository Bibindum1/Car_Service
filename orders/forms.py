from django import forms
from django.contrib.auth import get_user_model

from image_uploader_widget.widgets import ImageUploaderWidget

from .models import Service, Order

User = get_user_model()


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
            "vehicle",
            "description",
            "service"
        ]

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)
        service = kwargs.pop('service', None)

        super().__init__(*args, **kwargs)

        for f in self.fields.values():
            f.widget.attrs.update({
                'class': 'form-control'
            })

        if user:
            self.fields['vehicle'].queryset = (
                user.vehicles.all()
            )

            self.fields['vehicle'].label_from_instance = (
                lambda obj:
                f'{obj.brand} {obj.model} — {obj.plate_number}'
            )

        if service:
            self.fields['service'].initial = service
            self.fields['service'].widget = forms.HiddenInput()



class OrderManageForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = [
            'status',
            'master',
            'master_comment',
            'appointment_at',
        ]

        widgets = {
            'appointment_at': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),

            'master_comment': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Комментарий мастера'
            }),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        for f in self.fields.values():
            f.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['master'].queryset = (
            User.objects.filter(role='master')
        )

        if (
            user
            and user.role == 'master'
            and not user.is_staff
            and not user.is_superuser
        ):
            self.fields['master'].disabled = True


class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

        widgets = {
            "image": ImageUploaderWidget(),
        }