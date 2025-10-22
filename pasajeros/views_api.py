from rest_framework import viewsets
from .models import Pasajero
from .serializers import PasajeroSerializer

class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer
