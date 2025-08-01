from django import forms
from .models import Reserva, Asiento
from pasajeros.models import Pasajero

class ReservaForm(forms.ModelForm):
    pasajero = forms.ModelChoiceField(queryset=Pasajero.objects.all())
    asiento = forms.ModelChoiceField(queryset=Asiento.objects.none())

    class Meta:
        model = Reserva
        fields = ['pasajero', 'asiento']

    def __init__(self, *args, vuelo=None, **kwargs):
        super().__init__(*args, **kwargs)
        if vuelo:
            # Solo asientos disponibles del avión del vuelo
            self.fields['asiento'].queryset = vuelo.avion.asientos.filter(estado='disponible')
