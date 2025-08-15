from django import forms
from .models import Reserva, AsientoVuelo
from pasajeros.models import Pasajero
from django.utils.translation import gettext as _


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['pasajero', 'asiento']  # Ajustar según tu modelo



class PasajeroForm(forms.ModelForm):
    pasajero_existente = forms.ModelChoiceField(
        queryset=Pasajero.objects.all(),
        required=False,
        label="Seleccionar pasajero existente"
    )

    nombre = forms.CharField(required=False)
    tipo_documento = forms.CharField(required=False)
    documento = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    telefono = forms.CharField(required=False)
    fecha_nacimiento = forms.DateField(
        required=False,
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

    def clean(self):
        cleaned_data = super().clean()
        pasajero_existente = cleaned_data.get('pasajero_existente')

        # Si no se elige pasajero existente, obligamos a completar al menos nombre y documento
        if not pasajero_existente:
            required_fields = ['nombre', 'tipo_documento', 'documento', 'email', 'telefono', 'fecha_nacimiento']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(_(field, 'Este campo es obligatorio si no seleccionaste un pasajero existente.'))

        return cleaned_data

    def save(self, commit=True):
        pasajero_existente = self.cleaned_data.get('pasajero_existente')
        if pasajero_existente:
            return pasajero_existente
        return super().save(commit=commit)