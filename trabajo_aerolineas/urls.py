from django.contrib import admin
from django.urls import path, include

# Para servir archivos estáticos en desarrollo
from django.conf import settings
from django.conf.urls.static import static

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vuelos/', include(('vuelos.urls', 'vuelos'), namespace='vuelos')),
    path('pasajeros/', include(('pasajeros.urls', 'pasajeros'), namespace='pasajeros')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('', include('home.urls')),
    path('sentry-debug/', trigger_error),

    # Solo UNA vez la app reservas con namespace
    path('reservas/', include('reservas.urls', namespace='reservas')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
