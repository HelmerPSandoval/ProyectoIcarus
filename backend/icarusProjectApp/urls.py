
from django.urls import path, include
from rest_framework import routers
from .viewsets import UsuarioViewSet


route = routers.SimpleRouter()

#registramos las rutas de la clase que definimos para luego llamarlas de la url global
route.register('usuario', UsuarioViewSet)

#se generan de manera automatica
urlpatterns = route.urls
