# reservas/services.py

from vuelos.models import Avion

class AsientoService:

    @staticmethod
    def generar_asientos_para_avion(avion: Avion):
        """
        Crea asientos para un avión dado, según sus filas y columnas.
        """
        from .models import Asiento  # ✅ Import diferido para evitar import circular

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
        Determina si el asiento es de ventana, pasillo o medio.
        """
        if total_columnas == 1:
            return 'ventana'
        elif letra == 'A' or letra == chr(64 + total_columnas):
            return 'ventana'
        elif total_columnas >= 4 and (letra == 'B' or letra == chr(65 + total_columnas - 2)):
            return 'pasillo'
        else:
            return 'medio'
