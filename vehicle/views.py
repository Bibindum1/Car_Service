from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Vehicle
from .forms import VehicleForm

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(owner=request.user)
    search_query = request.GET.get('search', '')

    if search_query:
        vehicles = vehicles.filter(
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(vin__icontains=search_query)
        )

    context = {
        'vehicles': vehicles,
        'search_query': search_query
    }

    return render(request, "vehicle/vehicle.html", context)

@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return render(
        request,
        "vehicle/detail_vehicle.html",
        {"vehicle": vehicle},
    )

@login_required
def vehicle_create(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)

        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()

            messages.success(request, "Автомобиль создан.")
            return redirect("vehicle:vehicle_list")
    else:
        form = VehicleForm()

    return render(request, "vehicle/create_vehicle.html", {
        "form": form
    })

@login_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(
        Vehicle,
        pk=pk,
        owner=request.user
    )
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные автомобиля обновлены.")
            return redirect("vehicle:vehicle_detail", pk=pk)
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, "vehicle/update_vehicle.html", {"form": form})

@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(
        Vehicle,
        pk=pk,
        owner=request.user
    )
    if request.method == "POST":
        vehicle.delete()
        messages.success(request, "Автомобиль удалён.")
        return redirect("vehicle:vehicle_list")
    return render(request, "vehicle/delete_vehicle.html", {"vehicle": vehicle})

def home(request):
    return render(request, "index.html")