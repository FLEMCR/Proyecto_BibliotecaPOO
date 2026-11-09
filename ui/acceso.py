"""Ventana de acceso al sistema de biblioteca."""

from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog

from core import configuracion, errores


class VentanaAcceso(QDialog):
    """Pide el DNI, valida la cuenta y avisa cuando el ingreso es correcto."""

    usuario_autenticado = pyqtSignal(object)

    def __init__(self, biblioteca, parent=None):
        super().__init__(parent)
        uic.loadUi(str(Path(__file__).with_suffix(".ui")), self)
        self.biblioteca = biblioteca
        self.usuario_actual = None
        self._hay_error = False

        self.setWindowTitle(f"{configuracion.NOMBRE_BIBLIOTECA} | Acceso")
        self.tituloLabel.setText(configuracion.NOMBRE_BIBLIOTECA)
        self.subtituloLabel.setText(configuracion.LEMA)

        self.dniLineEdit.setValidator(QIntValidator(0, 99999999, self))
        self.dniLineEdit.setFocus()
        self.entrarButton.clicked.connect(self.validar_ingreso)
        self.dniLineEdit.returnPressed.connect(self.validar_ingreso)
        self.dniLineEdit.textChanged.connect(self.limpiar_mensaje)
        self.salirButton.clicked.connect(self.reject)
        self._mostrar_mensaje(
            "Prueba con 11111111 (estudiante) o 33333333 (administrador).",
            error=False,
        )

    def limpiar(self):
        """Deja la pantalla lista para un nuevo inicio de sesión."""
        self.dniLineEdit.clear()
        self.dniLineEdit.setFocus()
        self.usuario_actual = None
        self._mostrar_mensaje(
            "Prueba con 11111111 (estudiante) o 33333333 (administrador).",
            error=False,
        )

    def limpiar_mensaje(self):
        if self._hay_error:
            self._mostrar_mensaje("Usa el DNI registrado en la biblioteca.", error=False)

    def _mostrar_mensaje(self, texto, error=True):
        self.ayudaLabel.setText(texto)
        self._hay_error = error

    def validar_ingreso(self):
        """Valida DNI, estado de la cuenta y vigencia de la membresía."""
        dni = self.dniLineEdit.text().strip()
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
        self.usuario_autenticado.emit(usuario)
        self.accept()
