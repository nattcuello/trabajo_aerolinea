# pasajeros/serializers.py
from rest_framework import serializers
from core.serializers_mixins import AuditFieldsSerializer, IntegrityFriendlyMixin
from .models import Pasajero

class PasajeroSerializer(IntegrityFriendlyMixin, AuditFieldsSerializer):
    class Meta(AuditFieldsSerializer.Meta):
        model = Pasajero
        fields = "__all__"
        read_only_fields = AuditFieldsSerializer.Meta.read_only_fields
        # Si aplicaste constraint único en documento:
        UNIQUE_HINTS = {"uniq_pasajero_documento_activo": "Ya existe un pasajero activo con ese documento."}
