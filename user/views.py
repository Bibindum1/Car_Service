from django import views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import F
from django.urls import path

from .models import Customer
from .forms import CustomerForm

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "user/user.html", {"shop:customers": customers})


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(
        request,
        "user/detail_user.html",
        {"shop:customer": customer},
    )

def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Клиент создан.")
            return redirect("shop:customer_list")
    else:
        form = CustomerForm()
    return render(request, "user/create_user.html", {"form": form})


def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные клиента обновлены.")
            return redirect("shop:customer_detail", pk=pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, "user/update_user.html", {"form": form})


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        messages.success(request, "Клиент удалён.")
        return redirect("shop:customer_list")
    return render(request, "user/delete_user.html", {"customer": customer})

