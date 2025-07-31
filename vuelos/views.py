# vuelos/views.py
from django.shortcuts import render, get_object_or_404
from .models import Vuelo

def vuelo_list(request):
    vuelos = Vuelo.objects.select_related('avion').all()
    return render(request, 'vuelos/vuelo_list.html', {'vuelos': vuelos})

def vuelo_detail(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    return render(request, 'vuelos/vuelo_detail.html', {'vuelo': vuelo})
