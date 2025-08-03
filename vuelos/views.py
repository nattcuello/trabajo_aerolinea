from django.shortcuts import render, get_object_or_404, redirect
from .models import Vuelo, Avion
from .forms import VueloForm, AvionForm

from reservas.services import AsientoService  # Importamos el servicio que genera asientos


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


def crear_vuelo(request):
    if request.method == 'POST':
        form = VueloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vuelos:vuelo_list')
    else:
        form = VueloForm()
    return render(request, 'vuelos/crear_vuelo.html', {'form': form})


def crear_avion(request):
    if request.method == 'POST':
        form = AvionForm(request.POST)
        if form.is_valid():
            avion = form.save()  # Guardamos el avión primero
            # Generamos los asientos automáticamente para este avión
            AsientoService.generar_asientos_para_avion(avion)
            return redirect('vuelos:vuelo_list')  # Redirigimos a lista de vuelos o donde quieras
    else:
        form = AvionForm()
    return render(request, 'vuelos/crear_avion.html', {'form': form})
