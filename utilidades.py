def pausa():
    input("\nPresione Enter para continuar...")


def verificar_accion(estado, accion):
    while True:
        verificar = input(f"¿Estas seguro de {estado}? (s/n): ").lower()

        if verificar == "s" or verificar == "si":
            accion()
        elif verificar == "n" or verificar == "no":
            break
        else:
            print("Ingresa una opcion valida")
            continue
