from modulos import menu
from modulos.biblioteca import Biblioteca
from modulos.menu import menu_principal


def main():
    menu.portada()
    biblioteca = Biblioteca()
    menu_principal(biblioteca)


main()
