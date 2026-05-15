from django import views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import F
from django.urls import path

from .models import Vehicle
from .forms import VehicleForm

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    search_query = request.GET.get('search', '')

    if search_query:
        vehicles = vehicles.filter(name__icontains=search_query)

    context = {
        'vehicles': vehicles,
        'search_query': search_query
    }

    return render(request, "vehicle/vehicle.html", context)


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return render(
        request,
        "vehicle/detail_vehicle.html",
        {"shop:vehicle": vehicle},
    )

def vehicle_create(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Автомобиль создан.")
            return redirect("shop:vehicle_list")
    else:
        form = VehicleForm()
    return render(request, "vehicle/create_vehicle.html", {"form": form})

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные автомобиля обновлены.")
            return redirect("shop:vehicle_detail", pk=pk)
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, "vehicle/update_vehicle.html", {"form": form})

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        vehicle.delete()
        messages.success(request, "Автомобиль удалён.")
        return redirect("shop:vehicle_list")
    return render(request, "vehicle/delete_vehicle.html", {"vehicle": vehicle})

def home(request):
    return render(request, "index.html")