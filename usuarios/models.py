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

# Propiedad para acceder al perfil desde el usuario: user.perfil
def get_perfil(self):
    # Retorna el perfil si existe, sino None (o podrías usar get_or_create si querés)
    try:
        return self.perfilusuario
    except PerfilUsuario.DoesNotExist:
        return None

User.add_to_class('perfil', property(get_perfil))
