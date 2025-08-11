from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from vuelos.models import Vuelo
from .models import Reserva, Asiento
from .forms import ReservaForm
from django.db import transaction
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from vuelos.models import Avion

@login_required
def crear_reserva(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)

    if request.method == 'POST':
        form = ReservaForm(request.POST, vuelo=vuelo)
        if form.is_valid():
            reserva = form.save(commit=False)
            asiento = reserva.asiento

            try:
                with transaction.atomic():
                    asiento = Asiento.objects.select_for_update().get(pk=asiento.pk)
                    if asiento.estado != 'disponible':
                        form.add_error('asiento', 'Este asiento ya fue reservado por otro pasajero.')
                    else:
                        asiento.estado = 'ocupado'
                        asiento.save()
                        reserva.estado = 'confirmada'
                        reserva.precio_final = vuelo.precio_base
                        reserva.save()
                        return redirect('vuelos:vuelo_detail', vuelo_id=vuelo.id)
            except Exception as e:
                form.add_error(None, 'Ocurrió un error al crear la reserva: ' + str(e))
    else:
        form = ReservaForm(vuelo=vuelo)

    return render(request, 'reservas/crear_reserva.html', {'form': form, 'vuelo': vuelo})



@login_required
def lista_reservas(request):
    rol = request.user.perfil.rol

    if rol == 'admin' or rol == 'operador':
        reservas = Reserva.objects.select_related('vuelo', 'pasajero', 'asiento')
    else:
        # Asumiendo que Pasajero tiene un campo usuario con FK a User
        reservas = Reserva.objects.filter(pasajero__usuario=request.user).select_related('vuelo', 'asiento')

    return render(request, 'reservas/reserva_list.html', {'reservas': reservas})


@login_required
def ver_asientos_por_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    asientos = vuelo.avion.asientos.all().order_by('fila', 'columna')

    asientos_por_fila = {}
    for asiento in asientos:
        fila = asiento.fila
        if fila not in asientos_por_fila:
            asientos_por_fila[fila] = []
        asientos_por_fila[fila].append(asiento)

    return render(request, 'reservas/asientos_por_vuelo.html', {
        'vuelo': vuelo,
        'asientos_por_fila': asientos_por_fila
    })

def seleccionar_asiento(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    asientos = Asiento.objects.filter(vuelo=vuelo).order_by('numero')
    return render(request, 'reservas/seleccionar_asiento.html', {
        'vuelo': vuelo,
        'asientos': asientos
    })

@csrf_exempt  # solo para testeo, idealmente usar CSRF token en el fetch
def reservar_asientos(request, avion_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ids_asientos = data.get("asientos", [])

            # Cambiar estado solo si está disponible
            updated_count = Asiento.objects.filter(id__in=ids_asientos, avion_id=avion_id, estado="disponible").update(estado="ocupado")

            if updated_count == len(ids_asientos):
                return JsonResponse({"status": "ok"})
            else:
                return JsonResponse({"status": "error", "message": "Algunos asientos no estaban disponibles."}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)


@login_required
def ver_asientos_por_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    # Todos los asientos del avión de este vuelo
    asientos = vuelo.avion.asientos.all().order_by('fila', 'columna')

    # IDs de asientos reservados en este vuelo
    asientos_reservados_ids = Reserva.objects.filter(
        vuelo=vuelo,
        estado='confirmada'
    ).values_list('asiento_id', flat=True)

    # Construir dict por fila con estado dinámico
    asientos_por_fila = {}

    for asiento in asientos:
        estado_vuelo = 'ocupado' if asiento.id in asientos_reservados_ids else 'disponible'

        if asiento.fila not in asientos_por_fila:
            asientos_por_fila[asiento.fila] = []

        asientos_por_fila[asiento.fila].append({
            'id': asiento.id,
            'fila': asiento.fila,
            'columna': asiento.columna,
            'tipo': asiento.tipo,
            'estado_vuelo': estado_vuelo
        })

    return render(request, 'reservas/asientos_por_vuelo.html', {
        'vuelo': vuelo,
        'asientos_por_fila': asientos_por_fila
    })