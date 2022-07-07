#MAIN URLS MODULO



from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from icarusProjectApp.views import Login
from icarusProjectApp.views import (

    VueloAPIView,
    CiudadAPIView,
    AvionAPIView,
    VueloListAPIView,
    PagoAPIView,
    PagoListAPIView,

)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('vuelos/', VueloAPIView.as_view(), name = "vuelos"),
    path('ciudades/', CiudadAPIView.as_view(), name = "ciudades"),
    path('aviones/', AvionAPIView.as_view(), name = "aviones"),
    path('vuelo/<int:pk>', VueloListAPIView.as_view(), name ="vuelo"),
    path('pagos/', PagoAPIView.as_view(), name = "pagos"),
    path('pago/<int:pk>', PagoListAPIView.as_view(), name ="pago"),
    path('api/', include('icarusProjectApp.urls')),
    path('',Login.as_view(), name = 'Login'),

]

