from django.shortcuts import render, get_object_or_404
from .models import Vuelo

def lista_vuelos(request):
    vuelos = Vuelo.objects.all()
    return render(request, 'vuelos/lista_vuelos.html', {'vuelos': vuelos})

def detalle_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    return render(request, 'vuelos/detalle_vuelo.html', {'vuelo': vuelo})
