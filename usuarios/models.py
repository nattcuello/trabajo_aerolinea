# usuarios/models.py
from django.db import models
from django.contrib.auth.models import User
from core.models import SoftDeleteModel 

class PerfilUsuario(SoftDeleteModel):
    ROLES = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
        ('pasajero', 'Pasajero'),
    ]

    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='perfilusuario')
    rol = models.CharField(max_length=20, choices=ROLES, default='pasajero')

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"


# Agregar propiedad al modelo User para acceder a su perfil
def get_perfil(self):
    return getattr(self, 'perfilusuario', None)

User.add_to_class('perfil', property(get_perfil))
