from django.urls import path
from . import views

urlpatterns = [
    path('asientos/<int:avion_id>/', views.listado_asientos_por_avion, name='listado_asientos'),
]