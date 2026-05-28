from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    def clean_vin(self):
        vin = self.cleaned_data.get('vin')
        qs = Vehicle.objects.filter(vin=vin)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('Автомобиль с таким VIN же существует')

        return vin

    def clean_license_plate(self):
        license_plate = self.cleaned_data.get('license_plate')
        qs = Vehicle.objects.filter(license_plate=license_plate)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('Автомобиль с таким госномером уже существует')
        return license_plate

    class Meta:
        model = Vehicle
        exclude = ["owner"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
