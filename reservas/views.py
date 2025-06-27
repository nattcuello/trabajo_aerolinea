from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Asiento
from vuelos.models import Avion


def listado_asientos_por_avion(request, avion_id):
    avion = get_object_or_404(Avion, id=avion_id)
    asientos = Asiento.objects.filter(avion=avion).order_by('fila', 'columna')

    # Agrupamos los asientos por fila
    asientos_por_fila = {}
    for asiento in asientos:
        fila = asiento.fila
        if fila not in asientos_por_fila:
            asientos_por_fila[fila] = []
        asientos_por_fila[fila].append(asiento)

    context = {
        'avion': avion,
        'asientos_por_fila': asientos_por_fila,
    }

    return render(request, 'reservas/listado_asientos.html', context)