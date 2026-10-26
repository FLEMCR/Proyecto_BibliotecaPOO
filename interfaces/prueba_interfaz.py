import sys

from prueba_conexion import FormularioLibro
from PyQt5.QtWidgets import QApplication


def main():

    app = QApplication(sys.argv)

    ventana = FormularioLibro()
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
