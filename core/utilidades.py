import calendar
import unicodedata
from datetime import date

from . import errores


def normalizar_texto(texto):
    """Convierte un texto a minúsculas y quita tildes para comparar búsquedas."""
    texto = str(texto).strip().lower()
    sin_tildes = unicodedata.normalize("NFD", texto)
    return "".join(
        caracter for caracter in sin_tildes if unicodedata.category(caracter) != "Mn"
    )


def validar_dni(texto):
    """Valida que el DNI sea una cadena numérica exacta de 8 dígitos y la retorna limpia."""
    dni = str(texto).strip()
    if len(dni) != 8 or not dni.isdigit():
        raise errores.ErrorDeDatos("El DNI debe tener 8 digitos numericos")
    return dni


def validar_isbn(codigo):
    """Valida que el código ISBN sea una cadena numérica de 13 dígitos para identificar un libro."""
    isbn = str(codigo).strip()
    if len(isbn) != 13 or not isbn.isdigit():
        raise errores.ErrorDeDatos("El ISBN debe tener 13 digitos")
    return isbn


def convertir_fecha(texto):
    """Convierte un texto con formato AAAA-MM-DD a un objeto date válido verificando que la fecha exista."""
    partes = str(texto).strip().split("-")
    if len(partes) != 3:
        raise errores.ErrorDeDatos("La fecha debe tener el formato AAAA-MM-DD")
    try:
        año, mes, dia = partes
        return date(int(año), int(mes), int(dia))
    except ValueError:
        raise errores.ErrorDeDatos("La fecha " + str(texto) + " no es una fecha real")


def sumar_meses(fecha, meses):
    """Suma una cantidad de meses a una fecha y ajusta el día al último del mes."""
    if not isinstance(fecha, date):
        fecha = convertir_fecha(fecha)
    meses_totales = fecha.month - 1 + int(meses)
    año = fecha.year + meses_totales // 12
    mes = meses_totales % 12 + 1
    ultimo_dia = calendar.monthrange(año, mes)[1]
    dia = min(fecha.day, ultimo_dia)
    return date(año, mes, dia)
