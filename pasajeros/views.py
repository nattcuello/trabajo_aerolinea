from django.shortcuts import render, get_object_or_404
from .models import Pasajero
from .forms import PasajeroForm
from django.shortcuts import redirect


def lista_pasajeros(request):
    pasajeros = Pasajero.objects.all()
    return render(request, 'pasajeros/pasajeros_list.html', {'pasajeros': pasajeros})

def detalle_pasajero(request, pasajero_id):
    pasajero = get_object_or_404(Pasajero, id=pasajero_id)
    return render(request, 'pasajeros/pasajeros_detail.html', {'pasajero': pasajero})

def crear_pasajero(request):
    if request.method == 'POST':
        form = PasajeroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pasajeros:listado_pasajeros')
    else:
        form = PasajeroForm()
    return render(request, 'pasajeros/crear_pasajero.html', {'form': form})
