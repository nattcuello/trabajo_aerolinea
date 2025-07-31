from django import forms
from .models import Reserva, Asiento
from vuelos.models import Vuelo
from pasajeros.models import Pasajero

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['pasajero', 'vuelo', 'asiento', 'precio_final']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Solo mostrar asientos disponibles
        self.fields['asiento'].queryset = Asiento.objects.filter(estado='disponible')
