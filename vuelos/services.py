from vuelos.models import Avion, Vuelo

from vuelos.models import Avion, Vuelo
from reservas.models import Asiento, AsientoVuelo


class AsientoService:

    @staticmethod
    def generar_asientos_para_avion(avion: Avion):
        """
        Genera todos los asientos base para un avión según sus filas y columnas.
        Estos asientos son 'plantilla' y se vinculan solo al avión.
        """
        letras = [chr(i) for i in range(65, 65 + avion.columnas)]  # A, B, C...
        asientos_creados = []
        for fila in range(1, avion.filas + 1):
            for letra in letras:
                tipo = AsientoService.determinar_tipo_asiento(letra, avion.columnas)
                asiento = Asiento(
                    avion=avion,
                    fila=fila,
                    columna=letra,
                    tipo=tipo,
                    estado='disponible'
                )
                asientos_creados.append(asiento)
        Asiento.objects.bulk_create(asientos_creados)
        return asientos_creados

    @staticmethod
    def determinar_tipo_asiento(letra: str, total_columnas: int) -> str:
        """
        Define el tipo de asiento según la posición de la columna:
        - 'ventana' si es primera o última columna
        - 'pasillo' si está al lado de la ventana (cuando columnas >=4)
        - 'medio' el resto
        """
        if total_columnas == 1:
            return 'ventana'
        primera_columna = 'A'
        ultima_columna = chr(64 + total_columnas)
        if letra == primera_columna or letra == ultima_columna:
            return 'ventana'
        elif total_columnas >= 4 and (
            letra == chr(ord(primera_columna) + 1) or letra == chr(ord(ultima_columna) - 1)
        ):
            return 'pasillo'
        else:
            return 'medio'

    @staticmethod
    def generar_asientos_para_vuelo(vuelo: Vuelo):
        """
        Crea AsientoVuelo para cada asiento base del avión asignado al vuelo.
        """
        asientos_avion = vuelo.avion.asientos.all()
        asientos_vuelo = [
            AsientoVuelo(
                vuelo=vuelo,
                asiento=asiento,
                estado='disponible'
            )
            for asiento in asientos_avion
        ]
        AsientoVuelo.objects.bulk_create(asientos_vuelo)
        return asientos_vuelo
