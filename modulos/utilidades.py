from datetime import date, timedelta

from modulos import errores


def titulo(texto, caracter="="):
    linea = caracter * 60
    return f"{linea}\n{texto.upper().center(60)}\n{linea}"


def pausa():
    print()
    input("Presiona ENTER para continuar...")


def validar_dni(texto):
    limpio = str(texto).strip()
    if len(limpio) != 8 or not limpio.isdigit():
        raise errores.DatosInvalidosError("El DNI debe tener 8 digitos")
    return limpio


def validar_isbn(codigo):
    limpio = str(codigo).strip()
    if len(limpio) != 13 or not limpio.isdigit():
        raise errores.DatosInvalidosError("El ISBN debe tener 13 digitos")
    return limpio


def responder_si_no(texto):
    respuesta = input(texto).strip().lower()
    if respuesta == "s" or respuesta == "si":
        return True
    return False


def convertir_fecha(texto):
    # date() pide el orden inverso al que usamos al escribir: anio, mes, dia
    (anio, mes, dia) = str(texto).split("-")
    return date(int(anio), int(mes), int(dia))


def sumar_dias(fecha, dias):
    return fecha + timedelta(days=dias)


"""  AQUI DEJO UN EJEMPLO DE RECURSION, HAY QUE USAR ESE TEMA
def cuenta_regresiva(n):
    if n <= 0:
        print("Listo!")
        return 0
    print(n)
    return cuenta_regresiva(n - 1)
"""
