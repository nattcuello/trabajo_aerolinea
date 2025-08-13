# reservas/forms.py

from django import forms
from .models import Reserva, AsientoVuelo
from pasajeros.models import Pasajero # Importamos tu modelo Pasajero
from vuelos.models import Vuelo

# Formulario para una sola reserva (tu código original)
class ReservaForm(forms.ModelForm):
    # ... (tu código de ReservaForm aquí)

    class Meta:
        model = Reserva
        fields = ['pasajero', 'asiento'] # Ejemplo de campos

# --- NUEVO FORMULARIO PARA PASAJEROS ---
# Este formulario es el que debe usarse en la vista crear_reserva_multiple

class PasajeroForm(forms.ModelForm):
    # Define el campo con los formatos de fecha permitidos
    fecha_nacimiento = forms.DateField(
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'MM-DD-YYYY'})
    )

    class Meta:
        model = Pasajero
        fields = [
            'nombre',
            'tipo_documento',
            'documento',
            'email',
            'telefono',
            'fecha_nacimiento'
        ]