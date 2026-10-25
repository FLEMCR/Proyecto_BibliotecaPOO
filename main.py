from modulos import menu
from modulos.biblioteca import Biblioteca


def main():
    biblioteca = Biblioteca()
    menu.portada(biblioteca)
    menu.menu_de_acceso(biblioteca)


main()
