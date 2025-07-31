from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vuelos/', include('vuelos.urls')),  # esta línea es clave
    path('pasajeros/', include('pasajeros.urls')),

]
