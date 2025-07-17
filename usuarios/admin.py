# usuarios/admin.py

from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol')
    list_filter = ('rol',)
    search_fields = ('user__username', 'user__email')
