from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

from applications.forms import ApplicationForm
from applications.models import Application
from .forms import RegisterForm, LoginForm


def safe_redirect(request, url, default_name='shop:home'):
    if not url:
        return redirect(default_name)
    allowed = url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()},
                                              require_https=request.is_secure())
    if allowed:
        return redirect(url)
    return redirect(default_name)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('shop:home')
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return safe_redirect(request, next_url, default_name='shop:home')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {
        'form': form,
        'next': next_url,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:home')
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return safe_redirect(request, next_url, default_name='shop:home')
    else:
        form = LoginForm(request)

    return render(request, 'registration/login.html', {
        'form': form,
        'next': next_url,
    })


