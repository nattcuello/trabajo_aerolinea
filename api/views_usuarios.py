# api/views_usuarios.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import SoftDeleteModelViewSet
from usuarios.models import PerfilUsuario
from usuarios.serializers import PerfilUsuarioSerializer


class PerfilUsuarioViewSet(SoftDeleteModelViewSet):
    """
    API centralizada de PerfilUsuario.
    - Soft delete/restore heredados del core.
    - Búsqueda por username/email/rol.
    - Filtros por rol, user, is_active.
    - Endpoint extra: GET /api/usuarios/perfiles/me/ (perfil del usuario autenticado).
    """
    queryset = PerfilUsuario.objects.select_related("user").all()
    serializer_class = PerfilUsuarioSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["rol", "user", "is_active"]
    search_fields = ["rol", "user__username", "user__email", "user__first_name", "user__last_name"]
    ordering_fields = ["id", "rol", "user", "is_active"]
    ordering = ["id"]

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """
        Devuelve el perfil del usuario autenticado.
        """
        u = request.user
        if not u or not u.is_authenticated:
            return Response({"detail": "No autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

        perfil = getattr(u, "perfil", None)  # gracias a User.perfil (property del modelo)
        if not perfil:
            return Response({"detail": "El usuario no tiene perfil asociado."}, status=status.HTTP_404_NOT_FOUND)

        return Response(self.get_serializer(perfil).data)

