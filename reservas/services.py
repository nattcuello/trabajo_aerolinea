from vuelos.models import Avion, Vuelo
from reservas.models import Asiento, AsientoVuelo


class AsientoService:

    @staticmethod
    def generar_asientos_para_avion(avion: Avion):
        """
        Crea asientos para un avión dado según sus filas y columnas,
        sin duplicar si ya existen (idempotente).
        """
        letras = [chr(65 + i) for i in range(avion.columnas)]

        # Asientos existentes en el avión
        existentes = set(
            Asiento.objects.filter(avion=avion)
            .values_list('fila', 'columna')
        )

        asientos_creados = []
        for fila in range(1, avion.filas + 1):
            for letra in letras:
                if (fila, letra) in existentes:
                    continue  # ya existe

                tipo = AsientoService.determinar_tipo_asiento(letra, avion.columnas)
                asientos_creados.append(
                    Asiento(
                        avion=avion,
                        fila=fila,
                        columna=letra,
                        tipo=tipo,
                        estado='disponible'
                    )
                )

        if asientos_creados:
            Asiento.objects.bulk_create(asientos_creados)

        return asientos_creados

    @staticmethod
    def generar_asientos_para_vuelo(vuelo: Vuelo):
        """
        Crea los registros AsientoVuelo para todos los asientos de un avión,
        vinculados al vuelo indicado, sin duplicar si ya existen.
        """
        asientos_base = Asiento.objects.filter(avion=vuelo.avion)
        existentes = set(
            AsientoVuelo.objects.filter(vuelo=vuelo)
            .values_list('asiento_id', flat=True)
        )

        asientos_vuelo_creados = [
            AsientoVuelo(vuelo=vuelo, asiento=asiento, estado='disponible')
            for asiento in asientos_base
            if asiento.id not in existentes
        ]

        if asientos_vuelo_creados:
            AsientoVuelo.objects.bulk_create(asientos_vuelo_creados)

        return asientos_vuelo_creados

    @staticmethod
    def determinar_tipo_asiento(columna, total_columnas):
        """
        Devuelve el tipo de asiento (ventana, pasillo, etc.)
        según la columna y el total de columnas del avión.
        """
        if columna == 'A' or columna == chr(65 + total_columnas - 1):
            return 'ventana'
        if columna == 'B' or columna == chr(65 + total_columnas - 2):
            return 'pasillo'
        return 'medio'
