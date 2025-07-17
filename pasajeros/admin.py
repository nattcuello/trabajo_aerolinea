from django.contrib import admin
from .models import Pasajero


@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_documento', 'documento', 'email', 'telefono')
    search_fields = ('nombre', 'documento', 'email')
    list_filter = ('tipo_documento',)

# Register your models here.
