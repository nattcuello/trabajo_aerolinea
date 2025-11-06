# trabajo_aerolineas/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Sitio (home + autenticación web de usuarios)
    path("", include("home.urls")),
    path("usuarios/", include(("usuarios.urls", "usuarios"), namespace="usuarios")),

    # API central (router DRF + sub-API de usuarios + token)
    path("api/", include("trabajo_aerolineas.api_urls")),

    # exponer la documentación
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # (opcional) login/logout de la browsable API
    path("api-auth/", include("rest_framework.urls")),
]
