from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.utils.http import url_has_allowed_host_and_scheme

from orders.models import Order
from vehicle.models import Vehicle
from .forms import RegisterForm, LoginForm


def safe_redirect(request, url, default_name='orders:home'):
    if not url or url == 'None':
        return redirect(default_name)

    if url_has_allowed_host_and_scheme(
        url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        return redirect(url)

    return redirect(default_name)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('orders:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('orders:home')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('orders:home')

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return safe_redirect(request, next_url)
    else:
        form = LoginForm(request)

    return render(request, 'registration/login.html', {
        'form': form,
        'next': next_url,
    })

def logout_view(request):

    if request.method == "POST":
        logout(request)
        return redirect('users:login')

    return render(request, 'registration/logout.html')

@login_required
def profile_view(request):

    vehicles = Vehicle.objects.filter(
        owner=request.user
    )

    orders = Order.objects.filter(
        user=request.user
    ).select_related(
        "vehicle",
        "service"
    ).order_by("-created_at")

    return render(request, "profile/profile.html", {
        "vehicles": vehicles,
        "orders": orders,
    })