from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.lista_reservas, name='lista_reservas'),
    path('crear/<int:vuelo_id>/', views.crear_reserva, name='crear_reserva'),
    path('asientos/<int:vuelo_id>/', views.ver_asientos_por_vuelo, name='asientos_vuelo'),  # <-- Agregado
]
