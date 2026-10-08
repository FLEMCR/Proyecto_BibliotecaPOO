import sys

import utilidades
from config import nombre_biblioteca


def divisor(texto_hotdog):
    print("-" * 30, "\n", end=" ")
    print(f"{texto_hotdog.upper()}")
    print("-" * 30)


def menu_principal():
    while True:
        divisor(f"Bienvenido a {nombre_biblioteca} \n ¿Estas registrado?")
        print("1. Iniciar sesion")
        print("2. Registrarse")
        print("3. Acceder sin iniciar sesion (Invitado)")
        print("0. Salir")

        try:
            opcion = int(input("Elija una opcion: "))
        except ValueError:
            print("Ingresa una opcion valida")
            utilidades.pausa()
            continue

        if opcion == 1:
            print("Se procedera a iniciar sesion...")
            utilidades.pausa()
            pass
        elif opcion == 2:
            print("Se procedera a registrarse...")
            utilidades.pausa()
            pass
        elif opcion == 3:
            print("Se procedera a acceder sin iniciar sesion...")
            utilidades.pausa()
            pass
        elif opcion == 0:
            utilidades.verificar_accion("Salir", sys.exit)
        else:
            print("Ingrese una opcion valida")


menu_principal()
