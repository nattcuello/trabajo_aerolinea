# vuelos/views_api.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.viewsets import SoftDeleteModelViewSet
from .models import Avion, Vuelo
from .serializers import AvionSerializer, VueloSerializer

class AvionViewSet(SoftDeleteModelViewSet):
    queryset = Avion.objects.all()
    serializer_class = AvionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["modelo", "capacidad", "is_active"]
    search_fields = ["modelo"]
    ordering_fields = ["capacidad", "modelo", "id"]

class VueloViewSet(SoftDeleteModelViewSet):
    queryset = Vuelo.objects.select_related("avion").prefetch_related("usuarios_gestores").all()
    serializer_class = VueloSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["origen", "destino", "estado", "avion", "is_active"]
    search_fields = ["origen", "destino"]
    ordering_fields = ["fecha_salida", "fecha_llegada", "precio_base", "id"]

