from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rol']
