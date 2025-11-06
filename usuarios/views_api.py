# usuarios/views_api.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.viewsets import SoftDeleteModelViewSet
from .models import PerfilUsuario
from .serializers import PerfilUsuarioSerializer

class PerfilUsuarioViewSet(SoftDeleteModelViewSet):
    queryset = PerfilUsuario.objects.select_related("user").all()
    serializer_class = PerfilUsuarioSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["rol", "is_active", "user__username", "user__email"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "user__email"]
    ordering_fields = ["id", "user__username", "user__email"]
