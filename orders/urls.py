# orders/urls.py
from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),

    # Service
    path("services/", views.service_list, name="service_list"),
    path("services/<int:pk>/", views.service_detail, name="service_detail"),
    path("services/create/", views.service_create, name="service_create"),
    path("services/<int:pk>/update/", views.service_update, name="service_update"),
    path("services/<int:pk>/delete/", views.service_delete, name="service_delete"),

    # Order
    path("orders/", views.order_list, name="order_list"),
    path("orders/create/", views.order_create, name="order_create"),
    path("orders/<int:pk>/update/", views.order_update, name="order_update"),
    path("orders/<int:pk>/delete/", views.order_delete, name="order_delete"),

]