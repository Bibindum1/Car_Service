from django.urls import path

from applications.views import applications_view, create_application_view

urlpatterns = [
    path('applications/', applications_view, name='applications'),
    path('applications/create/', create_application_view, name='create_application'),
]