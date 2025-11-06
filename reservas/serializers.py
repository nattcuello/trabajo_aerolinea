# reservas/serializers.py
from rest_framework import serializers
from core.serializers_mixins import AuditFieldsSerializer, IntegrityFriendlyMixin
from .models import Asiento, AsientoVuelo, Reserva, Boleto
from pasajeros.models import Pasajero
from vuelos.models import Vuelo


class AsientoSerializer(IntegrityFriendlyMixin, AuditFieldsSerializer):
    class Meta(AuditFieldsSerializer.Meta):
        model = Asiento
        fields = "__all__"
        read_only_fields = AuditFieldsSerializer.Meta.read_only_fields


class AsientoVueloSerializer(IntegrityFriendlyMixin, AuditFieldsSerializer):
    class Meta(AuditFieldsSerializer.Meta):
        model = AsientoVuelo
        fields = "__all__"
        read_only_fields = AuditFieldsSerializer.Meta.read_only_fields


class ReservaSerializer(IntegrityFriendlyMixin, AuditFieldsSerializer):
    class Meta(AuditFieldsSerializer.Meta):
        model = Reserva
        fields = "__all__"
        read_only_fields = AuditFieldsSerializer.Meta.read_only_fields + ("fecha_reserva",)

    def validate(self, attrs):
        pasajero = attrs.get("pasajero")
        vuelo = attrs.get("vuelo")

        if pasajero and vuelo:
            existe = Reserva.objects.filter(pasajero=pasajero, vuelo=vuelo)
            if self.instance:
                existe = existe.exclude(pk=self.instance.pk)
            if existe.exists():
                raise serializers.ValidationError({"pasajero": "Ya existe una reserva activa para este pasajero en este vuelo."})

        return attrs

class BoletoSerializer(IntegrityFriendlyMixin, AuditFieldsSerializer):
    class Meta(AuditFieldsSerializer.Meta):
        model = Boleto
        fields = "__all__"
        read_only_fields = AuditFieldsSerializer.Meta.read_only_fields
