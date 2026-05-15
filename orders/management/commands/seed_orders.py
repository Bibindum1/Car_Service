from random import randint, choice
from decimal import Decimal

from faker import Faker

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from vehicle.models import Vehicle
from orders.models import Order, Service

fake = Faker("ru_RU")

BRANDS_AND_MODELS = {
    "Toyota": ["Camry", "Corolla", "RAV4"],
    "BMW": ["X5", "M3", "320i"],
    "Audi": ["A4", "A6", "Q7"],
    "Mercedes": ["C200", "E220", "GLE"],
    "Honda": ["Civic", "Accord", "CR-V"],
    "Ford": ["Focus", "Mustang", "Explorer"],
}

COLORS = ["Черный", "Белый", "Серый", "Синий", "Красный", "Зеленый"]

SERVICES = [
    "Замена масла",
    "Диагностика двигателя",
    "Ремонт подвески",
    "Шиномонтаж",
    "Замена тормозных колодок",
    "Покраска кузова",
    "Компьютерная диагностика",
    "Замена аккумулятора",
]


class Command(BaseCommand):
    help = "Заполнение базы тестовыми данными"

    def add_arguments(self, parser):
        parser.add_argument("--orders", type=int, default=20)
        parser.add_argument("--vehicles", type=int, default=20)
        parser.add_argument("--services", type=int, default=20)

    def handle(self, *args, **kwargs):

        User = get_user_model()
        user = User.objects.first()

        if not user:
            user = User.objects.create_user(
                username="seed_user",
                password="123456"
            )

        orders_count = kwargs["orders"]
        vehicles_count = kwargs["vehicles"]
        services_count = kwargs["services"]

        # ----------------------------
        # VEHICLES
        # ----------------------------
        self.stdout.write("Создание автомобилей...")

        vehicles = []

        for _ in range(vehicles_count):
            brand = choice(list(BRANDS_AND_MODELS.keys()))
            model = choice(BRANDS_AND_MODELS[brand])

            vehicle = Vehicle.objects.create(
                vin=fake.unique.bothify("???########????").upper(),
                plate_number=fake.unique.bothify("?###??##").upper(),
                brand=brand,
                model=model,
                year=randint(2000, 2025),
                mileage=randint(0, 300000),
                color=choice(COLORS),
            )

            vehicles.append(vehicle)

        self.stdout.write(
            self.style.SUCCESS(f"Создано автомобилей: {len(vehicles)}")
        )

        # ----------------------------
        # ORDERS
        # ----------------------------
        self.stdout.write("Создание заказов...")

        created_orders = 0

        for _ in range(orders_count):

            car = choice(vehicles)

            Order.objects.create(
                name=fake.name(),
                phone=fake.phone_number(),
                email=fake.email(),
                car_model=car.brand + " " + car.model,
                description=fake.text(),
                service=None,
                status=False,
                user=user,
            )

            created_orders += 1

        self.stdout.write(
            self.style.SUCCESS(f"Создано заказов: {created_orders}")
        )

        # ----------------------------
        # SERVICES
        # ----------------------------
        self.stdout.write("Создание услуг...")

        created_services = 0

        for _ in range(services_count):

            vehicle = choice(vehicles)

            service_date = fake.date_between(
                start_date="-1y",
                end_date="today"
            )

            if Service.objects.filter(
                vehicle=vehicle,
                date=service_date
            ).exists():
                continue

            Service.objects.create(
                vehicle=vehicle,
                date=service_date,
                description=choice(SERVICES),
                initial_price=Decimal(randint(500, 50000)),
            )

            created_services += 1

        self.stdout.write(
            self.style.SUCCESS(f"Создано услуг: {created_services}")
        )

        self.stdout.write(
            self.style.SUCCESS("Заполнение завершено")
        )