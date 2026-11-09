import sys

from PyQt5.QtWidgets import QApplication
from ui.acceso import Acceso


def main():
    app = QApplication(sys.argv)
    ventana = Acceso()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
