# reservas/views_api.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.viewsets import SoftDeleteModelViewSet
from .models import Asiento, AsientoVuelo, Reserva
from .serializers import AsientoSerializer, AsientoVueloSerializer, ReservaSerializer

class AsientoViewSet(SoftDeleteModelViewSet):
    queryset = Asiento.objects.select_related("avion").all()
    serializer_class = AsientoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["avion", "tipo", "estado", "is_active"]
    search_fields = ["tipo", "estado"]
    ordering_fields = ["fila", "columna", "id"]

class AsientoVueloViewSet(SoftDeleteModelViewSet):
    queryset = AsientoVuelo.objects.select_related("vuelo", "asiento").all()
    serializer_class = AsientoVueloSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["vuelo", "asiento", "estado", "is_active"]
    search_fields = ["estado", "vuelo__origen", "vuelo__destino"]
    ordering_fields = ["id"]

class ReservaViewSet(SoftDeleteModelViewSet):
    queryset = Reserva.objects.select_related("pasajero", "vuelo", "asiento").all()
    serializer_class = ReservaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["pasajero", "vuelo", "estado", "is_active"]
    search_fields = ["pasajero__nombre", "vuelo__origen", "vuelo__destino"]
    ordering_fields = ["fecha_reserva", "precio_final", "id"]


