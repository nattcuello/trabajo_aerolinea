from django.contrib import admin
from django.urls import path, include

# 👇 ESTAS DOS IMPORTACIONES SON CLAVE PARA SERVIR LOS ARCHIVOS ESTÁTICOS
from django.conf import settings
from django.conf.urls.static import static



def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vuelos/', include(('vuelos.urls', 'vuelos'), namespace='vuelos')),
    path('pasajeros/', include(('pasajeros.urls', 'pasajeros'), namespace='pasajeros')),
    path('reservas/', include('reservas.urls')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('', include('home.urls')),
    path('sentry-debug/', trigger_error),
]



# ✅ Agregá esto tal como está al final del archivo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])