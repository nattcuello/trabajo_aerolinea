from rest_framework.routers import DefaultRouter
from .views_api import AsientoViewSet, AsientoVueloViewSet, ReservaViewSet

router = DefaultRouter()
router.register(r"asientos", AsientoViewSet, basename="asiento")
router.register(r"asientos-vuelo", AsientoVueloViewSet, basename="asiento-vuelo")
router.register(r"reservas", ReservaViewSet, basename="reserva")

urlpatterns = router.urls

