from django.urls import path

from .views import healthcheck, register

urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('register/', register, name='register'),
]
