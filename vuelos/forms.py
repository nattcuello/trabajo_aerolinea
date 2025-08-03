from django import forms
from .models import Avion, Vuelo

class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = ['modelo', 'capacidad', 'filas', 'columnas']

class VueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = '__all__'
