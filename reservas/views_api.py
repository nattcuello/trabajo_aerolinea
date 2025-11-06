# reservas/views_api.py
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import secrets, string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.viewsets import SoftDeleteModelViewSet
from vuelos.models import Vuelo 
from .models import Asiento, AsientoVuelo, Reserva, Boleto
from .serializers import AsientoSerializer, AsientoVueloSerializer, ReservaSerializer, BoletoSerializer

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

    # --- REPORTE 1: Pasajeros por vuelo ---
    @action(detail=False, methods=["get"], url_path="pasajeros-por-vuelo")
    def pasajeros_por_vuelo(self, request):
        """
        GET /api/reservas/pasajeros-por-vuelo/?vuelo=<id>
        Devuelve pasajeros (vía reservas activas) para un vuelo dado.
        """
        vuelo_id = request.query_params.get("vuelo")
        if not vuelo_id:
            return Response({"detail": "Falta parámetro ?vuelo=<id>."}, status=400)

        vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
        reservas = (
            Reserva.objects
            .filter(vuelo=vuelo, is_active=True)
            .select_related("pasajero")
        )

        data = [
            {
                "reserva_id": r.id,
                "pasajero_id": r.pasajero_id,
                "pasajero_nombre": getattr(r.pasajero, "nombre", ""),
                "estado_reserva": r.estado,
            }
            for r in reservas
        ]
        return Response({"vuelo": vuelo.id, "pasajeros": data}, status=200)

    # --- REPORTE 2: Reservas activas por pasajero ---
    @action(detail=False, methods=["get"], url_path="reservas-activas-por-pasajero")
    def reservas_activas_por_pasajero(self, request):
        """
        GET /api/reservas/reservas-activas-por-pasajero/?pasajero=<id>
        Lista las reservas activas del pasajero.
        """
        pasajero_id = request.query_params.get("pasajero")
        if not pasajero_id:
            return Response({"detail": "Falta parámetro ?pasajero=<id>."}, status=400)

        qs = (
            Reserva.objects
            .filter(pasajero_id=pasajero_id, is_active=True)
            .select_related("vuelo")
        )
        return Response(
            [{"reserva_id": r.id, "vuelo_id": r.vuelo_id, "estado": r.estado} for r in qs],
            status=200
        )

    # --- ACCIÓN: Generar boleto para una reserva confirmada ---
    @action(detail=True, methods=["post"], url_path="generar-boleto")
    def generar_boleto(self, request, pk=None):
        """
        POST /api/reservas/{id}/generar-boleto/
        - Requiere que la reserva esté 'confirmada'
        - Crea un Boleto único (si no existe)
        - Devuelve el código -> {"codigo": "XXXX..."}
        """
        reserva = self.get_object()

        if reserva.estado != "confirmada":
            return Response({"detail": "La reserva debe estar confirmada."}, status=400)

        # Si ya existe, lo devolvemos (idempotencia)
        if hasattr(reserva, "boleto"):
            serializer = BoletoSerializer(reserva.boleto)
            return Response(serializer.data, status=200)

        boleto = Boleto.objects.create(reserva=reserva, codigo=_gen_codigo())
        serializer = BoletoSerializer(boleto)
        return Response(serializer.data, status=201)

def _gen_codigo(n=10):
    alfabeto = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alfabeto) for _ in range(n))


