from django.db import models
from django.contrib.auth.models import User
from core.models import SoftDeleteModel

class Avion(SoftDeleteModel):
    modelo = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    filas = models.PositiveIntegerField()
    columnas = models.PositiveIntegerField()


#Muestra el modelo de avión y su capacidad
    def __str__(self):
        return f"{self.modelo} ({self.capacidad} asientos)"

# Meta options for the model
    class Meta:
        verbose_name = "Avión"
        verbose_name_plural = "Aviones"

class Vuelo(SoftDeleteModel):
    ESTADOS = [
        ('programado', 'Programado'),
        ('en_vuelo', 'En Vuelo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]

    avion = models.ForeignKey(Avion, on_delete=models.PROTECT, related_name='vuelos')
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
        verbose_name = "Vuelo"
        verbose_name_plural = "Vuelos"
        ordering = ['fecha_salida']