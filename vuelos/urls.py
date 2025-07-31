from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_vuelos, name='lista_vuelos'),
    path('<int:vuelo_id>/', views.detalle_vuelo, name='detalle_vuelo'),
]
