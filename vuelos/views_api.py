from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Avion, Vuelo
from .serializers import AvionSerializer, VueloSerializer
from trabajo_aerolineas.permissions import SoloAdminPuedeModificar

class AvionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Avion.objects.all()
    serializer_class = AvionSerializer
    permission_classes = [IsAuthenticated]

class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer
    permission_classes = [IsAuthenticated & SoloAdminPuedeModificar]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['origen', 'destino', 'fecha_salida']
