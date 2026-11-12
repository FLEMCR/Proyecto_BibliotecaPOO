from datetime import date
from pathlib import Path

from core import configuracion, errores, utilidades
from PyQt5 import uic
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QMessageBox

ruta_ui = Path(__file__).resolve().parent / "registro.ui"


class VentanaRegistro(QDialog):
    """Formulario de autorregistro para un usuario nuevo."""

    def __init__(self, biblioteca, parent=None, permitir_administrador=False):
        super().__init__(parent)
        uic.loadUi(str(ruta_ui), self)
        self.biblioteca = biblioteca
        self.permitir_administrador = permitir_administrador
        self.dni_registrado = None

        tipos = ["Estudiante", "Docente"]
        if permitir_administrador:
            tipos.append("Administrador")
        self.tipoComboBox.clear()
        self.tipoComboBox.addItems(tipos)
        self.dniLineEdit.setValidator(QIntValidator(0, 99999999, self))
        self.dniLineEdit.setMaxLength(8)
        self.membresiaLabel.setText(
            "La membresía dura 3 meses desde hoy y vence el "
            f"{utilidades.sumar_meses(date.today(), configuracion.MESES_DE_MEMBRESIA)}."
        )
        self.registrarButton.setDefault(True)
        self.registrarButton.clicked.connect(self.registrar)
        self.cancelarButton.clicked.connect(self.reject)
        self.nombreLineEdit.returnPressed.connect(self.dniLineEdit.setFocus)
        self.dniLineEdit.returnPressed.connect(self.registrar)
        self.nombreLineEdit.setFocus()

    def registrar(self):
        """Valida los datos y crea el usuario en la biblioteca."""
        try:
            usuario = self.biblioteca.registrar_usuario(
                {
                    "dni": self.dniLineEdit.text(),
                    "nombre": self.nombreLineEdit.text(),
                    "tipo": self.tipoComboBox.currentText(),
                },
                permitir_administrador=self.permitir_administrador,
            )
        except errores.ErrorBiblioteca as error:
            if hasattr(self, "ayudaRegistroLabel"):
                self.ayudaRegistroLabel.setText(str(error))
            else:
                QMessageBox.warning(self, "No se pudo registrar", str(error))
            return

        self.dni_registrado = usuario.dni()
        self.accept()
