from rest_framework import serializers
from .models import Avion, Vuelo

class AvionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avion
        fields = '__all__'

class VueloSerializer(serializers.ModelSerializer):
    avion_modelo = serializers.CharField(source='avion.modelo', read_only=True)
    class Meta:
        model = Vuelo
        fields = '__all__'

    def validate(self, data):
        if data.get('fecha_llegada') <= data.get('fecha_salida'):
            raise serializers.ValidationError("La llegada debe ser posterior a la salida")
        return data
