# reservas/urls.py corregido
from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('lista/', views.lista_reservas, name='lista_reservas'),
    path('<int:vuelo_id>/seleccionar-asiento/', views.seleccionar_asiento, name='seleccionar_asiento'),
    path('<int:vuelo_id>/reservar-asientos/', views.crear_reserva_multiple, name='reservar_asientos'),
    path('<int:vuelo_id>/crear-reservas/', views.crear_reserva_multiple, name='crear_reserva_multiple'),
    path('<int:vuelo_id>/crear-reserva/', views.crear_reserva, name='crear_reserva'),
]
