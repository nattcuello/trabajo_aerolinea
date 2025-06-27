# reservas/models.py
from django.db import models
from vuelos.models import Avion


class Asiento(models.Model):
    TIPO_CHOICES = [
        ('ventana', 'Ventana'),
        ('pasillo', 'Pasillo'),
        ('medio', 'Medio'),
    ]

    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('ocupado', 'Ocupado'),
    ]

    #El avión al que pertenece el asiento
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name='asientos')
    #Fila y columna del asiento
    fila = models.PositiveIntegerField()
    columna = models.CharField(max_length=1)  # A, B, C...
    #Tipo de asiento (ventana, pasillo, medio)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    #Estado del asiento (disponible, reservado, ocupado)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='disponible')

    class Meta: #Asegura que no se repitan posiciones en el mismo avión
        unique_together = ('avion', 'fila', 'columna')
        verbose_name = 'Asiento'
        verbose_name_plural = 'Asientos'
        ordering = ['avion', 'fila', 'columna']

    def __str__(self):
        return f"Asiento {self.fila}{self.columna} - {self.avion.modelo}"


# Create your models here.
