from rest_framework.routers import DefaultRouter
from api.views_reservas import AsientoViewSet, AsientoVueloViewSet, ReservaViewSet

app_name = "reservas"

router = DefaultRouter()
router.register(r"asientos", AsientoViewSet, basename="asiento")
router.register(r"asientos-vuelo", AsientoVueloViewSet, basename="asiento-vuelo")
router.register(r"reservas", ReservaViewSet, basename="reserva")

urlpatterns = router.urls

