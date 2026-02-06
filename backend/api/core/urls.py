from django.urls import path

from .views import healthcheck, me, register, PublicAuthTokenView

urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('register/', register, name='register'),
    path('token/', PublicAuthTokenView.as_view(), name='api-token'),
    path('me/', me, name='me'),
]
