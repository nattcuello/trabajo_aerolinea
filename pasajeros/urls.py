# pasajeros/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # De momento puede estar vacío o tener alguna vista de prueba
    path('', views.home, name='home_pasajeros'),
]
