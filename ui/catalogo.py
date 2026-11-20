import html
from pathlib import Path

from core import errores
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QWidget

ruta_ui = Path(__file__).resolve().parent / "catalogo.ui"


class VentanaCatalogo(QWidget):
    """Página del catálogo con búsqueda, filtros, tabla y ficha del libro."""

    prestamo_solicitado = pyqtSignal(str)
    edicion_solicitada = pyqtSignal(str)
    eliminacion_solicitada = pyqtSignal(str)

    def __init__(self, biblioteca, usuario=None, parent=None):
        super().__init__(parent)
        uic.loadUi(str(ruta_ui), self)
        self.biblioteca = biblioteca
        self.usuario = usuario

        es_admin = self.usuario is not None and self.usuario.puede_administrar()
        for boton in (
            self.editarLibroButton,
            self.eliminarLibroButton,
        ):
            boton.setVisible(es_admin)

        self.campoComboBox.addItems(
            ["Todo", "ISBN", "Título", "Autor", "Categoría"]
        )
        self.ordenarComboBox.addItems(
            ["Título", "Autor", "Categoría", "Disponibilidad"]
        )
        self._cargar_categorias()
        self._conectar_senales()
        self.buscar()

    def _conectar_senales(self):
        """Conecta los controles de búsqueda y la selección de la tabla."""
        self.buscarButton.clicked.connect(self.buscar)
        self.buscarLineEdit.returnPressed.connect(self.buscar)
        self.limpiarButton.clicked.connect(self.limpiar)
        self.categoriaComboBox.currentIndexChanged.connect(self.buscar)
        self.ordenarComboBox.currentIndexChanged.connect(self.buscar)
        self.soloDisponiblesCheckBox.toggled.connect(self.buscar)
        self.tablaLibros.itemSelectionChanged.connect(self._mostrar_detalle)
        self.prestarDesdeCatalogoButton.clicked.connect(self._solicitar_prestamo)
        self.editarLibroButton.clicked.connect(self._solicitar_edicion)
        self.eliminarLibroButton.clicked.connect(self._solicitar_eliminacion)

    def _cargar_categorias(self):
        """Llena el filtro de categorías con las categorías del catálogo."""
        self.categoriaComboBox.clear()
        self.categoriaComboBox.addItem("Todas")
        self.categoriaComboBox.addItems(self.biblioteca.categorias())

    def buscar(self):
        """Aplica los filtros y muestra los libros encontrados en la tabla."""
        categoria = self.categoriaComboBox.currentText()
        libros = self.biblioteca.buscar_avanzado(
            texto=self.buscarLineEdit.text(),
            campo=self.campoComboBox.currentText(),
            categoria=categoria,
            solo_disponibles=self.soloDisponiblesCheckBox.isChecked(),
            ordenar_por=self.ordenarComboBox.currentText(),
        )
        self._llenar_tabla(libros)

    def _llenar_tabla(self, libros):
        """Coloca los libros en la tabla y actualiza el contador."""
        self.tablaLibros.setSortingEnabled(False)
        self.tablaLibros.clearContents()
        self.tablaLibros.setRowCount(len(libros))

        for fila, libro in enumerate(libros):
            valores = [
                libro["isbn"],
                libro["titulo"],
                libro["autor"],
                libro["categoria"],
                str(libro["disponibles"]),
            ]
            for columna, valor in enumerate(valores):
                item = QTableWidgetItem(valor)
                if columna == 0:
                    item.setData(Qt.UserRole, libro["isbn"])
                self.tablaLibros.setItem(fila, columna, item)

        cantidad = len(libros)
        if cantidad > 0:
            self.tablaLibros.selectRow(0)
        else:
            self.detalleTextEdit.setHtml(
                "<p>No hay libros que coincidan con los filtros.</p>"
            )

    def _isbn_seleccionado(self):
        """Devuelve el ISBN del libro seleccionado, o una cadena vacía."""
        fila = self.tablaLibros.currentRow()
        if fila < 0:
            return ""
        item = self.tablaLibros.item(fila, 0)
        if item is None:
            return ""
        return str(item.data(Qt.UserRole) or "")

    def _mostrar_detalle(self):
        """Muestra la ficha del libro seleccionado en la tabla."""
        isbn = self._isbn_seleccionado()
        if not isbn:
            return
        try:
            libro = self.biblioteca.datos_de_un_libro(isbn)
        except errores.ErrorBiblioteca:
            return

        self.detalleTextEdit.setHtml(
            f"<h2>{html.escape(libro['titulo'])}</h2>"
            f"<p><b>Autor:</b> {html.escape(libro['autor'])}</p>"
            f"<p><b>Categoría:</b> {html.escape(libro['categoria'])}</p>"
            f"<p><b>ISBN:</b> {html.escape(libro['isbn'])}</p>"
            f"<p><b>Sección:</b> {html.escape(libro['seccion'])} · "
            f"{html.escape(libro['seccion_nombre'])}</p>"
            f"<p><b>Estante:</b> {libro['estante']}</p>"
            f"<p><b>Ejemplares:</b> {libro['ejemplares']} · "
            f"<b>Prestados:</b> {libro['prestados']}</p>"
            f"<p><b>Disponibles para préstamo:</b> {libro['disponibles']}</p>"
        )

    def _solicitar_prestamo(self):
        """Envía el ISBN del libro visible en la ficha a la página de préstamos."""
        isbn = self._isbn_seleccionado()
        if isbn:
            self.prestamo_solicitado.emit(isbn)

    def _solicitar_edicion(self):
        """Pide editar el libro seleccionado."""
        isbn = self._isbn_seleccionado()
        if isbn:
            self.edicion_solicitada.emit(isbn)

    def _solicitar_eliminacion(self):
        """Pide eliminar el libro seleccionado."""
        isbn = self._isbn_seleccionado()
        if isbn:
            self.eliminacion_solicitada.emit(isbn)

    def limpiar(self):
        """Restablece todos los filtros y vuelve a mostrar el catálogo completo."""
        self.buscarLineEdit.clear()
        self.campoComboBox.setCurrentIndex(0)
        self.categoriaComboBox.setCurrentIndex(0)
        self.ordenarComboBox.setCurrentIndex(0)
        self.soloDisponiblesCheckBox.setChecked(False)
        self.buscar()
        self.buscarLineEdit.setFocus()

    def showEvent(self, evento):
        """Refresca el catálogo cada vez que se muestra la página."""
        super().showEvent(evento)
        self.buscar()
