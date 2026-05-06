from django import views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import F
from django.urls import path

from .models import Service, Order
from .forms import  ServiceForm, OrderForm

def service_list(request):
    services = (
        Service.objects.select_related("customer", "vehicle")
        .order_by("-date")
    )
    return render(request, "", {"shop:services": services})

def service_detail(request, pk):
    service = get_object_or_404(
        Service.objects.select_related("shop:customer", "vehicle"),
        pk=pk,
    )
    return render(
        request,
        "",
        {"shop:service": service},
    )

def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Услуга создана.")
            return redirect("shop:service_list")
    else:
        form = ServiceForm()
    return render(request, "", {"form": form})

def service_update(request, pk):
    service = get_object_or_404(
        Service.objects.select_related("shop:customer", "vehicle"),
        pk=pk,
    )
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные услуги обновлены.")
            return redirect("shop:service_detail", pk=pk)
    else:
        form = ServiceForm(instance=service)
    return render(request, "", {"form": form})

def service_delete(request, pk):
    service = get_object_or_404(
        Service.objects.select_related("customer", "vehicle"),
        pk=pk,
    )
    if request.method == "POST":
        service.delete()
        messages.success(request, "Услуга удалена.")
        return redirect("shop:service_list")
    return render(request, "", {"service": service})

def order_list(request):
    orders = (
        Order.objects.select_related("customer", "vehicle")
        .order_by("-date")
    )
    return render(request, "orders/orders.html", {"shop:orders": orders})

def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заказ создан.")
            return redirect("shop:order_list")
    else:
        form = OrderForm()
    return render(request, "orders/create_order.html", {"form": form})

def order_update(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("customer", "vehicle"),
        pk=pk,
    )
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные заказа обновлены.")
            return redirect("shop:order_detail", pk=pk)
    else:
        form = OrderForm(instance=order)
    return render(request, "orders/update_order.html", {"form": form})

def order_delete(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("customer", "vehicle"),
        pk=pk,
    )
    if request.method == "POST":
        order.delete()
        messages.success(request, "Заказ удалён.")
        return redirect("shop:order_list")
    return render(request, "orders/delete_order.html", {"order": order})

def home(request):
    return render(request, "index.html")