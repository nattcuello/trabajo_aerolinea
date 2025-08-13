from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Vuelo, Avion
from .forms import VueloForm, AvionForm
from reservas.services import AsientoService  # Servicio para generar asientos
from django.contrib import messages


@login_required
def vuelo_list(request):
    if request.user.perfil and request.user.perfil.rol == 'admin':

        vuelos = Vuelo.objects.all()
    elif request.user.perfil.rol == 'operador':
        vuelos = Vuelo.objects.filter(usuarios_gestores=request.user)
    else:
        # El pasajero no debería ver esta vista
        return redirect('home:index')

    return render(request, 'vuelos/vuelo_list.html', {'vuelos': vuelos})



@login_required
def vuelo_detail(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    asientos_disponibles = vuelo.avion.asientos.filter(estado="disponible")
    reservas_confirmadas = vuelo.reservas.filter(estado="confirmada").select_related('asiento', 'pasajero')
    
    return render(request, 'vuelos/vuelo_detail.html', {
        'vuelo': vuelo,
        'asientos_disponibles': asientos_disponibles,
        'reservas_confirmadas': reservas_confirmadas
    })




@login_required
def crear_vuelo(request):
    if request.method == 'POST':
        form = VueloForm(request.POST)
        if form.is_valid():
            vuelo = form.save()
            vuelo.usuarios_gestores.add(request.user)  # Asigna al usuario actual
            vuelo.save()
            return redirect('vuelos:vuelo_list')
    else:
        form = VueloForm()
    return render(request, 'vuelos/crear_vuelo.html', {'form': form})


@login_required
def crear_avion(request):
    if request.method == 'POST':
        form = AvionForm(request.POST)
        if form.is_valid():
            avion = form.save()
            AsientoService.generar_asientos_para_avion(avion)  # Generar asientos
            return redirect('vuelos:vuelo_list')
    else:
        form = AvionForm()
    return render(request, 'vuelos/crear_avion.html', {'form': form})

@login_required
def editar_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    if request.method == 'POST':
        form = VueloForm(request.POST, instance=vuelo)
        if form.is_valid():
            form.save()
            messages.success(request, "Vuelo actualizado exitosamente.")
            return redirect('vuelos:vuelo_list')
    else:
        form = VueloForm(instance=vuelo)
    return render(request, 'vuelos/editar_vuelo.html', {'form': form, 'vuelo': vuelo})

@login_required
def eliminar_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    if request.method == 'POST':
        vuelo.delete()
        messages.success(request, "Vuelo eliminado exitosamente.") 
        return redirect('vuelos:vuelo_list')
    return render(request, 'vuelos/confirmar_eliminar_vuelo.html', {'vuelo': vuelo})