# api/views_vuelos.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from core.viewsets import SoftDeleteModelViewSet
from vuelos.models import Avion, Vuelo
from vuelos.serializers import AvionSerializer, VueloSerializer


# ---------- Avión ----------
class AvionViewSet(SoftDeleteModelViewSet):
    queryset = Avion.objects.all()
    serializer_class = AvionSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["modelo", "capacidad", "filas", "columnas", "is_active"]
    search_fields = ["modelo"]
    ordering_fields = ["id", "modelo", "capacidad", "filas", "columnas", "is_active"]
    ordering = ["id"]


# ---------- Vuelo ----------
class VueloViewSet(SoftDeleteModelViewSet):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        "avion", "origen", "destino", "estado",
        "fecha_salida", "fecha_llegada", "is_active",
        "usuarios_gestores",   # podés filtrar por id del user: ?usuarios_gestores=<id>
    ]
    search_fields = [
        "origen", "destino", "estado",
        "avion__modelo", "usuarios_gestores__username",
    ]
    ordering_fields = [
        "id", "fecha_salida", "fecha_llegada", "estado",
        "precio_base", "is_active", "avion",
    ]
    ordering = ["fecha_salida"]
