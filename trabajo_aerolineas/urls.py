from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from . import api_urls


def trigger_error(request):
    division_by_zero = 1 / 0

# Rutas que no dependen de idioma (por ejemplo, cambiar idioma)
urlpatterns = [
    path('set_language/', set_language, name='set_language'),
]

# Rutas que sí dependen del idioma
urlpatterns += ( 
    path("admin/", admin.site.urls),
    path("vuelos/", include(("vuelos.urls", "vuelos"), namespace="vuelos")),
    path("pasajeros/", include(("pasajeros.urls", "pasajeros"), namespace="pasajeros")),
    path("usuarios/", include("usuarios.urls", namespace="usuarios")),
    path("", include("home.urls")),
    path("reservas/", include("reservas.urls", namespace="reservas")),
    path("sentry-debug/", trigger_error),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(api_urls)),
)

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

