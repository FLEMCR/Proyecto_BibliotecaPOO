from pathlib import Path

from core import configuracion, errores
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

ruta_ui = Path(__file__).resolve().parent / "libro_form.ui"


class VentanaLibro(QWidget):
    """Página para registrar o actualizar un libro del catálogo."""

    datos_actualizados = pyqtSignal()

    def __init__(self, biblioteca, usuario=None, parent=None):
        super().__init__(parent)
        uic.loadUi(str(ruta_ui), self)
        self.biblioteca = biblioteca
        self.usuario = usuario
        self._isbn_original = None

        self.categoriaComboBox.addItems(configuracion.CATEGORIAS)
        for letra, nombre in configuracion.SECCIONES.items():
            self.seccionComboBox.addItem(f"{letra} · {nombre}", letra)

        self.guardarButton.clicked.connect(self.guardar)
        self.cancelarButton.clicked.connect(self.limpiar)
        self.limpiar()

    def guardar(self):
        """Registra o actualiza el libro con los datos del formulario."""
        datos = {
            "isbn": self.isbnLineEdit.text(),
            "titulo": self.tituloLineEdit.text(),
            "autor": self.autorLineEdit.text(),
            "categoria": self.categoriaComboBox.currentText(),
            "seccion": self.seccionComboBox.currentData(),
            "estante": self.estanteSpinBox.value(),
            "ejemplares": self.ejemplaresSpinBox.value(),
            "disponibles": self.disponiblesSpinBox.value(),
        }

        try:
            if self._isbn_original is None:
                libro = self.biblioteca.registrar_libro(datos)
            else:
                libro = self.biblioteca.actualizar_libro(
                    self._isbn_original, datos
                )
        except errores.ErrorBiblioteca as error:
            self._mensaje(str(error), error=True)
            return

        self.limpiar()
        self._mensaje(f"Libro guardado: {libro.titulo()}.")
        self.datos_actualizados.emit()

    def cargar_libro(self, isbn):
        """Carga un libro existente en el formulario para editarlo."""
        try:
            libro = self.biblioteca.libro(isbn)
        except errores.ErrorBiblioteca as error:
            self._mensaje(str(error), error=True)
            return

        self._isbn_original = libro.isbn()
        self.isbnLineEdit.setText(libro.isbn())
        self.isbnLineEdit.setEnabled(False)
        self.tituloLineEdit.setText(libro.titulo())
        self.autorLineEdit.setText(libro.autor())
        self.categoriaComboBox.setCurrentText(libro.categoria())
        indice_seccion = self.seccionComboBox.findData(libro.seccion())
        self.seccionComboBox.setCurrentIndex(max(indice_seccion, 0))
        self.estanteSpinBox.setValue(libro.estante())
        self.ejemplaresSpinBox.setValue(libro.ejemplares())
        self.disponiblesSpinBox.setValue(libro.disponibles())
        self.tituloFormularioLabel.setText("Editar libro")
        self._mensaje("Modifica los datos y guarda los cambios.")

    def limpiar(self):
        """Deja el formulario listo para registrar un libro nuevo."""
        self._isbn_original = None
        self.isbnLineEdit.setEnabled(True)
        self.isbnLineEdit.clear()
        self.tituloLineEdit.clear()
        self.autorLineEdit.clear()
        self.categoriaComboBox.setCurrentIndex(0)
        self.seccionComboBox.setCurrentIndex(0)
        self.estanteSpinBox.setValue(1)
        self.ejemplaresSpinBox.setValue(1)
        self.disponiblesSpinBox.setValue(1)
        self.tituloFormularioLabel.setText("Datos del libro")
        self._mensaje("El ISBN debe tener 13 dígitos y no puede repetirse.")
        self.isbnLineEdit.setFocus()

    def _mensaje(self, texto, error=False):
        """Muestra una ayuda en la etiqueta de estado del formulario."""
        self.ayudaLibroLabel.setText(texto)

    def showEvent(self, evento):
        """Enfoca el ISBN al entrar a la página."""
        super().showEvent(evento)
        if self.isbnLineEdit.isEnabled():
            self.isbnLineEdit.setFocus()
