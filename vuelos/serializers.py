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


