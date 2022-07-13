#URLS API

from django.urls import path, include
from rest_framework import routers
from .views import usuario_api_view, usuario_detail_api_view, reserva_api_view, reserva_detail_api_view


urlpatterns = [
    path('usuario/', usuario_api_view, name = 'usuario_api'),
    path('usuario/<int:pk>', usuario_detail_api_view, name='usuario_detail_api_view'),
    path('reserva/', reserva_api_view, name = 'reserva_api'),
    path('reserva/<int:pk>', reserva_detail_api_view, name='reserva_detail_api_view'),
]







