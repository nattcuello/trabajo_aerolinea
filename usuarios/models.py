from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    OPCIONES_ROL = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
        ('pasajero', 'Pasajero'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=OPCIONES_ROL)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
