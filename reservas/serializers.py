from rest_framework import serializers
from .models import Asiento, AsientoVuelo, Reserva
from vuelos.models import Vuelo
from pasajeros.models import Pasajero

class AsientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asiento
        fields = "__all__"

class AsientoVueloSerializer(serializers.ModelSerializer):
    asiento = AsientoSerializer(read_only=True)
    asiento_id = serializers.PrimaryKeyRelatedField(
        queryset=Asiento.objects.all(), source="asiento", write_only=True
    )
    class Meta:
        model = AsientoVuelo
        fields = ["id","vuelo","asiento","asiento_id","estado"]

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"
        read_only_fields = ["fecha_reserva", "precio_final"]

class ReservaCreateSerializer(serializers.Serializer):
    vuelo_id = serializers.IntegerField()
    pasajero_id = serializers.IntegerField()
    asientovuelo_id = serializers.IntegerField()

    def create(self, data):
        vuelo = Vuelo.objects.get(pk=data["vuelo_id"])
        pasajero = Pasajero.objects.get(pk=data["pasajero_id"])
        av = AsientoVuelo.objects.select_related("vuelo").get(pk=data["asientovuelo_id"])
        if av.vuelo_id != vuelo.id:
            raise serializers.ValidationError("El asiento no pertenece a ese vuelo.")
        if getattr(av, "estado", "disponible") != "disponible":
            raise serializers.ValidationError("El asiento ya no está disponible.")
        if Reserva.objects.filter(vuelo=vuelo, pasajero=pasajero).exists():
            raise serializers.ValidationError("El pasajero ya tiene una reserva en este vuelo.")
        reserva = Reserva.objects.create(
            vuelo=vuelo, pasajero=pasajero, asiento=av,
            estado="confirmada", precio_final=vuelo.precio_base
        )
        try:
            av.estado = "ocupado"; av.save(update_fields=["estado"])
        except Exception:
            pass
        return reserva
