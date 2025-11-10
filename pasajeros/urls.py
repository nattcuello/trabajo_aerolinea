from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from api.views_pasajeros import PasajeroViewSet

urlpatterns = [
    path('', views.lista_pasajeros, name='listado_pasajeros'),
    path('<int:pasajero_id>/', views.detalle_pasajero, name='detalle_pasajero'),
    path('crear/', views.crear_pasajero, name='crear_pasajero'),
 

]

router = DefaultRouter()
router.register(r"pasajeros", PasajeroViewSet, basename="pasajero")

urlpatterns = router.urls
