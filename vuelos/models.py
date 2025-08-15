from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Avion(models.Model):
    modelo = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    filas = models.PositiveIntegerField()
    columnas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.modelo} ({self.capacidad} asientos)"

    class Meta:
        verbose_name = _("Avión")
        verbose_name_plural = _("Aviones")


class Vuelo(models.Model):
    ESTADOS = [
        ('programado', _('Programado')),
        ('en_vuelo', _('En Vuelo')),
        ('finalizado', _('Finalizado')),
        ('cancelado', _('Cancelado')),
    ]

    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name='vuelos')
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='programado')
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    usuarios_gestores = models.ManyToManyField(User, related_name='vuelos_gestionados')

    def __str__(self):
        return f"{self.origen} → {self.destino} | {self.fecha_salida.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = _("Vuelo")
        verbose_name_plural = _("Vuelos")
        ordering = ['fecha_salida']
