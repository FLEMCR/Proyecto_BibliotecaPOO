from modulos import biblioteca, errores, menu


def main():
    try:
        mi_biblioteca = biblioteca.Biblioteca()
    except errores.ErrorDeArchivo as error:
        print("No se pudieron leer los datos: " + str(error))
        return
    menu.portada(mi_biblioteca)
    menu.menu_de_acceso(mi_biblioteca)


main()
