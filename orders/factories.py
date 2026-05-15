import factory

from models import Vehicle, Order


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    car_model = factory.Iterator(Vehicle.objects.all())