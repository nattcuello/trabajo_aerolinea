from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vuelos/', include('vuelos.urls')),
    path('pasajeros/', include('pasajeros.urls')),
    path('reservas/', include('reservas.urls')),
<<<<<<< HEAD

]
=======
]
>>>>>>> 8adfaff1926169654ce8d00882a278eddd1a4598
