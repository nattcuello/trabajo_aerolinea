from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Avion
from reservas.services import AsientoService

@receiver(post_save, sender=Avion)
def crear_asientos(sender, instance, created, **kwargs):
    if created:
        AsientoService.generar_asientos_para_avion(instance)
