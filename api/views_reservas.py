# api/views_reservas.py
from django.utils import timezone

from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from core.viewsets import SoftDeleteModelViewSet

from reservas.models import Asiento, AsientoVuelo, Reserva
from reservas.serializers import (
    AsientoSerializer,
    AsientoVueloSerializer,
    ReservaSerializer,
)

from pasajeros.models import Pasajero
from vuelos.models import Vuelo


# ---------- Asiento ----------
class AsientoViewSet(SoftDeleteModelViewSet):
    queryset = Asiento.objects.all()
    serializer_class = AsientoSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["avion", "tipo", "estado", "is_active"]
    search_fields = ["fila", "columna", "tipo", "estado"]
    ordering_fields = ["id", "fila", "columna", "tipo", "estado", "is_active"]
    ordering = ["id"]


# ---------- AsientoVuelo ----------
class AsientoVueloViewSet(SoftDeleteModelViewSet):
    queryset = AsientoVuelo.objects.all()
    serializer_class = AsientoVueloSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["vuelo", "asiento", "estado", "is_active"]
    search_fields = ["estado", "vuelo__id", "asiento__fila", "asiento__columna"]
    ordering_fields = ["id", "estado", "is_active", "vuelo", "asiento"]
    ordering = ["id"]


# ---------- Reserva ----------
class ReservaViewSet(SoftDeleteModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        "pasajero", "vuelo", "asiento", "estado", "is_active",
        # extras útiles por fechas/precio
        "fecha_reserva", "precio_final",
    ]
    search_fields = [
        "estado",
        "pasajero__nombre", "pasajero__documento",
        "vuelo__id",
        "asiento__asiento__fila", "asiento__asiento__columna",  # Reserva.asiento -> AsientoVuelo.asiento
    ]
    ordering_fields = [
        "id", "precio_final", "fecha_reserva", "estado", "is_active", "pasajero", "vuelo", "asiento"
    ]
    ordering = ["-fecha_reserva"]

    # ============ REPORTES ============

    @action(detail=False, methods=["get"], url_path="pasajeros-por-vuelo")
    def pasajeros_por_vuelo(self, request):
        """
        GET /api/reservas/pasajeros-por-vuelo/?vuelo=<id>
        Devuelve pasajeros con reserva activa para ese vuelo.
        """
        vuelo_id = request.query_params.get("vuelo")
        if not vuelo_id:
            return Response({"detail": "Parámetro 'vuelo' es requerido."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            vuelo = Vuelo._base_manager.get(pk=vuelo_id)
        except Vuelo.DoesNotExist:
            return Response({"detail": "No Vuelo matches the given query."},
                            status=status.HTTP_404_NOT_FOUND)

        reservas_qs = (
            Reserva._base_manager
            .filter(is_active=True, vuelo=vuelo)  # ← Reserva tiene ForeignKey directo a Vuelo
            .select_related("pasajero", "asiento", "asiento__asiento")  # asiento: AsientoVuelo; asiento.asiento: Asiento
        )

        data = []
        for r in reservas_qs:
            pasajero = r.pasajero
            av = r.asiento                     # AsientoVuelo
            asiento = av.asiento if av else None  # Asiento

            data.append({
                "reserva_id": r.id,
                "pasajero": {
                    "id": getattr(pasajero, "id", None),
                    "nombre": getattr(pasajero, "nombre", None),
                    "documento": getattr(pasajero, "documento", None),
                    "email": getattr(pasajero, "email", None),
                },
                "asiento": {
                    "id": getattr(asiento, "id", None),
                    "fila": getattr(asiento, "fila", None),
                    "columna": getattr(asiento, "columna", None),
                    "tipo": getattr(asiento, "tipo", None),
                },
            })

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="reservas-activas-por-pasajero")
    def reservas_activas_por_pasajero(self, request):
        """
        GET /api/reservas/reservas-activas-por-pasajero/?pasajero=<id>
        Devuelve reservas activas del pasajero.
        """
        pasajero_id = request.query_params.get("pasajero")
        if not pasajero_id:
            return Response({"detail": "Parámetro 'pasajero' es requerido."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            pasajero = Pasajero._base_manager.get(pk=pasajero_id)
        except Pasajero.DoesNotExist:
            return Response({"detail": "No Pasajero matches the given query."},
                            status=status.HTTP_404_NOT_FOUND)

        reservas_qs = (
            Reserva._base_manager
            .filter(is_active=True, pasajero=pasajero)
            .select_related("vuelo", "asiento", "asiento__asiento")
        )
        return Response(ReservaSerializer(reservas_qs, many=True).data, status=status.HTTP_200_OK)

    # ============ BOLETO ============

    @action(detail=True, methods=["post"], url_path="generar-boleto")
    def generar_boleto(self, request, pk=None):
        """
        POST /api/reservas/{id}/generar-boleto/
        Devuelve un "boleto" (JSON) con datos de reserva/pasajero/vuelo/asiento.
        """
        try:
            r = (Reserva._base_manager
                 .select_related("pasajero", "vuelo", "asiento", "asiento__asiento")
                 .get(pk=pk))
        except Reserva.DoesNotExist:
            return Response({"detail": "No Reserva matches the given query."},
                            status=status.HTTP_404_NOT_FOUND)

        pasajero = r.pasajero
        vuelo = r.vuelo
        av = r.asiento                     # AsientoVuelo
        asiento = av.asiento if av else None

        boleto = {
            "boleto_id": f"R-{r.id}",
            "emitido_en": timezone.now().isoformat(timespec="seconds"),
            "reserva": {
                "id": r.id,
                "precio_final": r.precio_final,
                "estado": r.estado,
                "is_active": r.is_active,
            },
            "pasajero": {
                "id": getattr(pasajero, "id", None),
                "nombre": getattr(pasajero, "nombre", None),
                "documento": getattr(pasajero, "documento", None),
                "email": getattr(pasajero, "email", None),
                "telefono": getattr(pasajero, "telefono", None),
            },
            "vuelo": {
                "id": getattr(vuelo, "id", None),
                "codigo": getattr(vuelo, "codigo", None),      # ajustá si tu modelo usa otro campo
                "origen": getattr(vuelo, "origen", None),
                "destino": getattr(vuelo, "destino", None),
                "salida": getattr(vuelo, "fecha_salida", None) or getattr(vuelo, "fecha_hora_salida", None),
                "llegada": getattr(vuelo, "fecha_llegada", None) or getattr(vuelo, "fecha_hora_llegada", None),
            },
            "asiento": {
                "id": getattr(asiento, "id", None),
                "fila": getattr(asiento, "fila", None),
                "columna": getattr(asiento, "columna", None),
                "tipo": getattr(asiento, "tipo", None),
            },
        }
        return Response(boleto, status=status.HTTP_200_OK)
