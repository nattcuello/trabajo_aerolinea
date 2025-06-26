
# Register your models here.
from django.contrib import admin
from .models import Avion, Vuelo


@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'capacidad', 'filas', 'columnas')
    search_fields = ('modelo',)
    list_filter = ('capacidad',)
    ordering = ('modelo',)

# Registra el modelo Avion en el admin de Django
# Esto permite gestionar instancias de Avion a través de la interfaz de administración de Django
@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    #Muestra columnas útiles en la lista de objetos Vuelo en el admin
    list_display = (
        'origen',
        'destino',
        'fecha_salida',
        'fecha_llegada',
        'estado',
        'precio_base',
        'get_avion',
    )
    # Permite buscar vuelos por origen y destino
    search_fields = ('origen', 'destino')
    # Permite filtrar vuelos por estado y fecha de salida
    list_filter = ('estado', 'fecha_salida')
    # Permite ordenar los vuelos por fecha de salida
    date_hierarchy = 'fecha_salida'
    ordering = ('fecha_salida',)

    # Método para mostrar el modelo del avión asociado al vuelo
    def get_avion(self, obj):
        return obj.avion.modelo
    get_avion.short_description = 'Avión'

    # Permite gestionar los usuarios gestores del vuelo desde el admin
    # Esto permite asignar múltiples usuarios gestores a un vuelo
    filter_horizontal = ('usuarios_gestores',)  # Para gestionar M2M con User desde admin
