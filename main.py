from core import menu
from core.biblioteca import Biblioteca


def main():
    biblioteca = Biblioteca()
    menu.portada(biblioteca)
    menu.menu_de_acceso(biblioteca)


if __name__ == "__main__":
    main()
