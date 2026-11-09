from pathlib import Path

from core import configuracion, errores
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox

ruta_ui = Path(__file__).resolve().parent / "acceso.ui"


class VentanaAcceso(QDialog):
    usuario_autenticado = pyqtSignal(object)

    def __init__(self, biblioteca):
        super().__init__()
        uic.loadUi(str(ruta_ui), self)
        self.biblioteca = biblioteca
        self.usuario_actual = None

        self.setWindowTitle(configuracion.NOMBRE_BIBLIOTECA)
        self.tituloLabel.setText(configuracion.NOMBRE_BIBLIOTECA)
        self.lemaLabel.setText(configuracion.LEMA)

        self.entrarBtn.clicked.connect(self.validar_usuario)
        self.salirBtn.clicked.connect(self.reject)

    def validar_usuario(self):
        """Valida DNI, estado de la cuenta y vigencia de la membresía."""
        dni = self.dniLineEdit.text().strip().lower()
        if dni == "":
            self._mostrar_mensaje("Escribe tu DNI para continuar.")
            self.dniLineEdit.setFocus()
            return
        try:
            usuario = self.biblioteca.usuario(dni)
        except errores.ErrorBiblioteca as error:
            self._mostrar_mensaje(str(error))
            self.dniLineEdit.setFocus()
            self.dniLineEdit.selectAll()
            return

        if not usuario.esta_activo():
            self._mostrar_mensaje(
                f"{usuario.nombre()} está de baja. Consulta con administración."
            )
            return
        if not usuario.tiene_membresia_vigente():
            self._mostrar_mensaje(
                f"La membresía de {usuario.nombre()} venció el "
                f"{usuario.vencimiento_membresia()}."
            )
            return

        self.usuario_actual = usuario
        self.usuario_autenticado.emit(self.usuario_actual)
        # En esta señal de arriba me sale un error pero es falso positivo del Pylance porque si funciona al ejecutarse
        self.accept()

    def limpiar(self):
        """Deja la pantalla lista para un nuevo inicio de sesión."""
        self.dniLineEdit.clear()
        self.dniLineEdit.setFocus()
        self.usuario_actual = None

    def _mostrar_mensaje(self, mensaje):
        dato = QMessageBox(self)
        dato.setText(mensaje)
        dato.exec()
