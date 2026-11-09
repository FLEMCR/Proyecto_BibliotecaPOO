from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

ruta_ui = Path(__file__).resolve().parent / "principal.ui"


class VentanaPrincipal(QMainWindow):
    sesion_cerrada = pyqtSignal()

    def __init__(self, biblioteca, usuario):
        super().__init__()
        uic.loadUi(str(ruta_ui), self)
        self.biblioteca = biblioteca
        self.usuario = usuario

        self.bienvenidaLabel.setText(f"Bienvenido, {usuario.nombre()}")
        self.cerrarSesionButton.clicked.connect(self.cerrar_sesion)

    def cerrar_sesion(self):
        """Avisa al controlador para que vuelva a la pantalla de acceso."""
        self.sesion_cerrada.emit()
