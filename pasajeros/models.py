from django.db import models

class Pasajero(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('DNI', 'DNI'),
        ('PAS', 'Pasaporte'),
        ('LC', 'Libreta Cívica'),
        ('LE', 'Libreta de Enrolamiento'),
        ('OTRO', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES)
    documento = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()

    class Meta:
        verbose_name = 'Pasajero'
        verbose_name_plural = 'Pasajeros'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.tipo_documento} {self.documento})"

# Create your models here.
