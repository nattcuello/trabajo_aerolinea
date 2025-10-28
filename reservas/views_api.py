from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Asiento, AsientoVuelo, Reserva
from .serializers import AsientoSerializer, AsientoVueloSerializer, ReservaSerializer, ReservaCreateSerializer
from pasajeros.serializers import PasajeroSerializer
from trabajo_aerolineas.permissions import IsAdminOrOperadorOrReadOnly

class AsientoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Asiento.objects.select_related("avion")
    serializer_class = AsientoSerializer

class AsientoVueloViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AsientoVuelo.objects.select_related("vuelo","asiento","asiento__avion")
    serializer_class = AsientoVueloSerializer
    def get_queryset(self):
        v = self.request.query_params.get("vuelo")
        return super().get_queryset().filter(vuelo_id=v) if v else super().get_queryset()

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.select_related("vuelo","pasajero","asiento","asiento__asiento","asiento__vuelo")
    serializer_class = ReservaSerializer
    permission_classes = [IsAdminOrOperadorOrReadOnly]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        ser = ReservaCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        reserva = ser.save()
        return Response(ReservaSerializer(reserva).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="por-vuelo")
    def por_vuelo(self, request):
        vuelo_id = request.query_params.get("vuelo")
        if not vuelo_id: return Response({"detail":"Falta 'vuelo'."}, status=400)
        rs = self.get_queryset().filter(vuelo_id=vuelo_id).select_related("pasajero")
        pasajeros = [r.pasajero for r in rs]
        return Response(PasajeroSerializer(pasajeros, many=True).data)

    @action(detail=False, methods=["get"], url_path="activas-por-pasajero")
    def activas_por_pasajero(self, request):
        pid = request.query_params.get("pasajero")
        if not pid: return Response({"detail":"Falta 'pasajero'."}, status=400)
        rs = self.get_queryset().filter(pasajero_id=pid, estado__in=["pendiente","confirmada"])
        return Response(ReservaSerializer(rs, many=True).data)

