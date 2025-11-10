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
         """
         - Por defecto: sólo activos (is_active=True).
         - Si ?include_inactive=1|true|True => ignora el manager filtrado y usa _base_manager
         para traer TODOS (activos + inactivos).
         """
         include_inactive = self.request.query_params.get("include_inactive")
        # modelo asociado al qs que definiste en el ViewSet hijo
         model = super().get_queryset().model

         if include_inactive in ("1", "true", "True"):
        # _base_manager evita el filtro de managers custom (ActiveQuerySet, etc.)
            qs = model._base_manager.all()
         else:
        # comportamiento normal: sólo activos
            qs = model._base_manager.all().filter(is_active=True)

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
        """
        Restaura un registro soft-deleted.
        Ignora el manager filtrado (ActiveQuerySet) usando _base_manager.
        """
        model = super().get_queryset().model
        try:
            obj = model._base_manager.get(pk=pk)  # ← evita el filtro de activos
        except model.DoesNotExist:
            return Response(
                {"detail": f"No {model.__name__} matches the given query."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if getattr(obj, "is_active", True):
            return Response(
                {"detail": "El registro ya está activo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Reactivar
        obj.is_active = True
        # (Opcional) limpiar campos de auditoría
        if hasattr(obj, "deleted_at"):
            obj.deleted_at = None
        if hasattr(obj, "deleted_by"):
            obj.deleted_by = None

        # Guardar cambios
        fields = [f for f in ["is_active", "deleted_at", "deleted_by"] if hasattr(obj, f)]
        obj.save(update_fields=fields)

        return Response({"detail": "Registro restaurado."}, status=status.HTTP_200_OK)
