from django.core.management.base import BaseCommand
from vuelos.models import Vuelo
from reservas.models import AsientoVuelo
from reservas.services import AsientoService

class Command(BaseCommand):
    help = "Regenera los asientos (AsientoVuelo) para vuelos que no los tienen."

    def handle(self, *args, **kwargs):
        vuelos_sin_asientos = Vuelo.objects.exclude(
            id__in=AsientoVuelo.objects.values_list('vuelo_id', flat=True)
        )

        if not vuelos_sin_asientos.exists():
            self.stdout.write(self.style.SUCCESS("Todos los vuelos ya tienen asientos generados."))
            return

        for vuelo in vuelos_sin_asientos:
            AsientoService.generar_asientos_para_vuelo(vuelo)
            self.stdout.write(self.style.SUCCESS(f"Asientos generados para vuelo {vuelo.id}"))

        self.stdout.write(self.style.SUCCESS("Proceso completado."))
