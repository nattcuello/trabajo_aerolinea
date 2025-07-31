from django.urls import path
from . import views

app_name = 'vuelos'

urlpatterns = [
    path('', views.vuelo_list, name='vuelo_list'),            # /vuelos/
    path('<int:vuelo_id>/', views.vuelo_detail, name='vuelo_detail'),  # /vuelos/1/
]
