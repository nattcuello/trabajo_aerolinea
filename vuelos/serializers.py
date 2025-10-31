# vuelos/serializers.py
from rest_framework import serializers
from core.serializers_mixins import AuditFieldsSerializer, IntegrityFriendlyMixin
from .models import Avion, Vuelo

class AvionSerializer(IntegrityFriendlyMixin, AuditFieldsSerializer):
    class Meta(AuditFieldsSerializer.Meta):
        model = Avion
        fields = "__all__"
        read_only_fields = AuditFieldsSerializer.Meta.read_only_fields


class VueloSerializer(IntegrityFriendlyMixin, AuditFieldsSerializer):
    class Meta(AuditFieldsSerializer.Meta):
        model = Vuelo
        fields = "__all__"
        read_only_fields = AuditFieldsSerializer.Meta.read_only_fields

    def validate(self, attrs):
        salida = attrs.get("fecha_salida")
        llegada = attrs.get("fecha_llegada")
        if salida and llegada and llegada <= salida:
            raise serializers.ValidationError(
                {"fecha_llegada": "La fecha de llegada debe ser posterior a la salida."}
            )
        return attrs

