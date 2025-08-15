from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Avion, Vuelo

class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = ['modelo', 'capacidad', 'filas', 'columnas']
        labels = {
            'modelo': _('Modelo'),
            'capacidad': _('Capacidad'),
            'filas': _('Filas'),
            'columnas': _('Columnas'),
        }

class VueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        exclude = ['usuarios_gestores'] 
        labels = {
            'avion':( _('Avión')),
            'origen': _('Origen'),
            'destino': _('Destino'),
            'fecha_salida': _('Fecha de salida'),
            'fecha_llegada': _('Fecha de llegada'),
            'estado': _('Estado'),
            'precio_base': _('Precio base'),
        }
