from pathlib import Path

from core import errores
from PyQt5 import uic
from PyQt5.QtCore import QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget

ruta_ui = Path(__file__).resolve().parent / "prestamo.ui"


class VentanaPrestamo(QWidget):
    """Página para registrar un préstamo a nombre del usuario conectado."""

    datos_actualizados = pyqtSignal()

    def __init__(self, biblioteca, usuario, parent=None):
        super().__init__(parent)
        uic.loadUi(str(ruta_ui), self)
        self.biblioteca = biblioteca
        self.usuario = usuario
        self._libro_seleccionado = None

        self.isbnLineEdit.setValidator(
            QRegExpValidator(QRegExp(r"\d{0,13}"), self)
        )
        self.isbnLineEdit.returnPressed.connect(self.buscar_libro)
        self.prestarButton.clicked.connect(self.prestar)
        self.cancelarButton.clicked.connect(self.limpiar)
        self.actualizar()

    def actualizar(self):
        """Actualiza el usuario y el estado de su préstamo activo."""
        self.usuarioLabel.setText(
            f"{self.usuario.nombre()} · DNI {self.usuario.dni()}"
        )
        prestamo = self.biblioteca.prestamo_activo_de_usuario(self.usuario.dni())

        if prestamo is None:
            self._habilitar_formulario(True)
            self.prestamoActivoLabel.setText("No tienes préstamos activos.")
            self.fechaLimiteLabel.setText(
                "Fecha límite de devolución: se calcula al confirmar."
            )
            return

        self._habilitar_formulario(False)
        titulo = self._titulo_del_prestamo(prestamo)
        self.prestamoActivoLabel.setText(
            f"Ya tienes un préstamo activo: {titulo}. "
            "Devuélvelo antes de pedir otro libro."
        )
        self.fechaLimiteLabel.setText(
            f"Fecha límite de devolución: {prestamo.fecha_limite()}"
        )

    def _habilitar_formulario(self, habilitado):
        """Habilita o bloquea el ISBN y el botón de préstamo."""
        self.isbnLineEdit.setEnabled(habilitado)
        self.prestarButton.setEnabled(habilitado)

    def _titulo_del_prestamo(self, prestamo):
        """Devuelve el título del libro de un préstamo o su ISBN si no existe."""
        try:
            return self.biblioteca.libro(prestamo.isbn()).titulo()
        except errores.ErrorBiblioteca:
            return prestamo.isbn()

    def buscar_libro(self):
        """Busca el libro por ISBN y muestra su disponibilidad."""
        if self.biblioteca.prestamo_activo_de_usuario(self.usuario.dni()) is not None:
            self.actualizar()
            return

        isbn = self.isbnLineEdit.text().strip()
        if isbn == "":
            self._limpiar_detalle()
            self._mensaje("Escribe el ISBN del libro que quieres llevar.")
            return

        try:
            libro = self.biblioteca.libro(isbn)
        except errores.ErrorBiblioteca as error:
            self._limpiar_detalle()
            self._mensaje(str(error), error=True)
            return

        self._libro_seleccionado = libro
        self.tituloLibroLabel.setText(f"{libro.titulo()} · {libro.autor()}")
        self.disponiblesLabel.setText(
            f"Disponibles para préstamo: {libro.disponibles()} "
            f"de {libro.ejemplares()} ejemplares"
        )

        if libro.se_puede_prestar():
            self._mensaje("Libro disponible. Puedes confirmar el préstamo.")
            self.prestarButton.setEnabled(True)
        else:
            self.prestarButton.setEnabled(False)
            if libro.disponibles() == 1:
                self._mensaje(
                    "Solo queda un ejemplar y se reserva para consulta.",
                    error=True,
                )
            else:
                self._mensaje(
                    "Este libro no tiene ejemplares disponibles para préstamo.",
                    error=True,
                )

    def prestar(self):
        """Registra el préstamo del ISBN escrito usando el DNI de la sesión."""
        if self.biblioteca.prestamo_activo_de_usuario(self.usuario.dni()) is not None:
            self.actualizar()
            return

        isbn = self.isbnLineEdit.text().strip()
        try:
            prestamo = self.biblioteca.prestar(isbn, self.usuario.dni())
        except errores.ErrorBiblioteca as error:
            self._mensaje(str(error), error=True)
            return

        self._mensaje(
            f"Préstamo registrado. Fecha límite: {prestamo.fecha_limite()}."
        )
        self.isbnLineEdit.clear()
        self._limpiar_detalle()
        self.actualizar()
        self.datos_actualizados.emit()

    def limpiar(self):
        """Limpia el formulario para consultar otro ISBN."""
        self.isbnLineEdit.clear()
        self._libro_seleccionado = None
        self._limpiar_detalle()
        self._mensaje("Escribe el ISBN del libro para consultar su disponibilidad.")
        self.actualizar()
        self.isbnLineEdit.setFocus()

    def _limpiar_detalle(self):
        """Restablece los textos de la ficha del libro."""
        self.tituloLibroLabel.setText("Libro: sin seleccionar")
        self.disponiblesLabel.setText("Disponibles para préstamo: —")

    def _mensaje(self, texto, error=False):
        """Muestra una ayuda en la etiqueta de estado del formulario."""
        self.ayudaPrestamoLabel.setText(texto)

    def showEvent(self, evento):
        """Refresca el estado del préstamo al entrar a la página."""
        super().showEvent(evento)
        self.actualizar()
        self.isbnLineEdit.setFocus()
