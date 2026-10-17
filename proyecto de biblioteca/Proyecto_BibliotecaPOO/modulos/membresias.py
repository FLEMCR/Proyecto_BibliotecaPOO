from datetime import date

from dateutil.relativedelta import relativedelta
from errores import MembresiaNoExiste


class Membresia:
    TIPO = None
    PREFIJO = None
    LIMITE_LIBROS = 0
    _MULTA_POR_DIA = 0.50
    DESCUENTO_PORCENTAJE = 0.0
    ADMINISTRA = False

    def __init__(self):
        self._vencimiento = self.calcular_fecha_vencimiento()

    def calcular_fecha_vencimiento(self):
        return date.today() + relativedelta(months=1)

    @property
    def tipo(self):
        return self.TIPO

    @property
    def prefijo(self):
        return self.PREFIJO

    @property
    def vencimiento(self):
        return self._vencimiento

    @property
    def descuento(self):
        return self.DESCUENTO_PORCENTAJE

    def puede_administrar(self):
        return self.ADMINISTRA

    def vigente(self):
        return date.today() <= self._vencimiento

    def dias_para_vencer(self):
        return (self._vencimiento - date.today()).days

    def estado(self):
        dias = self.dias_para_vencer()
        return "Vencida" if dias < 0 else f"{dias} días"

    def multa(self):
        dias = (date.today() - self._vencimiento).days
        if dias > 0:
            return round(dias * self._MULTA_POR_DIA, 2)
        return 0.0

    def renovar(self):
        self._vencimiento = date.today() + relativedelta(months=1)

    def __str__(self):
        return f"La membresía es {self.tipo} (vence {self._vencimiento})"


class Invitado(Membresia):
    TIPO = "invitado"
    PREFIJO = "100"
    LIMITE_LIBROS = 0
    _MULTA_POR_DIA = 0.0


class Estudiante(Membresia):
    TIPO = "estudiante"
    PREFIJO = "101"
    LIMITE_LIBROS = 3
    _MULTA_POR_DIA = 0.50


class Docente(Membresia):
    TIPO = "docente"
    PREFIJO = "102"
    LIMITE_LIBROS = 5
    _MULTA_POR_DIA = 0.50
    DESCUENTO_PORCENTAJE = 0.50


class Admin(Membresia):
    TIPO = "admin"
    PREFIJO = "103"
    LIMITE_LIBROS = 5
    _MULTA_POR_DIA = 0.0
    ADMINISTRA = True


CLASES = {
    "invitado": Invitado,
    "estudiante": Estudiante,
    "docente": Docente,
    "admin": Admin,
}


def crear_membresia(tipo):
    if tipo not in CLASES:
        raise MembresiaNoExiste(f"Tipo de membresía desconocido: {tipo}")
    return CLASES[tipo]()
