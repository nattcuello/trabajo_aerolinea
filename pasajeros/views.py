from django.shortcuts import render, get_object_or_404
from .models import Pasajero

def lista_pasajeros(request):
    pasajeros = Pasajero.objects.all()
    return render(request, 'pasajeros/pasajeros_list.html', {'pasajeros': pasajeros})

def detalle_pasajero(request, pasajero_id):
    pasajero = get_object_or_404(Pasajero, id=pasajero_id)
    return render(request, 'pasajeros/pasajeros_detail.html', {'pasajero': pasajero})
