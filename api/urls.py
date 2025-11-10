# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# ⬇️ importa desde api.*
from api.views_vuelos import AvionViewSet, VueloViewSet
from api.views_reservas import AsientoViewSet, AsientoVueloViewSet, ReservaViewSet
from api.views_pasajeros import PasajeroViewSet
from api.views_usuarios import PerfilUsuarioViewSet  # si lo usás
from api.auth import token_view
from api.auth import token_view, token_view_rotate, token_revoke                # tu token documentado

router = DefaultRouter()
router.register(r"aviones", AvionViewSet, basename="avion")
router.register(r"vuelos", VueloViewSet, basename="vuelo")
router.register(r"asientos", AsientoViewSet, basename="asiento")
router.register(r"asientos-vuelo", AsientoVueloViewSet, basename="asiento-vuelo")
router.register(r"reservas", ReservaViewSet, basename="reserva")
router.register(r"pasajeros", PasajeroViewSet, basename="pasajero")  # ⬅️ NUEVO
router.register(r"usuarios/perfiles", PerfilUsuarioViewSet, basename="perfil-usuario")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", token_view, name="token"),
    path("token/rotate/", token_view_rotate, name="token-rotate"),   # opcional
    path("token/revoke/", token_revoke, name="token-revoke"),
]