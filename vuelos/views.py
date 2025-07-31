from django.shortcuts import render, get_object_or_404
from .models import Vuelo

def vuelo_detail(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    asientos_disponibles = vuelo.avion.asientos.filter(estado="disponible")
    return render(request, 'vuelos/vuelo_detail.html', {
        'vuelo': vuelo,
        'asientos_disponibles': asientos_disponibles
    })

def vuelo_list(request):
    vuelos = Vuelo.objects.all()
    return render(request, 'vuelos/vuelo_list.html', {'vuelos': vuelos})
