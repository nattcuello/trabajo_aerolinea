from django import forms
from .models import Reserva, AsientoVuelo
from pasajeros.models import Pasajero
from django.utils.translation import gettext as _


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['vuelo', 'pasajero', 'asiento']  # Incluimos vuelo

    def __init__(self, *args, vuelo=None, **kwargs):
        super().__init__(*args, **kwargs)
        if vuelo:
            self.fields['vuelo'].initial = vuelo
            self.fields['vuelo'].widget = forms.HiddenInput()


class PasajeroForm(forms.ModelForm):
    pasajero_existente = forms.ModelChoiceField(
        queryset=Pasajero.objects.all(),
        required=False,
        label="Seleccionar pasajero existente"
    )

    nombre = forms.CharField(required=False, label=_("Nombre"))
    tipo_documento = forms.CharField(required=False, label=_("Tipo documento"))
    documento = forms.CharField(required=False, label=_("Documento"))
    email = forms.EmailField(required=False, label=_("Email"))
    telefono = forms.CharField(required=False, label=_("Teléfono"))
    fecha_nacimiento = forms.DateField(
        required=False,
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
        label=_("Fecha de nacimiento"),
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
        cleaned = super().clean()
        pasajero_existente = cleaned.get('pasajero_existente')

        # Si NO se elige pasajero existente, obligamos a completar datos
        if not pasajero_existente:
            required_fields = ['nombre', 'tipo_documento', 'documento', 'email', 'telefono', 'fecha_nacimiento']
            for field in required_fields:
                if not cleaned.get(field):
                    self.add_error(
                        field,
                        _("Este campo es obligatorio si no seleccionaste un pasajero existente.")
                    )
        return cleaned

    def save(self, commit=True):
        pasajero_existente = self.cleaned_data.get('pasajero_existente')
        if pasajero_existente:
            return pasajero_existente
        return super().save(commit=commit)