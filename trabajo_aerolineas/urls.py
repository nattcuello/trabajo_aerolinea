from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from . import api_urls
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)   

def trigger_error(request):
    1/0

urlpatterns = [
 # Admin (única entrada)
    path("admin/", admin.site.urls),

 # Home
    path("", include("home.urls")),
    path("set_language/", set_language, name="set_language"),

 # API REST central (un solo include con el router)
    path("api/", include(api_urls)),
    path("api-auth/", include("rest_framework.urls")),

 # Swagger / OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

 # Debug Sentry (si querés mantenerlo)
    path("sentry-debug/", trigger_error),
]


# Vistas HTML por app
# Como ya centralizamos la API en api_urls, estas rutas son solo para templates HTML.

urlpatterns += [
    path("vuelos/", include(("vuelos.urls", "vuelos"), namespace="vuelos")),
    path("pasajeros/", include(("pasajeros.urls", "pasajeros"), namespace="pasajeros")),
    path("usuarios/", include(("usuarios.urls", "usuarios"), namespace="usuarios")),
    path("reservas/", include(("reservas.urls", "reservas"), namespace="reservas")),
]


# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

