from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.lista_reservas, name='lista_reservas'),  # 👈 esta línea nueva
]
