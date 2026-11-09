"""Pantalla de catálogo con buscador por ISBN, título, autor y categoría."""

import html
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QSizePolicy,
    QTableWidgetItem,
    QWidget,
)


class VentanaCatalogo(QWidget):
    """Muestra la tabla del catálogo y la ficha formateada del libro elegido."""

    COLUMNAS = [
        "ISBN",
        "Título",
        "Autor",
        "Categoría",
        "Disponibles",
        "Estado",
    ]
    CAMPOS = [
        ("Todo el catálogo", "Todo"),
        ("ISBN", "ISBN"),
        ("Título", "titulo"),
        ("Autor", "autor"),
        ("Categoría", "categoria"),
    ]
    ORDENES = [
        ("Título (A-Z)", "titulo"),
        ("Autor (A-Z)", "autor"),
        ("Categoría (A-Z)", "categoria"),
        ("Más disponibles", "disponibles"),
    ]

    def __init__(self, biblioteca, parent=None):
        super().__init__(parent)
        uic.loadUi(str(Path(__file__).with_suffix(".ui")), self)
        self.biblioteca = biblioteca
        self._configurar_tabla()
        self._preparar_filtros()
        self._conectar_senales()
        self.layoutCatalogo.setStretch(0, 0)
        self.layoutCatalogo.setStretch(1, 0)
        self.layoutCatalogo.setStretch(2, 1)
        self.cantidadLibrosLabel.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Fixed
        )
        self.filtrosFrame.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed
        )
        self.splitterCatalogo.setStretchFactor(0, 1)
        self.splitterCatalogo.setStretchFactor(1, 0)
        self.buscar()

    def _configurar_tabla(self):
        self.tablaLibros.setColumnCount(len(self.COLUMNAS))
        self.tablaLibros.setHorizontalHeaderLabels(self.COLUMNAS)
        self.tablaLibros.verticalHeader().setVisible(False)
        self.tablaLibros.setShowGrid(False)
        self.tablaLibros.setWordWrap(False)
        self.tablaLibros.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablaLibros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaLibros.setEditTriggers(QAbstractItemView.NoEditTriggers)
        cabecera = self.tablaLibros.horizontalHeader()
        fuente = self.tablaLibros.font()
        fuente.setPointSize(9)
        self.tablaLibros.setFont(fuente)
        cabecera.setFont(fuente)
        cabecera.setSectionResizeMode(QHeaderView.Interactive)
        for columna, ancho in {
            0: 105,
            3: 95,
            4: 92,
            5: 90,
        }.items():
            self.tablaLibros.setColumnWidth(columna, ancho)
        cabecera.setSectionResizeMode(1, QHeaderView.Stretch)
        cabecera.setSectionResizeMode(2, QHeaderView.Stretch)

    def _preparar_filtros(self):
        for texto, valor in self.CAMPOS:
            self.campoComboBox.addItem(texto, valor)
        self.categoriaComboBox.addItem("Todas las categorías", "")
        for categoria in self.biblioteca.categorias():
            self.categoriaComboBox.addItem(categoria, categoria)
        for texto, valor in self.ORDENES:
            self.ordenarComboBox.addItem(texto, valor)
        self.limiteSpinBox.setValue(100)

    def _conectar_senales(self):
        self.buscarButton.clicked.connect(self.buscar)
        self.buscarLineEdit.returnPressed.connect(self.buscar)
        self.limpiarButton.clicked.connect(self.limpiar_filtros)
        self.campoComboBox.currentIndexChanged.connect(self.buscar)
        self.categoriaComboBox.currentIndexChanged.connect(self.buscar)
        self.ordenarComboBox.currentIndexChanged.connect(self.buscar)
        self.soloDisponiblesCheckBox.stateChanged.connect(self.buscar)
        self.limiteSpinBox.valueChanged.connect(self.buscar)
        self.tablaLibros.itemSelectionChanged.connect(self.mostrar_detalle)

    def buscar(self):
        """Toma los filtros de la pantalla y pide los resultados a la biblioteca."""
        texto = self.buscarLineEdit.text().strip()
        campo = self.campoComboBox.currentData() or "Todo"
        categoria = self.categoriaComboBox.currentData() or ""
        solo_disponibles = self.soloDisponiblesCheckBox.isChecked()
        ordenar_por = self.ordenarComboBox.currentData() or "titulo"
        limite = self.limiteSpinBox.value()

        datos = self.biblioteca.buscar_avanzado(
            texto=texto,
            campo=campo,
            categoria=categoria,
            solo_disponibles=solo_disponibles,
            ordenar_por=ordenar_por,
            limite=limite,
        )
        self._llenar_tabla(datos)
        return datos

    def limpiar_filtros(self):
        """Devuelve todos los filtros a su estado inicial y muestra el catálogo."""
        widgets = [
            self.buscarLineEdit,
            self.campoComboBox,
            self.categoriaComboBox,
            self.ordenarComboBox,
            self.soloDisponiblesCheckBox,
            self.limiteSpinBox,
        ]
        for widget in widgets:
            widget.blockSignals(True)
        self.buscarLineEdit.clear()
        self.campoComboBox.setCurrentIndex(0)
        self.categoriaComboBox.setCurrentIndex(0)
        self.ordenarComboBox.setCurrentIndex(0)
        self.soloDisponiblesCheckBox.setChecked(False)
        self.limiteSpinBox.setValue(100)
        for widget in widgets:
            widget.blockSignals(False)
        self.buscar()
        self.buscarLineEdit.setFocus()

    def _llenar_tabla(self, datos):
        self.tablaLibros.setSortingEnabled(False)
        self.tablaLibros.clearContents()
        self.tablaLibros.setRowCount(len(datos))
        for fila, libro in enumerate(datos):
            estado, color_estado = self._estado_del_libro(libro)
            valores = [
                libro["isbn"],
                libro["titulo"],
                libro["autor"],
                libro["categoria"],
                libro["disponibles"],
                estado,
            ]
            for columna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))
                item.setToolTip(str(valor))
                if columna == 0:
                    item.setData(Qt.UserRole, libro)
                if columna == 4:
                    item.setTextAlignment(Qt.AlignCenter)
                if columna == 5:
                    item.setForeground(QColor(color_estado))
                self.tablaLibros.setItem(fila, columna, item)
        self.tablaLibros.setSortingEnabled(True)
        self.tablaLibros.sortItems(1, Qt.AscendingOrder)
        self.cantidadLibrosLabel.setText(
            f"{len(datos)} libro(s) encontrado(s)"
        )
        if datos:
            self.tablaLibros.selectRow(0)
            self.mostrar_detalle()
        else:
            self.mostrar_sin_resultados()

    def _estado_del_libro(self, libro):
        if libro["disponibles"] <= 0:
            return "Sin ejemplares", "#b91c1c"
        if libro["se_puede_prestar"] == "Si":
            return "Disponible", "#15803d"
        return "Solo consulta", "#b45309"

    def mostrar_sin_resultados(self):
        self.detalleTextEdit.setHtml(
            """
            <div style="font-family:'Segoe UI'; color:#6b7280; padding:18px;">
              <h3 style="color:#374151;">No se encontraron libros</h3>
              <p>Prueba con otro texto, cambia la categoría o pulsa
              <b>Limpiar</b> para ver todo el catálogo.</p>
            </div>
            """
        )

    def mostrar_detalle(self):
        """Pinta la ficha del libro seleccionado en el panel derecho."""
        filas = self.tablaLibros.selectionModel().selectedRows()
        if not filas:
            return
        item = self.tablaLibros.item(filas[0].row(), 0)
        if item is None:
            return
        libro = item.data(Qt.UserRole)
        if not libro:
            return
        self.detalleTextEdit.setHtml(self._html_del_libro(libro))

    def _html_del_libro(self, libro):
        estado, color_estado = self._estado_del_libro(libro)
        titulo = html.escape(str(libro["titulo"]))
        autor = html.escape(str(libro["autor"]))
        categoria = html.escape(str(libro["categoria"]))
        seccion_nombre = html.escape(str(libro["seccion_nombre"]))
        isbn = html.escape(str(libro["isbn"]))
        return f"""
        <div style="font-family:'Segoe UI'; color:#1f2937; font-size:13px;">
          <h2 style="margin:0 0 2px 0; font-size:16px; color:#111827;">{titulo}</h2>
          <p style="margin:0 0 12px 0; color:#6b7280;">{autor}</p>
          <table cellspacing="0" cellpadding="4" width="100%">
            <tr><td style="color:#6b7280; width:34%;">ISBN</td>
                <td style="white-space:nowrap;"><b>{isbn}</b></td></tr>
            <tr><td style="color:#6b7280;">Categoría</td>
                <td>{categoria}</td></tr>
            <tr><td style="color:#6b7280;">Ubicación</td>
                <td>Sección {libro['seccion']} · {seccion_nombre} · Estante {libro['estante']}</td></tr>
            <tr><td style="color:#6b7280;">Ejemplares</td>
                <td>{libro['ejemplares']}</td></tr>
            <tr><td style="color:#6b7280;">Disponibles</td>
                <td><b>{libro['disponibles']}</b></td></tr>
            <tr><td style="color:#6b7280;">Prestados</td>
                <td>{libro['prestados']}</td></tr>
          </table>
          <p style="margin-top:14px; padding:8px 10px; background:#eff6ff;
                    border-radius:8px; color:#1d4ed8;">
            <b>Estado:</b> <span style="color:{color_estado};">{estado}</span>
          </p>
          <p style="margin-top:8px; color:#6b7280; font-size:12px;">
            Selecciona otra fila de la tabla para ver su ficha.
          </p>
        </div>
        """
