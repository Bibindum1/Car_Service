from django.contrib import admin
from django.urls import path, include

from orders import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("orders.urls")),
]