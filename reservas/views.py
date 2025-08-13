from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from vuelos.models import Vuelo
from .models import Reserva, Asiento, AsientoVuelo
from .forms import ReservaForm
from django.db import transaction
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from usuarios.decorators import role_required
from django.forms import formset_factory
from .forms import ReservaForm, PasajeroForm
from django.forms import modelformset_factory
from pasajeros.models import Pasajero


# La vista `crear_reserva` se mantiene, pero es un método alternativo a `reservar_asientos`
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
                        return redirect('vuelos:vuelo_detail', vuelo_id=vuelo.id)
            except Exception as e:
                form.add_error(None, f'Ocurrió un error al crear la reserva: {e}')
    else:
        form = ReservaForm(vuelo=vuelo)

    return render(request, 'reservas/crear_reserva.html', {'form': form, 'vuelo': vuelo})


@login_required
@role_required('admin', 'operador')
def lista_reservas(request):
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol if perfil else 'sin rol'
    print(f"Usuario: {request.user}, rol: {rol}")
    reservas = Reserva.objects.select_related('vuelo', 'pasajero', 'asiento')
    return render(request, 'reservas/reserva_list.html', {'reservas': reservas})


@login_required
def seleccionar_asiento(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    # Usar `AsientoVuelo` es clave para evitar duplicados
    asientos_vuelo = AsientoVuelo.objects.filter(vuelo=vuelo).order_by('asiento__fila', 'asiento__columna')

    asientos_por_fila = {}

    for asiento_vuelo in asientos_vuelo:
        asiento = asiento_vuelo.asiento
        estado_vuelo = asiento_vuelo.estado

        asientos_por_fila.setdefault(asiento.fila, []).append({
            'id': asiento_vuelo.id,
            'fila': asiento.fila,
            'columna': asiento.columna,
            'tipo': asiento.tipo,
            'estado_vuelo': estado_vuelo,
        })

    return render(request, 'reservas/seleccionar_asiento.html', {
        'vuelo': vuelo,
        'asientos_por_fila': asientos_por_fila
    })


@login_required
@role_required('admin', 'operador')
def ver_asientos_por_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    asientos_vuelo = AsientoVuelo.objects.filter(vuelo=vuelo).order_by('asiento__fila', 'asiento__columna')

    asientos_por_fila = {}

    for asiento_vuelo in asientos_vuelo:
        asiento = asiento_vuelo.asiento
        estado_vuelo = asiento_vuelo.estado

        asientos_por_fila.setdefault(asiento.fila, []).append({
            'id': asiento_vuelo.id,
            'fila': asiento.fila,
            'columna': asiento.columna,
            'tipo': asiento.tipo,
            'estado_vuelo': estado_vuelo,
        })

    return render(request, 'reservas/asientos_por_vuelo.html', {
        'vuelo': vuelo,
        'asientos_por_fila': asientos_por_fila
    })



@csrf_exempt
@login_required
def reservar_asientos(request, vuelo_id):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        ids_asientos = data.get("asientos", [])
        if not ids_asientos:
            return JsonResponse({"status": "error", "message": "No se enviaron IDs de asientos"}, status=400)

        vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
        pasajero = request.user.perfil # ¡Revisa esta línea!

        with transaction.atomic():
            asientos_vuelo = (
                AsientoVuelo.objects.select_for_update()
                .filter(id__in=ids_asientos, vuelo=vuelo)
            )

            for asiento_vuelo in asientos_vuelo:
                if asiento_vuelo.estado != "disponible":
                    return JsonResponse(
                        {"status": "error", "message": f"Asiento {asiento_vuelo.id} no está disponible."},
                        status=400
                    )
            
            # Crear las reservas y marcar los asientos como ocupados
            for asiento_vuelo in asientos_vuelo:
                # El error podría estar aquí. Asegúrate de que 'pasajero' no sea None.
                Reserva.objects.create(
                    pasajero=pasajero,  
                    vuelo=vuelo,
                    asiento=asiento_vuelo,
                    estado="confirmada",
                    precio_final=vuelo.precio_base
                )
                asiento_vuelo.estado = "ocupado"
                asiento_vuelo.save()

        return JsonResponse({"status": "ok", "message": "Asientos reservados con éxito"})

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    


@login_required
def lista_reservas(request):
    reservas = Reserva.objects.all().select_related('vuelo', 'pasajero')
    return render(request, 'reservas/reserva_list.html', {'reservas': reservas})

@login_required
def crear_reserva_multiple(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    num_pasajeros = int(request.GET.get('num_pasajeros', 1))
    # Recibimos los asientos como lista de strings desde GET o POST, según tu implementación
    ids_asientos = request.GET.getlist('asientos')  # Ejemplo: ?asientos=1&asientos=2

    if len(ids_asientos) != num_pasajeros:
        # Manejar inconsistencia, por ejemplo:
        return render(request, 'reservas/error.html', {
            'mensaje': 'El número de asientos no coincide con el número de pasajeros.'
        })

    PasajeroFormSet = modelformset_factory(Pasajero, form=PasajeroForm, extra=num_pasajeros)

    if request.method == 'POST':
        formset = PasajeroFormSet(request.POST)
        if formset.is_valid():
            asientos_vuelo = AsientoVuelo.objects.filter(id__in=ids_asientos)
            if asientos_vuelo.count() != num_pasajeros:
                return render(request, 'reservas/error.html', {
                    'mensaje': 'Asientos inválidos o incompletos.'
                })

            # Ordenar asientos para que coincida con el orden de ids_asientos
            asientos_vuelo_ordered = sorted(asientos_vuelo, key=lambda a: ids_asientos.index(str(a.id)))

            for form, asiento_vuelo in zip(formset, asientos_vuelo_ordered):
                pasajero = form.save()
                reserva = Reserva.objects.create(
                    vuelo=vuelo,
                    pasajero=pasajero,
                    asiento=asiento_vuelo,
                    estado='confirmada',
                    precio_final=vuelo.precio_base
                )
                asiento_vuelo.estado='ocupado'
                asiento_vuelo.save()
            return redirect('reservas:lista_reservas')
    else:
        formset = PasajeroFormSet(queryset=Pasajero.objects.none())

    return render(request, 'reservas/crear_reserva_multiple.html', {
        'vuelo': vuelo,
        'formset': formset,
        'num_pasajeros': num_pasajeros,
        'ids_asientos': ids_asientos,
    })