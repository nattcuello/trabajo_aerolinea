# api/pasajeros.py
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import SoftDeleteModelViewSet  # tu base con soft-delete y permisos
from pasajeros.models import Pasajero
from pasajeros.serializers import PasajeroSerializer


class PasajeroViewSet(SoftDeleteModelViewSet):
    """
    ViewSet centralizado de Pasajero (API).
    - Soft delete (DELETE marca is_active=False y setea deleted_*).
    - Acción extra: POST /{id}/restore/ para reactivar.
    - Filtro 'is_active' True por defecto; ?include_inactive=1 para traer todos.
    - Búsqueda/ordenamiento expuestos en Swagger.
    """
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer

    # Filtros/búsqueda/orden (requiere DjangoFilterBackend configurado en settings)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # Ajustá estos campos a los que tengas en tu modelo:
    search_fields = ["nombre", "tipo_documento", "documento","email", "telefono", "fecha_nacimiento"]
    ordering_fields = ["id", "nombre", "tipo_documento", "documento", "is_active"]
    ordering = ["id"]

    def get_queryset(self):
        qs = super().get_queryset()
        # Por defecto, sólo activos. Si ?include_inactive=1, trae todos.
        include_inactive = self.request.query_params.get("include_inactive")
        if not include_inactive:
            qs = qs.filter(is_active=True)
        return qs
