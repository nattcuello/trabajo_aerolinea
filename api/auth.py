# api/auth.py
# api/auth.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiExample


# ---------------------------
# Serializers solo para documentación
# ---------------------------
class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


# ---------------------------
# /api/token/ : devuelve (o crea) el token del usuario
# ---------------------------
@extend_schema(
    tags=["auth"],
    request=TokenRequestSerializer,
    responses={200: TokenResponseSerializer},
    examples=[
        OpenApiExample("Ejemplo request", value={"username": "imanol", "password": "0123456789"}, request_only=True),
        OpenApiExample("Ejemplo response", value={"token": "xxxxxxxx"}, response_only=True),
    ],
    description="Obtiene el token del usuario. Usar en Authorization: **Token &lt;token&gt;**.",
)
@api_view(["POST"])
@permission_classes([AllowAny])
def token_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"detail": "username y password son obligatorios."},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"detail": "Credenciales inválidas."},
                        status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)  # token estable
    return Response({"token": token.key}, status=status.HTTP_200_OK)


# ---------------------------
# /api/token/rotate/ : emite un token nuevo y revoca el anterior (opcional)
# ---------------------------
@extend_schema(
    tags=["auth"],
    request=TokenRequestSerializer,
    responses={200: TokenResponseSerializer},
    description="(Opcional) Emite un token nuevo y revoca el anterior.",
)
@api_view(["POST"])
@permission_classes([AllowAny])
def token_view_rotate(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"detail": "username y password son obligatorios."},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"detail": "Credenciales inválidas."},
                        status=status.HTTP_400_BAD_REQUEST)

    Token.objects.filter(user=user).delete()
    token = Token.objects.create(user=user)
    return Response({"token": token.key}, status=status.HTTP_200_OK)


# ---------------------------
# /api/token/revoke/ : invalida el token actual (logout API)
# ---------------------------
@extend_schema(
    tags=["auth"],
    responses={204: None},
    description="Revoca el token del usuario autenticado (logout). "
                "Requiere header Authorization: **Token &lt;token&gt;**.",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def token_revoke(request):
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

