from rest_framework import serializers
from .models import Pasajero

class PasajeroSerializer(serializers.ModelSerializer):
    edad = serializers.ReadOnlyField()

    class Meta:
        model = Pasajero
        fields = '__all__'
