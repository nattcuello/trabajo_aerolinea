from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vuelos/', include('vuelos.urls')),
    path('pasajeros/', include('pasajeros.urls')),
    path('reservas/', include('reservas.urls')),
<<<<<<< HEAD
    path('', include('home.urls')),

=======
    path('pasajeros/', include('pasajeros.urls')),
>>>>>>> 3332a1e (templates pasajeros list y detail)

]
