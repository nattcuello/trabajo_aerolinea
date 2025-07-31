from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('crear/<int:vuelo_id>/', views.crear_reserva, name='crear_reserva'),
]
