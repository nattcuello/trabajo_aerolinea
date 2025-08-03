from django.urls import path
from . import views

app_name = 'vuelos'

urlpatterns = [
    path('', views.vuelo_list, name='vuelo_list'),            # /vuelos/
    path('crear/', views.crear_vuelo, name='crear_vuelo'),
    path('crear-avion/', views.crear_avion, name='crear_avion'),
    path('<int:vuelo_id>/', views.vuelo_detail, name='vuelo_detail'), 

]

