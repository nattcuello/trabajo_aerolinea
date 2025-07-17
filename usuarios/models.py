# usuarios/models.py

from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
        ('pasajero', 'Pasajero'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"
