from modulos import biblioteca, menu


def main():
    sistema = biblioteca.Biblioteca()
    resumen = sistema.cargar_datos()
    print(f"Cargados: {resumen['libros']} libros, {resumen['miembros']} miembros")
    menu.ejecutar(sistema)


main()
