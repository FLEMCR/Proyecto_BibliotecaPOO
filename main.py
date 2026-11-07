from proyecto_parcial.core import menu
from proyecto_parcial.core.biblioteca import Biblioteca


def main():
    biblioteca = Biblioteca()
    menu.portada(biblioteca)
    menu.menu_de_acceso(biblioteca)


main()
