from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import login_view, register_view

app_name = 'users'

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="orders:home"), name="logout"),
    path("register/", register_view, name="register"),


]