from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import OrderForm, OrderManageForm
from .models import Order, Service


def staff_required(user):
    return user.is_authenticated and getattr(user, "can_manage_orders", False)


def service_list(request):
    q = request.GET.get("q", "")
    sort = request.GET.get("sort", "")

    services = Service.objects.annotate(popularity=Count("orders", distinct=True))

    if q:
        services = services.filter(Q(title__icontains=q) | Q(description__icontains=q))

    if sort == "price_asc":
        services = services.order_by("initial_price")
    elif sort == "price_desc":
        services = services.order_by("-initial_price")
    elif sort == "popular":
        services = services.order_by("-popularity", "-service_id")
    else:
        services = services.order_by("-service_id")

    return render(request, "services/services.html", {"services": services, "q": q, "sort": sort})


@login_required
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    user_vehicles = request.user.vehicles.all()

    if request.method == "POST":
        form = OrderForm(request.POST, user=request.user, service=service)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.service = service
            order.status = "new"
            order.save()
            messages.success(request, "Заявка создана.")
            return redirect("orders:order_list")
    else:
        form = OrderForm(user=request.user, service=service)

    return render(request, "services/services_detail.html", {
        "service": service,
        "form": form,
        "user_vehicles": user_vehicles
    })


@login_required
def order_list(request):
    if getattr(request.user, "can_manage_orders", False):
        orders = Order.objects.select_related("user", "vehicle", "service", "master").all()
        if request.user.role == "master" and not request.user.is_staff and not request.user.is_superuser:
            orders = orders.filter(Q(master=request.user) | Q(master__isnull=True))
    else:
        orders = Order.objects.filter(user=request.user).select_related("vehicle", "service", "master")

    search_query = request.GET.get("search", "")
    status = request.GET.get("status", "")

    if search_query:
        orders = orders.filter(
            Q(name__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(vehicle__brand__icontains=search_query)
            | Q(vehicle__model__icontains=search_query)
            | Q(vehicle__plate_number__icontains=search_query)
            | Q(master__full_name__icontains=search_query)
        )

    if status:
        orders = orders.filter(status=status)

    return render(request, "orders/orders.html", {"orders": orders, "search_query": search_query, "status": status, "status_choices": Order.STATUS_CHOICES})


@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, "Заказ создан.")
            return redirect("orders:order_list")
    else:
        form = OrderForm(user=request.user)

    return render(request, "orders/order_form.html", {"form": form, "title": "Создание заказа", "button_text": "Создать заказ"})


@login_required
@user_passes_test(staff_required)
def order_manage(request, pk):
    order = get_object_or_404(Order.objects.select_related("user", "vehicle", "service", "master"), pk=pk)

    if request.method == "POST":
        form = OrderManageForm(request.POST, instance=order, user=request.user)
        if form.is_valid():
            managed_order = form.save(commit=False)
            if request.user.role == "master" and not request.user.is_staff and not request.user.is_superuser:
                managed_order.master = request.user
            managed_order.save()
            messages.success(request, "Заказ обновлён.")
            return redirect("orders:order_list")
    else:
        form = OrderManageForm(instance=order, user=request.user)

    return render(request, "orders/order_manage.html", {"form": form, "order": order})


@login_required
@user_passes_test(staff_required)
def schedule_calendar(request):
    selected_date = request.GET.get("date")
    orders = Order.objects.select_related("user", "vehicle", "service", "master").exclude(appointment_at__isnull=True)

    if request.user.role == "master" and not request.user.is_staff and not request.user.is_superuser:
        orders = orders.filter(master=request.user)

    if selected_date:
        orders = orders.filter(appointment_at__date=selected_date)

    orders = orders.order_by("appointment_at")
    grouped = OrderedDict()
    for order in orders:
        local_dt = timezone.localtime(order.appointment_at) if timezone.is_aware(order.appointment_at) else order.appointment_at
        grouped.setdefault(local_dt.date(), []).append(order)

    return render(request, "orders/calendar.html", {"grouped_orders": grouped, "selected_date": selected_date})


def home(request):
    services = Service.objects.annotate(popularity=Count("orders")).order_by("-popularity")[:6]
    return render(request, "index.html", {"services": services})


def about_list(request):
    return render(request, 'about.html')


def reviews(request):
    return render(request, 'reviews.html')
