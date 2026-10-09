import errores


def pausa():
    input("\nPresione Enter para continuar...")


def divisor(titulo):
    linea = "-" * 62
    print(f"\n{linea}\n  {titulo.upper().center(58)}\n{linea}")


def verificar_accion(estado, accion):
    while True:
        verificar = input(f"¿Estas seguro de {estado}? (s/n): ").strip().lower()
        if verificar in ("s", "si", "sí"):
            return accion()
        elif verificar in ("n", "no"):
            break
        print("Ingresa una opcion valida")


def validar_dni(texto):
    limpio = str(texto).strip()
    if len(limpio) != 8 or not limpio.isdigit():
        raise errores.DatosInvalidosError("El DNI tiene 8 digitos")
    return limpio
