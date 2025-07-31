from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vuelos/', include('vuelos.urls')),
    path('pasajeros/', include('pasajeros.urls')),
    path('reservas/', include('reservas.urls')),
<<<<<<< HEAD
<<<<<<< HEAD
    path('', include('home.urls')),

=======
    path('pasajeros/', include('pasajeros.urls')),
>>>>>>> 3332a1e (templates pasajeros list y detail)
=======
    path('pasajeros/', include('pasajeros.urls')),
>>>>>>> 00e2955a1d20be3457177b808c4cc7a859905a19

]
