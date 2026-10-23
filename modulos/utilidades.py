from datetime import date

from modulos import errores


def validar_dni(texto):
    dni = str(texto).strip()
    if len(dni) != 8 or not dni.isdigit():
        raise errores.ErrorDeDatos("El DNI debe tener 8 digitos")
    return dni


def validar_isbn(codigo):
    isbn = str(codigo).strip()
    if len(isbn) != 13 or not isbn.isdigit():
        raise errores.ErrorDeDatos("El ISBN debe tener 13 digitos")
    return isbn


def convertir_fecha(texto):
    partes = str(texto).strip().split("-")
    if len(partes) != 3:
        raise errores.ErrorDeDatos("La fecha debe tener el formato AAAA-MM-DD")
    try:
        anio, mes, dia = partes
        return date(int(anio), int(mes), int(dia))
    except ValueError:
        raise errores.ErrorDeDatos("La fecha " + str(texto) + " no es una fecha real")


def si_o_no(valor):
    if valor:
        return "Si"
    return "No"
