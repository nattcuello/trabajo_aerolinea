from django import forms
from .models import Reserva, AsientoVuelo
from pasajeros.models import Pasajero



class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['pasajero', 'asiento']  # ajustá según tu modelo

class PasajeroForm(forms.ModelForm):
    pasajero_existente = forms.ModelChoiceField(
        queryset=Pasajero.objects.all(),
        required=False,
        label="Seleccionar pasajero existente"
    )

    fecha_nacimiento = forms.DateField(
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'MM-DD-YYYY'})
    )

    class Meta:
        model = Pasajero
        fields = [
            'pasajero_existente',
            'nombre',
            'tipo_documento',
            'documento',
            'email',
            'telefono',
            'fecha_nacimiento'
        ]

    def save(self, commit=True):
        pasajero_existente = self.cleaned_data.get('pasajero_existente')
        if pasajero_existente:
            return pasajero_existente
        return super().save(commit=commit)
