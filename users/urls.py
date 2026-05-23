from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import login_view, register_view, logout_view, profile_view

app_name = 'users'

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
]
