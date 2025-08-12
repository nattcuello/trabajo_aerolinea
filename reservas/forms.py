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
        self.vuelo = vuelo
        if vuelo:
            self.fields['asiento'].queryset = vuelo.avion.asientos.filter(estado='disponible')

    def clean(self):
        # Asignar vuelo antes de validar
        if self.vuelo:
            self.instance.vuelo = self.vuelo
        return super().clean()

    def save(self, commit=True):
        reserva = super().save(commit=False)
        if self.vuelo:
            reserva.vuelo = self.vuelo
        if commit:
            reserva.save()
        return reserva
