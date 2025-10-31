
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views_api import AvionViewSet, VueloViewSet
# La línea siguiente ya no es necesaria y causaba el error
# from reservas.views import ver_asientos_por_vuelo 

app_name = 'vuelos'

urlpatterns = [
    path('', views.vuelo_list, name='vuelo_list'),
    path('crear/', views.crear_vuelo, name='crear_vuelo'),
    path('crear-avion/', views.crear_avion, name='crear_avion'),
    path('<int:vuelo_id>/', views.vuelo_detail, name='vuelo_detail'),
    path('<int:vuelo_id>/editar/', views.editar_vuelo, name='editar_vuelo'),
    path('<int:vuelo_id>/eliminar/', views.eliminar_vuelo, name='eliminar_vuelo'),
]

router = DefaultRouter()
router.register(r"aviones", AvionViewSet, basename="avion")
router.register(r"vuelos", VueloViewSet, basename="vuelo")

urlpatterns = router.urls