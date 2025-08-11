from django.urls import path
from . import views

app_name = 'reservas'
urlpatterns = [
    path('', views.lista_reservas, name='lista_reservas'),
    path('crear/<int:vuelo_id>/', views.crear_reserva, name='crear_reserva'),
    path('asientos/<int:vuelo_id>/', views.ver_asientos_por_vuelo, name='asientos_vuelo'),  # <-- Agregado
    path('<int:vuelo_id>/seleccionar-asiento/', views.seleccionar_asiento, name='seleccionar_asiento'),
    path('<int:vuelo_id>/reservar-asientos/', views.reservar_asientos, name='reservar_asientos'),
    # urls.py (algo así)
    path('reservas/asientos/<int:vuelo_id>/', views.ver_asientos_por_vuelo, name='ver_asientos_por_vuelo'),
    path('vuelos/<int:vuelo_id>/asientos/', views.ver_asientos_por_vuelo, name='ver_asientos_por_vuelo'),
    path('reservar-asientos/<int:avion_id>/', views.reservar_asientos, name='reservar_asientos'),

 



]
