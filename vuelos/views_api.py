from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Avion, Vuelo
from .serializers import AvionSerializer, VueloSerializer
from trabajo_aerolineas.permissions import IsAdminOrOperadorOrReadOnly  # <—

class AvionViewSet(viewsets.ModelViewSet):
    queryset = Avion.objects.all()
    serializer_class = AvionSerializer
    permission_classes = [IsAdminOrOperadorOrReadOnly]

class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.all().order_by("fecha_salida")
    serializer_class = VueloSerializer
    permission_classes = [IsAdminOrOperadorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "origen": ["exact", "icontains"],
        "destino": ["exact", "icontains"],
        "fecha_salida": ["date", "gte", "lte"],
    }
