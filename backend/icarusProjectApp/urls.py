#URLS API

from django.urls import path, include
from rest_framework import routers
from .viewsets import usuario_api_view, usuario_detail_api_view#, UsuarioViewSet, UsuarioViewSetLog


urlpatterns = [
    path('usuario/', usuario_api_view, name = 'usuario_api'),
    path('usuario/<int:pk>', usuario_detail_api_view, name='usuario_detail_api_view'),
]







