from modulos import errores, menu
from modulos.biblioteca import Biblioteca


def main():
    try:
        biblioteca = Biblioteca()
    except errores.ErrorDeArchivo as error:
        print("No se pudieron leer los datos: " + str(error))
        return
    menu.portada(biblioteca)
    menu.menu_de_acceso(biblioteca)


main()
