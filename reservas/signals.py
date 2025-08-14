# reservas/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from vuelos.models import Vuelo
from reservas.models import Asiento, AsientoVuelo

@receiver(post_save, sender=Vuelo)
def crear_asientos_para_vuelo(sender, instance, created, **kwargs):
    if created:
        asientos = Asiento.objects.filter(avion=instance.avion)
        nuevos_asientos_vuelo = [
            AsientoVuelo(vuelo=instance, asiento=a, estado='disponible')
            for a in asientos
        ]
        AsientoVuelo.objects.bulk_create(nuevos_asientos_vuelo)
        print(f"✅ {len(nuevos_asientos_vuelo)} asientos creados para vuelo {instance.id}")
