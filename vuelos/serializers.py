from rest_framework import serializers
from .models import Avion, Vuelo

class AvionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avion
        fields = "__all__"

class VueloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vuelo
        fields = "__all__"

    def validate(self, data):
        # opcional: si querés validar fechas
        fs = data.get("fecha_salida") or getattr(self.instance, "fecha_salida", None)
        fl = data.get("fecha_llegada") or getattr(self.instance, "fecha_llegada", None)
        if fs and fl and fl <= fs:
            raise serializers.ValidationError("La llegada debe ser posterior a la salida")
        return data

