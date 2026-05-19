from django.urls import path, include
from . import views

app_name = 'orders'

urlpatterns = [
    path("", views.home, name="home"),

    # Service
    path("services/", views.service_list, name="services_list"),
    path("services/<int:pk>/", views.service_detail, name="service_detail"),

    # Order
    path("orders/", views.order_list, name="order_list"),

    path("about/", views.about_list, name="about_list"),
    path("prices/", views.prices, name="prices"),
    path("reviews/", views.reviews, name="reviews"),
]