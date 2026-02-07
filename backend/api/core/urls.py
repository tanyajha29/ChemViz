from django.urls import path

from .views import healthcheck, logout, me, register, PublicAuthTokenView

urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('register/', register, name='register'),
    path('token/', PublicAuthTokenView.as_view(), name='api-token'),
    path('me/', me, name='me'),
    path('profile/', me, name='profile'),
    path('logout/', logout, name='logout'),
]
