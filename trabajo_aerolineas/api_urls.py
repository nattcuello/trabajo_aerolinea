# trabajo_aerolineas/api_urls.py

from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token

from drf_spectacular.utils import extend_schema, OpenApiExample

# ViewSets (API principal)
from vuelos.views_api import AvionViewSet, VueloViewSet
from reservas.views_api import AsientoViewSet, AsientoVueloViewSet, ReservaViewSet
from pasajeros.views_api import PasajeroViewSet

# Sub-API de usuarios (perfil de usuario vía router DRF)
# Nota: en usuarios/api_urls.py debés tener el router con PerfilUsuarioViewSet
from django.urls import include as django_include  # alias para claridad


# ---------------------------
# Serializers SOLO para doc del endpoint /api/token/
# ---------------------------
class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


# ---------------------------
# /api/token/ (documentado para Swagger/Redoc)
# ---------------------------
@extend_schema(
    tags=["auth"],
    request=TokenRequestSerializer,
    responses={200: TokenResponseSerializer},
    examples=[
        OpenApiExample(
            "Ejemplo de request",
            value={"username": "sofia", "password": "270620"},
            request_only=True,
        ),
        OpenApiExample(
            "Ejemplo de response",
            value={"token": "983a0160d7637a470788f0a6cdead117b08e3b3b"},
            response_only=True,
        ),
    ],
    description="Obtiene un token de autenticación. Enviar username y password.",
)
@api_view(["POST"])
@permission_classes([AllowAny])
def token_view(request):
    """
    Genera (o devuelve) el token del usuario autenticado.
    Implementado con DRF para evitar el error de Request al envolver obtain_auth_token.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    # Validación simple
    if not username or not password:
        return Response(
            {"detail": "username y password son obligatorios."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Autenticar
    from django.contrib.auth import authenticate

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"detail": "Credenciales inválidas."}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_200_OK)


# ---------------------------
# Router de la API principal
# ---------------------------
router = DefaultRouter()
router.register(r"aviones", AvionViewSet, basename="avion")
router.register(r"vuelos", VueloViewSet, basename="vuelo")
router.register(r"asientos", AsientoViewSet, basename="asiento")
router.register(r"asientos-vuelo", AsientoVueloViewSet, basename="asiento-vuelo")
router.register(r"reservas", ReservaViewSet, basename="reserva")
router.register(r"pasajeros", PasajeroViewSet, basename="pasajero")


# ---------------------------
# URL patterns finales
# ---------------------------
urlpatterns = [
    # Endpoints del router principal
    path("", include(router.urls)),

    # Sub-API de usuarios: /api/usuarios/perfiles/...
    path("usuarios/", django_include("usuarios.api_urls")),

    # Auth por token (documentado correctamente)
    path("token/", token_view, name="token"),
]