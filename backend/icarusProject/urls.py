#MAIN URLS MODULO



from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api-auth/', include('rest_framework.urls')),


    #urls de la api
    path('api/', include('icarusProjectApp.urls')),
]

