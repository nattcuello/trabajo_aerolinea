# trabajo_aerolineas/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vuelos.views_api import AvionViewSet, VueloViewSet
from reservas.views_api import AsientoViewSet, AsientoVueloViewSet, ReservaViewSet
from pasajeros.views_api import PasajeroViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r"aviones", AvionViewSet, basename="api-aviones")
router.register(r"vuelos", VueloViewSet, basename="api-vuelos")
router.register(r"asientos", AsientoViewSet, basename="api-asientos")
router.register(r"asientos-vuelo", AsientoVueloViewSet, basename="api-asientos-vuelo")
router.register(r"reservas", ReservaViewSet, basename="api-reservas")
router.register(r"pasajeros", PasajeroViewSet, basename="api-pasajeros")

urlpatterns = [
    path("token/", obtain_auth_token, name="api-token"),  # POST: {"username","password"}
    path("", include(router.urls)),
    # Sub-API de usuarios: /api/usuarios/perfiles/
    path("usuarios/", include("usuarios.api_urls")),
]
