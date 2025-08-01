from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pasajeros, name='listado_pasajeros'),
    path('<int:pasajero_id>/', views.detalle_pasajero, name='detalle_pasajero'),
]
