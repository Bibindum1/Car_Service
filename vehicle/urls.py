
from django.urls import path
from . import views

app_name = 'vehicle'

urlpatterns = [
    path("", views.home, name="home"),
    # Vehicle
    path("vehicles/", views.vehicle_list, name="vehicle_list"),
    path("vehicles/<int:pk>/", views.vehicle_detail, name="vehicle_detail"),
    path("vehicles/create/", views.vehicle_create, name="vehicle_create"),
    path("vehicles/<int:pk>/update/", views.vehicle_update, name="vehicle_update"),
    path("vehicles/<int:pk>/delete/", views.vehicle_delete, name="vehicle_delete"),
]