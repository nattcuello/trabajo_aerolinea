# core/viewsets.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone

class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    """
    - Filtra por defecto is_active=True.
    - DELETE => soft delete (is_active=False, deleted_at, deleted_by).
    - Acción extra: POST {id}/restore/ para reactivar.
    - ?include_inactive=1 para incluir inactivos en list().
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ()
    ordering_fields = "__all__"
    ordering = ("id",)

    def get_queryset(self):
        qs = super().get_queryset()
        include_inactive = self.request.query_params.get("include_inactive")
        if include_inactive not in ("1", "true", "True"):
            qs = qs.filter(is_active=True)
        return qs

    def perform_destroy(self, instance):
        # soft delete (no cascada)
        if getattr(instance, "is_active", True):
            instance.is_active = False
            if hasattr(instance, "deleted_at"):
                instance.deleted_at = timezone.now()
            if hasattr(instance, "deleted_by"):
                try:
                    instance.deleted_by = self.request.user if self.request and self.request.user.is_authenticated else None
                except Exception:
                    pass
            instance.save(update_fields=[f for f in ["is_active", "deleted_at", "deleted_by"] if hasattr(instance, f)])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": f"{instance.__class__.__name__} soft-deleted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="restore")
    def restore(self, request, pk=None):
        obj = self.get_object()
        if getattr(obj, "is_active", True):
            return Response({"detail": "El registro ya está activo."}, status=status.HTTP_400_BAD_REQUEST)
        obj.is_active = True
        # no tocamos deleted_at/deleted_by para auditoría, salvo que quieras limpiarlos
        obj.save(update_fields=["is_active"])
        return Response({"detail": "Registro restaurado."}, status=status.HTTP_200_OK)
