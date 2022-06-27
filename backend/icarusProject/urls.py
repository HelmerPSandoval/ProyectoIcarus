#MAIN URLS MODULO



from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from icarusProjectApp.viewsets import Login

urlpatterns = [
    path('admin/', admin.site.urls),


    #urls de la api
    path('api/', include('icarusProjectApp.urls')),
    path('',Login.as_view(), name = 'Login'),
]

