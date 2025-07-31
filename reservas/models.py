from django.db import models
from pasajeros.models import Pasajero
from vuelos.models import Vuelo

# 👇 Importá Asiento antes de usarlo en Reserva
class Asiento(models.Model):
    avion = models.ForeignKey(Vuelo, on_delete=models.CASCADE, related_name="asientos")  # o Avion si es más correcto
    fila = models.IntegerField()
    columna = models.CharField(max_length=1)
    tipo = models.CharField(max_length=20, choices=[
        ('ventana', 'Ventana'),
        ('pasillo', 'Pasillo'),
        ('medio', 'Medio')
    ])
    estado = models.CharField(max_length=20, choices=[
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado')
    ], default='disponible')

    def __str__(self):
        return f"Asiento {self.fila}{self.columna} - {self.tipo} ({self.estado})"


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, related_name="reservas")
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE, related_name="reservas")
    asiento = models.OneToOneField(Asiento, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reserva de {self.pasajero.nombre} en vuelo {self.vuelo.id} ({self.estado})"

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_reserva']
