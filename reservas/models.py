from django.db import models
from django.core.exceptions import ValidationError
from pasajeros.models import Pasajero
from vuelos.models import Vuelo, Avion


class Asiento(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name="asientos")
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
    asiento = models.OneToOneField(Asiento, on_delete=models.PROTECT)  # PROTECT para evitar borrar asiento reservado
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def clean(self):
        if not self.vuelo or not self.pasajero:
            return  # Evita validación si vuelo o pasajero aún no están definidos

        if Reserva.objects.filter(vuelo=self.vuelo, pasajero=self.pasajero).exclude(pk=self.pk).exists():
            raise ValidationError('El pasajero ya tiene una reserva para este vuelo.')

    def save(self, *args, **kwargs):
        self.clean()
        if not self.precio_final:
            self.precio_final = self.vuelo.precio_base
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de {self.pasajero.nombre} en vuelo {self.vuelo.id} ({self.estado})"

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_reserva']
