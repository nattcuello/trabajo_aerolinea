from django.shortcuts import render, redirect
from .forms import ReservaForm
from .models import Reserva, Asiento

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)

            # Marcar el asiento como reservado
            asiento = reserva.asiento
            if asiento:
                asiento.estado = 'reservado'
                asiento.save()
            
            reserva.save()
            return redirect('reservas:lista_reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservas/reserva_form.html', {'form': form})
    
def lista_reservas(request):
    reservas = Reserva.objects.select_related('pasajero', 'vuelo', 'asiento').all()
    return render(request, 'reservas/reserva_list.html', {'reservas': reservas})
