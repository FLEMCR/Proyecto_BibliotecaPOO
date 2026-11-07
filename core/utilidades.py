from datetime import date

from proyecto_parcial.core import errores


def pausa():
    """Pausa la ejecución en la consola hasta que el usuario presione ENTER."""
    print()
    input("Pulsa ENTER para volver al menu")


def validar_dni(texto):
    """Valida que el DNI sea una cadena numérica exacta de 8 dígitos y la retorna limpia."""
    dni = str(texto).strip()
    if len(dni) != 8 or not dni.isdigit():
        raise errores.ErrorDeDatos("El DNI debe tener 8 digitos")
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


def si_o_no(valor):
    """Convierte un valor booleano True/False en un texto legible 'Si' o 'No' para mostrar en pantalla."""
    if valor:
        return "Si"
    return "No"
