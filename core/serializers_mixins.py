# core/serializers_mixins.py
from rest_framework import serializers
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _

class IntegrityFriendlyMixin:
    """Captura IntegrityError y da mensajes legibles."""
    UNIQUE_HINTS = {}

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(self._map_integrity_error(e))

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                return super().update(instance, validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(self._map_integrity_error(e))

    def _map_integrity_error(self, err: IntegrityError):
        msg = str(err)
        for constraint, friendly in self.UNIQUE_HINTS.items():
            if constraint in msg:
                return {"detail": friendly}
        return {"detail": _("Error de integridad o duplicado.")}


class AuditFieldsSerializer(serializers.ModelSerializer):
    """Agrega campos de auditoría read-only a cualquier serializer."""
    class Meta:
        fields = "__all__"
        read_only_fields = ("is_active", "deleted_at", "deleted_by")
