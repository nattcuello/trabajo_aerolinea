from django.contrib import admin
from django.urls import path, include

# 👇 ESTAS DOS IMPORTACIONES SON CLAVE PARA SERVIR LOS ARCHIVOS ESTÁTICOS
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vuelos/', include('vuelos.urls')),
    path('pasajeros/', include('pasajeros.urls')),
    path('reservas/', include('reservas.urls')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('', include('home.urls')),
    path('pasajeros/', include('pasajeros.urls')),
    path('pasajeros/', include('pasajeros.urls')),
]

# ✅ Agregá esto tal como está al final del archivo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])