import os
import random
from decimal import Decimal
from random import choice, randint

from faker import Faker

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand

from orders.models import Order, Service
from vehicle.models import Vehicle

fake = Faker("ru_RU")

User = get_user_model()

# ---------------------------------------------------
# НАСТРОЙКИ
# ---------------------------------------------------

CAR_BRANDS = {
    "BMW": ["M5", "X5", "320i", "M3"],
    "Mercedes": ["E63", "C200", "GLE", "CLS"],
    "Audi": ["A6", "RS7", "Q8", "A4"],
    "Toyota": ["Camry", "Corolla", "Land Cruiser"],
    "Honda": ["Accord", "Civic", "CR-V"],
    "Volkswagen": ["Golf", "Passat", "Touareg"],
    "Ford": ["Mustang", "Focus", "Explorer"],
    "Porsche": ["911", "Panamera", "Cayenne"],
}

COLORS = [
    "Черный",
    "Белый",
    "Серый",
    "Красный",
    "Синий",
    "Зеленый",
    "Оранжевый",
]

SERVICES = [
    "Замена масла",
    "Компьютерная диагностика",
    "Ремонт двигателя",
    "Замена тормозных колодок",
    "Шиномонтаж",
    "Полировка кузова",
    "Покраска кузова",
    "Замена аккумулятора",
    "Ремонт подвески",
    "Ремонт коробки передач",
]

ORDER_STATUSES = [
    "new",
    "accepted",
    "in_progress",
    "waiting_parts",
    "done",
    "cancelled",
]

PAYMENT_METHODS = [
    "cash",
    "card",
]


class Command(BaseCommand):

    help = "Полное заполнение базы автосервиса"

    def add_arguments(self, parser):

        parser.add_argument(
            "--users",
            type=int,
            default=15
        )

        parser.add_argument(
            "--vehicles",
            type=int,
            default=30
        )

        parser.add_argument(
            "--services",
            type=int,
            default=50
        )

        parser.add_argument(
            "--orders",
            type=int,
            default=60
        )

        parser.add_argument(
            "--applications",
            type=int,
            default=40
        )

    def handle(self, *args, **kwargs):

        users_count = kwargs["users"]
        vehicles_count = kwargs["vehicles"]
        services_count = kwargs["services"]
        orders_count = kwargs["orders"]
        applications_count = kwargs["applications"]

        self.stdout.write(
            self.style.WARNING("Удаление старых данных...")
        )

        Order.objects.all().delete()
        Service.objects.all().delete()
        Vehicle.objects.all().delete()

        # ---------------------------------------------------
        # USERS
        # ---------------------------------------------------

        self.stdout.write(
            self.style.WARNING("Создание пользователей...")
        )

        users = []

        for _ in range(users_count):

            username = fake.unique.user_name()

            user = User.objects.create_user(
                username=username,

                email=fake.unique.email(),

                password="123456",

                full_name=fake.name(),

                phone=fake.phone_number()[:16]
            )

            users.append(user)

        self.stdout.write(
            self.style.SUCCESS(
                f"Пользователей создано: {len(users)}"
            )
        )

        # ---------------------------------------------------
        # VEHICLES
        # ---------------------------------------------------

        self.stdout.write(
            self.style.WARNING("Создание автомобилей...")
        )

        vehicles = []

        for _ in range(vehicles_count):

            brand = choice(list(CAR_BRANDS.keys()))

            model = choice(CAR_BRANDS[brand])

            owner = choice(users)

            vehicle = Vehicle.objects.create(

                vin=fake.unique.bothify(
                    text="????????#########"
                ).upper()[:17],

                plate_number=fake.unique.bothify(
                    text="?###??##"
                ).upper(),

                brand=brand,

                model=model,

                year=randint(2000, 2025),

                mileage=randint(1000, 350000),

                color=choice(COLORS),

                owner=owner
            )

            vehicles.append(vehicle)

        self.stdout.write(
            self.style.SUCCESS(
                f"Автомобилей создано: {len(vehicles)}"
            )
        )

        # ---------------------------------------------------
        # MEDIA
        # ---------------------------------------------------

        media_seed_path = os.path.join(
            settings.BASE_DIR,
            "media_seed"
        )

        images = []

        if os.path.exists(media_seed_path):

            for file in os.listdir(media_seed_path):

                if file.lower().endswith((
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".webp"
                )):
                    images.append(
                        os.path.join(
                            media_seed_path,
                            file
                        )
                    )

        # ---------------------------------------------------
        # SERVICES
        # ---------------------------------------------------

        self.stdout.write(
            self.style.WARNING("Создание услуг...")
        )

        services = []

        for _ in range(services_count):

            vehicle = choice(vehicles)

            service = Service.objects.create(

                user=vehicle.owner,

                vehicle=vehicle,

                description=fake.text(
                    max_nb_chars=400
                ),

                initial_price=Decimal(
                    randint(50, 3000)
                ),

                date=fake.date_between(
                    start_date="-1y",
                    end_date="today"
                )
            )

            # image

            if images:

                random_image = random.choice(images)

                with open(random_image, "rb") as image_file:

                    service.image.save(
                        os.path.basename(random_image),

                        File(image_file),

                        save=True
                    )

            services.append(service)

        self.stdout.write(
            self.style.SUCCESS(
                f"Услуг создано: {len(services)}"
            )
        )

        # ---------------------------------------------------
        # ORDERS
        # ---------------------------------------------------

        self.stdout.write(
            self.style.WARNING("Создание заказов...")
        )

        orders = []

        for _ in range(orders_count):

            vehicle = choice(vehicles)

            service = choice(services)

            order = Order.objects.create(

                user=vehicle.owner,

                vehicle=vehicle,

                service=service,

                name=vehicle.owner.full_name,

                phone=vehicle.owner.phone,

                email=vehicle.owner.email,

                description=fake.text(
                    max_nb_chars=250
                ),

                status=choice(
                    ORDER_STATUSES
                )
            )

            orders.append(order)

        self.stdout.write(
            self.style.SUCCESS(
                f"Заказов создано: {len(orders)}"
            )
        )


        self.stdout.write(
            self.style.SUCCESS(
                "База успешно заполнена"
            )
        )