# ejemplo para pasajeros/forms.py
from django import forms
from .models import Pasajero

class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['nombre', 'tipo_documento', 'documento', 'email', 'telefono', 'fecha_nacimiento']
