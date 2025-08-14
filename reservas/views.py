from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from vuelos.models import Vuelo
from .models import Reserva, Asiento, AsientoVuelo
from .forms import ReservaForm, PasajeroForm
from django.db import transaction
from django.http import JsonResponse
from usuarios.decorators import role_required
from pasajeros.models import Pasajero
from collections import defaultdict
from django.forms import formset_factory
from django.core.exceptions import ValidationError


# ----------------------------
# Crear reserva simple
# ----------------------------
@login_required
def crear_reserva(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)

    if request.method == 'POST':
        form = ReservaForm(request.POST, vuelo=vuelo)
        if form.is_valid():
            reserva = form.save(commit=False)
            asiento_vuelo = reserva.asiento  # AsientoVuelo

            try:
                with transaction.atomic():
                    asiento_vuelo_for_update = AsientoVuelo.objects.select_for_update().get(pk=asiento_vuelo.pk)

                    if asiento_vuelo_for_update.estado != 'disponible':
                        form.add_error('asiento', 'Este asiento ya fue reservado por otro pasajero.')
                    else:
                        asiento_vuelo_for_update.estado = 'ocupado'
                        asiento_vuelo_for_update.save()
                        reserva.estado = 'confirmada'
                        reserva.precio_final = vuelo.precio_base
                        reserva.save()
                        # Redirigimos al detalle del vuelo, no a lista general
                        return redirect('vuelos:vuelo_detail', vuelo_id=vuelo.id)
            except Exception as e:
                form.add_error(None, f'Ocurrió un error al crear la reserva: {e}')
    else:
        form = ReservaForm(vuelo=vuelo)

    return render(request, 'reservas/crear_reserva.html', {'form': form, 'vuelo': vuelo})


# ----------------------------
# Lista de reservas (solo admins y operadores)
# ----------------------------
@login_required
@role_required('admin', 'operador')
def lista_reservas(request):
    reservas = Reserva.objects.select_related('vuelo', 'pasajero', 'asiento')
    return render(request, 'reservas/reserva_list.html', {'reservas': reservas})


# ----------------------------
# Crear reservas múltiples
# ----------------------------
@login_required
def crear_reserva_multiple(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    num_pasajeros = int(request.GET.get('num_pasajeros', 1))
    ids_asientos = request.GET.getlist('asientos')  # Ej: ?asientos=44&asientos=45

    if len(ids_asientos) != num_pasajeros:
        return render(request, 'reservas/error.html', {
            'mensaje': 'El número de asientos no coincide con el número de pasajeros.'
        })

    PasajeroFormSet = formset_factory(PasajeroForm, extra=num_pasajeros)

    if request.method == 'POST':
        formset = PasajeroFormSet(request.POST)
        if formset.is_valid():
            asientos_vuelo = AsientoVuelo.objects.select_for_update().filter(id__in=ids_asientos)

            if asientos_vuelo.count() != num_pasajeros:
                return render(request, 'reservas/error.html', {
                    'mensaje': 'Asientos inválidos o incompletos.'
                })

            # Ordenamos los asientos según ids_asientos
            asientos_vuelo_ordered = sorted(
                asientos_vuelo, 
                key=lambda a: ids_asientos.index(str(a.id))
            )

            try:
                with transaction.atomic():
                    for form, asiento_vuelo in zip(formset, asientos_vuelo_ordered):
                        pasajero = form.save()  # Devuelve existente o crea nuevo

                        # Validación: el pasajero no puede tener ya reserva en este vuelo
                        if Reserva.objects.filter(vuelo=vuelo, pasajero=pasajero).exists():
                            raise ValidationError(f'El pasajero {pasajero} ya tiene una reserva para este vuelo.')

                        if asiento_vuelo.estado != 'disponible':
                            raise ValidationError(f'El asiento {asiento_vuelo} ya fue reservado.')

                        reserva = Reserva(
                            vuelo=vuelo,
                            pasajero=pasajero,
                            asiento=asiento_vuelo,
                            estado='confirmada',
                            precio_final=vuelo.precio_base
                        )
                        reserva.save()

                        asiento_vuelo.estado = 'ocupado'
                        asiento_vuelo.save()

                    # Redirigimos al detalle del vuelo, no a lista general
                    return redirect('vuelos:vuelo_detail', vuelo_id=vuelo.id)

            except ValidationError as e:
                return render(request, 'reservas/error.html', {'mensaje': e.messages})
            except Exception as e:
                return render(request, 'reservas/error.html', {'mensaje': str(e)})

    else:
        formset = PasajeroFormSet()

    return render(request, 'reservas/crear_reserva_multiple.html', {
        'vuelo': vuelo,
        'formset': formset,
        'num_pasajeros': num_pasajeros,
        'ids_asientos': ids_asientos,
    })


# ----------------------------
# Seleccionar asiento
# ----------------------------
@login_required
def seleccionar_asiento(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)

    asientos_vuelo = AsientoVuelo.objects.filter(vuelo=vuelo).select_related('asiento').order_by(
        'asiento__fila', 'asiento__columna'
    )

    asientos_por_fila = defaultdict(list)
    for av in asientos_vuelo:
        asiento_info = {
            'id': av.id,
            'fila': av.asiento.fila,
            'columna': av.asiento.columna,
            'tipo': getattr(av.asiento, 'tipo', ''),
            'estado_vuelo': av.estado
        }
        asientos_por_fila[av.asiento.fila].append(asiento_info)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'asientos': list(asientos_vuelo.values())})

    return render(request, 'reservas/seleccionar_asiento.html', {
        'vuelo': vuelo,
        'asientos_por_fila': dict(asientos_por_fila),
    })
