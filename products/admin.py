from django.contrib import admin
from .models import Usuario, Avion, Vuelo, Pasajero, Asiento, Reserva, Boleto # si lo creaste

admin.site.register(Usuario)
admin.site.register(Avion)
admin.site.register(Vuelo)
admin.site.register(Pasajero)
admin.site.register(Asiento)
admin.site.register(Reserva)
admin.site.register(Boleto)
# admin.site.register(Producto)  # si existe

# Register your models here.
