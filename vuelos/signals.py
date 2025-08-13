from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Avion, Vuelo
from reservas.services import AsientoService

@receiver(post_save, sender=Avion)
def crear_asientos_base(sender, instance, created, **kwargs):
    """
    Cuando se crea un avión nuevo, generar sus asientos base.
    """
    if created:
        AsientoService.generar_asientos_para_avion(instance)

@receiver(post_save, sender=Vuelo)
def crear_asientos_para_vuelo(sender, instance, created, **kwargs):
    """
    Cuando se crea un vuelo nuevo, generar sus asientos vinculados (AsientoVuelo).
    """
    if created:
        AsientoService.generar_asientos_para_vuelo(instance)
