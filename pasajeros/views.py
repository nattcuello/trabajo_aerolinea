from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pasajero
from .forms import PasajeroForm
from django.utils.translation import gettext as _


@login_required
def lista_pasajeros(request):
    # Solo admin puede ver la lista completa
    if request.user.perfil and request.user.perfil.rol != 'admin':

        return redirect('home:index')

    pasajeros = Pasajero.objects.all()
    return render(request, 'pasajeros/pasajeros_list.html', {'pasajeros': pasajeros})


@login_required
def detalle_pasajero(request, pasajero_id):
    # Solo admin puede ver detalle de pasajero
    if request.user.perfil and request.user.perfil.rol != 'admin':

        return redirect('home:index')

    pasajero = get_object_or_404(Pasajero, id=pasajero_id)
    return render(request, 'pasajeros/pasajeros_detail.html', {'pasajero': pasajero})


@login_required
def crear_pasajero(request):
    # Solo admin y operador pueden crear pasajeros
    if request.user.perfil and request.user.perfil.rol not in ['admin', 'operador']:
        return redirect('home:index')

    if request.method == 'POST':
        form = PasajeroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pasajeros:listado_pasajeros')
    else:
        form = PasajeroForm()

    return render(request, 'pasajeros/crear_pasajero.html', {'form': form})
