from django.db import models

class Usuario(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('cliente', 'Cliente'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')

    def __str__(self):
        return self.username


class Avion(models.Model):
    modelo = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    filas = models.PositiveIntegerField()
    columnas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.modelo} (Capacidad: {self.capacidad})"


class Vuelo(models.Model):
    ESTADO_CHOICES = [
        ('programado', 'Programado'),
        ('en_vuelo', 'En Vuelo'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    avion = models.ForeignKey(Avion, on_delete=models.PROTECT, related_name='vuelos')
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    duracion = models.DurationField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programado')
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.origen} → {self.destino} ({self.fecha_salida.date()})"


class Pasajero(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('dni', 'DNI'),
        ('pasaporte', 'Pasaporte'),
    ]

    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=50, unique=True)
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} ({self.documento})"


class Asiento(models.Model):
    TIPO_CHOICES = [
        ('economico', 'Económico'),
        ('premium', 'Premium'),
        ('primera', 'Primera Clase'),
    ]
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('ocupado', 'Ocupado'),
    ]

    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name='asientos')
    numero = models.CharField(max_length=5)
    fila = models.PositiveIntegerField()
    columna = models.PositiveIntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')

    class Meta:
        unique_together = ('avion', 'numero')

    def __str__(self):
        return f"Asiento {self.numero} ({self.tipo}) - {self.avion.modelo}"


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('reservado', 'Reservado'),
        ('cancelado', 'Cancelado'),
        ('check_in', 'Check-in'),
    ]

    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE, related_name='reservas')
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, related_name='reservas')
    asiento = models.OneToOneField(Asiento, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='reservado')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_reserva = models.CharField(max_length=10, unique=True)

    class Meta:
        unique_together = ('vuelo', 'pasajero')

    def __str__(self):
        return f"Reserva {self.codigo_reserva} - {self.pasajero.nombre}"


class Boleto(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('usado', 'Usado'),
        ('anulado', 'Anulado'),
    ]

    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='boleto')
    codigo_barra = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

    def __str__(self):
        return f"Boleto {self.codigo_barra} - {self.reserva.pasajero.nombre}"
