from django.shortcuts import render, redirect, get_object_or_404
from vuelos.models import Vuelo
from .models import Reserva, Asiento
from .forms import ReservaForm
from django.db import transaction

def crear_reserva(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)

    if request.method == 'POST':
        form = ReservaForm(request.POST, vuelo=vuelo)
        if form.is_valid():
            pasajero = form.cleaned_data['pasajero']
            asiento = form.cleaned_data['asiento']

            # Validar que pasajero no tenga reserva en ese vuelo
            if Reserva.objects.filter(vuelo=vuelo, pasajero=pasajero).exists():
                form.add_error('pasajero', 'Este pasajero ya tiene una reserva para este vuelo.')
            else:
                try:
                    with transaction.atomic():
                        # Crear reserva
                        reserva = Reserva.objects.create(
                            vuelo=vuelo,
                            pasajero=pasajero,
                            asiento=asiento,
                            precio_final=vuelo.precio_base,
                            estado='confirmada'
                        )
                        # Cambiar estado asiento a ocupado
                        asiento.estado = 'ocupado'
                        asiento.save()
                    return redirect('vuelos:vuelo_detail', vuelo_id=vuelo.id)
                except Exception as e:
                    form.add_error(None, 'Ocurrió un error al crear la reserva: ' + str(e))
    else:
        form = ReservaForm(vuelo=vuelo)

    return render(request, 'reservas/crear_reserva.html', {'form': form, 'vuelo': vuelo})

def lista_reservas(request):
    reservas = Reserva.objects.select_related('vuelo', 'pasajero', 'asiento')
    return render(request, 'reservas/lista_reservas.html', {'reservas': reservas})
