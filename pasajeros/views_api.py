""" # pasajeros/views_api.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.viewsets import SoftDeleteModelViewSet
from .models import Pasajero
from .serializers import PasajeroSerializer

class PasajeroViewSet(SoftDeleteModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["tipo_documento", "documento", "email", "is_active"]
    search_fields = ["nombre", "documento", "email", "telefono"]
    ordering_fields = ["nombre", "documento", "email", "id"]
 """