from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from vehicle.models import Vehicle
from .models import Service, Order
from .forms import OrderForm, ServiceForm

from django.db.models import Count


def service_list(request):
    q = request.GET.get("q", "")
    sort = request.GET.get("sort", "")

    services = Service.objects.annotate(
        popularity=Count("orders", distinct=True)
    )

    if q:
        services = services.filter(
            (Q(description__icontains=q) |
             Q(vehicle__brand__icontains=q)))

    if sort == "price_asc":
        services = services.order_by("initial_price")

    elif sort == "price_desc":
        services = services.order_by("-initial_price")

    elif sort == "popular":
        services = services.order_by("-popularity", "-service_id")

    else:
        services = services.order_by("-service_id")

    return render(request, "services/services.html", {
        "services": services,
        "q": q,
        "sort": sort,
    })


@login_required
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if request.method == "POST":
        form = OrderForm(request.POST)

        form.fields["vehicle"].queryset = Vehicle.objects.filter(
            owner=request.user
        )

        if form.is_valid():
            order = form.save(commit=False)

            order.user = request.user
            order.service = service
            order.status = "new"

            order.save()

            return redirect("orders:order_list")

    else:
        form = OrderForm()

        form.fields["vehicle"].queryset = Vehicle.objects.filter(
            owner=request.user
        )

    return render(request, "services/services_detail.html", {
        "service": service,
        "form": form
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-order_id")

    search_query = request.GET.get("search", "")

    if search_query:
        orders = orders.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(vehicle__brand__icontains=search_query) |
            Q(vehicle__model__icontains=search_query) |
            Q(vehicle__plate_number__icontains=search_query)
        )

    return render(request, "orders/orders.html", {
        "orders": orders,
        "search_query": search_query
    })


@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            messages.success(request, "Заказ создан.")
            return redirect("orders:order_list")

    else:
        form = OrderForm()

    return render(request, "orders/orders.html", {
        "form": form
    })


def home(request):
    return render(request, "index.html")


def about_list(request):
    return render(request, 'about.html')


def reviews(request):
    return render(request, 'reviews.html')


def prices(request):
    return render(request, 'prices.html')
