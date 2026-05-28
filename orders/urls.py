from django.urls import path, include
from . import views

app_name = 'orders'

urlpatterns = [
    path("", views.home, name="home"),

    path("services/", views.service_list, name="services_list"),
    path("services/<int:pk>/", views.service_detail, name="service_detail"),
    path("orders/create/", views.order_create, name="order_create"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/calendar/", views.schedule_calendar, name="calendar"),

    path("about/", views.about_list, name="about_list"),
    path("reviews/", views.reviews, name="reviews"),
]
