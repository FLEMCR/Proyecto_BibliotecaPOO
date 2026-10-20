from modulos import errores


def titulo(texto, caracter="="):
    linea = caracter * 60
    return f"\n{linea}\n{texto.upper().center(60)}\n{linea}"


def pausa():
    texto = "Presiona ENTER para continuar..."
    return input(texto)


def validar_dni(texto):
    limpio = str(texto).strip()
    if len(limpio) != 8 or not limpio.isdigit():
        raise errores.DatosInvalidosError("El DNI debe tener 8 digitos")
    return limpio


def validar_isbn(codigo):
    if len(codigo) != 13:
        raise errores.DatosInvalidosError("El ISBN debe tener 13 digitos")
    return codigo


def responder_si_no(texto="¿Deseas continuar? (s/n): "):
    respuesta = input(texto).strip().lower()
    if respuesta == "s" or respuesta == "si":
        return True
    return False


def contar_regresiva(n):
    if n <= 0:
        print("¡Listo!")
        return 0
    print(n)
    return contar_regresiva(n - 1)
