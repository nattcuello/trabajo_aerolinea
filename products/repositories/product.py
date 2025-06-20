from typing import Optional
from django.db.models.query import QuerySet
from .models import Usuario, Avion, Vuelo, Pasajero, Asiento, Reserva, Boleto


class UsuarioRepository:

    @staticmethod
    def get_all() -> QuerySet[Usuario]:
        return Usuario.objects.all()

    @staticmethod
    def get_by_id(usuario_id: int) -> Optional[Usuario]:
        return Usuario.objects.filter(id=usuario_id).first()

    @staticmethod
    def create(**kwargs) -> Usuario:
        return Usuario.objects.create(**kwargs)

    @staticmethod
    def delete(usuario_id: int) -> tuple[int, dict]:
        return Usuario.objects.filter(id=usuario_id).delete()


class AvionRepository:

    @staticmethod
    def get_all() -> QuerySet[Avion]:
        return Avion.objects.all()

    @staticmethod
    def get_by_id(avion_id: int) -> Optional[Avion]:
        return Avion.objects.filter(id=avion_id).first()

    @staticmethod
    def create(**kwargs) -> Avion:
        return Avion.objects.create(**kwargs)

    @staticmethod
    def delete(avion_id: int) -> tuple[int, dict]:
        return Avion.objects.filter(id=avion_id).delete()


class VueloRepository:

    @staticmethod
    def get_all() -> QuerySet[Vuelo]:
        return Vuelo.objects.all()

    @staticmethod
    def get_by_id(vuelo_id: int) -> Optional[Vuelo]:
        return Vuelo.objects.filter(id=vuelo_id).first()

    @staticmethod
    def get_by_estado(estado: str) -> QuerySet[Vuelo]:
        return Vuelo.objects.filter(estado=estado)

    @staticmethod
    def create(**kwargs) -> Vuelo:
        return Vuelo.objects.create(**kwargs)

    @staticmethod
    def delete(vuelo_id: int) -> tuple[int, dict]:
        return Vuelo.objects.filter(id=vuelo_id).delete()


class PasajeroRepository:

    @staticmethod
    def get_all() -> QuerySet[Pasajero]:
        return Pasajero.objects.all()

    @staticmethod
    def get_by_documento(doc: str) -> Optional[Pasajero]:
        return Pasajero.objects.filter(documento=doc).first()

    @staticmethod
    def create(**kwargs) -> Pasajero:
        return Pasajero.objects.create(**kwargs)


class AsientoRepository:

    @staticmethod
    def get_all() -> QuerySet[Asiento]:
        return Asiento.objects.all()

    @staticmethod
    def get_disponibles(avion_id: int) -> QuerySet[Asiento]:
        return Asiento.objects.filter(avion_id=avion_id, estado='disponible')

    @staticmethod
    def create(**kwargs) -> Asiento:
        return Asiento.objects.create(**kwargs)


class ReservaRepository:

    @staticmethod
    def get_all() -> QuerySet[Reserva]:
        return Reserva.objects.all()

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Reserva]:
        return Reserva.objects.filter(codigo_reserva=codigo).first()

    @staticmethod
    def create(**kwargs) -> Reserva:
        return Reserva.objects.create(**kwargs)


class BoletoRepository:

    @staticmethod
    def get_all() -> QuerySet[Boleto]:
        return Boleto.objects.all()

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Boleto]:
        return Boleto.objects.filter(codigo_barra=codigo).first()

    @staticmethod
    def create(**kwargs) -> Boleto:
        return Boleto.objects.create(**kwargs)
