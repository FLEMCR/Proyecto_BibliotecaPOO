from pathlib import Path

from core import configuracion, errores, reportes, utilidades
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from ui.catalogo import VentanaCatalogo
from ui.devolucion import VentanaDevolucion
from ui.libro_form import VentanaLibro
from ui.prestamo import VentanaPrestamo

ruta_ui = Path(__file__).resolve().parent / "principal.ui"

FILA_INICIO = 0
FILA_CATALOGO = 1
FILA_PRESTAMO = 2
FILA_DEVOLUCION = 3
FILA_MEMBRESIA = 4
FILA_LIBRO = 5
FILA_USUARIOS = 6
FILA_REPORTES = 7

FILAS_DE_ADMINISTRACION = (FILA_LIBRO, FILA_USUARIOS, FILA_REPORTES)


class VentanaPrincipal(QMainWindow):
    sesion_cerrada = pyqtSignal()

    def __init__(self, biblioteca, usuario):
        super().__init__()
        uic.loadUi(str(ruta_ui), self)
        self.biblioteca = biblioteca
        self.usuario = usuario

        self._configurar_marca()
        self._configurar_usuario()
        self._incrustar_paginas()
        self._conectar_acciones()
        self._cargar_membresia()
        self._configurar_navegacion()
        self.cerrarSesionButton.clicked.connect(self.cerrar_sesion)

    def _configurar_marca(self):
        """Carga el nombre y el lema de la biblioteca desde la configuración."""
        self.setWindowTitle(configuracion.NOMBRE_BIBLIOTECA)
        self.marca1Label.setText(configuracion.NOMBRE_BIBLIOTECA)
        self.marca2Label.setText(configuracion.LEMA)

    def _configurar_usuario(self):
        """Muestra el nombre, el tipo y el estado del usuario conectado."""
        self.bienvenidaLabel.setText(f"Hola, {self.usuario.nombre()}")
        self.tipoLabel.setText(f"{self.usuario.tipo()} · {self.usuario.estado()}")

    def _incrustar_paginas(self):
        """Coloca el catálogo y los formularios dentro de la ventana principal."""
        self.catalogo = VentanaCatalogo(self.biblioteca, self.usuario)
        self.layoutCatalogoContenedor.addWidget(self.catalogo)

        self.pagina_prestamo = VentanaPrestamo(self.biblioteca, self.usuario)
        self.layoutPaginaPrestamo.addWidget(
            self.pagina_prestamo, 0, Qt.AlignHCenter
        )
        self.pagina_prestamo.datos_actualizados.connect(self._refrescar_datos)

        self.pagina_devolucion = VentanaDevolucion(self.biblioteca, self.usuario)
        self.layoutPaginaDevolucion.addWidget(
            self.pagina_devolucion, 0, Qt.AlignHCenter
        )
        self.pagina_devolucion.datos_actualizados.connect(self._refrescar_datos)

        self.pagina_libro = None
        if self.usuario.puede_administrar():
            self.pagina_libro = VentanaLibro(self.biblioteca, self.usuario)
            self.layoutPaginaLibro.addWidget(
                self.pagina_libro, 0, Qt.AlignHCenter
            )
            self.pagina_libro.datos_actualizados.connect(self._refrescar_datos)

    def _conectar_acciones(self):
        """Conecta los accesos entre páginas y las acciones de administración."""
        self.catalogo.prestamo_solicitado.connect(self._abrir_prestamo_con_isbn)
        self.catalogo.libro_nuevo_solicitado.connect(self._nuevo_libro)
        self.catalogo.edicion_solicitada.connect(self._editar_libro)
        self.catalogo.eliminacion_solicitada.connect(self._eliminar_libro)
        self.buscarUsuarioButton.clicked.connect(self._cargar_usuarios)
        self.buscarUsuarioLineEdit.returnPressed.connect(self._cargar_usuarios)
        self.renovarMembresiaButton.clicked.connect(self._renovar_membresia)
        self.exportarReporteButton.clicked.connect(self._exportar_reporte)

    def _refrescar_datos(self):
        """Actualiza el catálogo, los formularios y los reportes después de un cambio."""
        self.catalogo.buscar()
        self.pagina_prestamo.actualizar()
        self.pagina_devolucion.actualizar()
        if self.usuario.puede_administrar():
            self._cargar_usuarios()
            self._cargar_reporte()

    def _abrir_prestamo_con_isbn(self, isbn):
        """Va a la página de préstamos con el ISBN del libro elegido en el catálogo."""
        self.navegacionListWidget.setCurrentRow(FILA_PRESTAMO)
        self.pagina_prestamo.cargar_isbn(isbn)

    def _nuevo_libro(self):
        """Abre el formulario de libros en blanco para registrar uno nuevo."""
        if not self.usuario.puede_administrar() or self.pagina_libro is None:
            return
        self.pagina_libro.limpiar()
        self.navegacionListWidget.setCurrentRow(FILA_LIBRO)

    def _editar_libro(self, isbn):
        """Abre el formulario de libros con los datos del libro elegido."""
        if not self.usuario.puede_administrar() or self.pagina_libro is None:
            return
        self.pagina_libro.cargar_libro(isbn)
        self.navegacionListWidget.setCurrentRow(FILA_LIBRO)

    def _eliminar_libro(self, isbn):
        """Quita del catálogo el libro elegido si no tiene préstamos activos."""
        if not self.usuario.puede_administrar():
            return
        try:
            libro = self.biblioteca.eliminar_libro(isbn)
        except errores.ErrorBiblioteca as error:
            QMessageBox.warning(self, "No se pudo eliminar", str(error))
            return
        QMessageBox.information(
            self, "Libro eliminado", f"Se eliminó: {libro.titulo()}."
        )
        self._refrescar_datos()

    def _cargar_usuarios(self):
        """Muestra los usuarios y aplica el filtro por DNI, nombre o tipo."""
        texto = utilidades.normalizar_texto(self.buscarUsuarioLineEdit.text())
        usuarios = []
        for usuario in self.biblioteca.todos_los_usuarios():
            datos = usuario.datos_de_membresia()
            campos = (datos["dni"], datos["nombre"], datos["tipo"])
            if texto and not any(texto in utilidades.normalizar_texto(campo) for campo in campos):
                continue
            usuarios.append((usuario, datos))

        self.tablaUsuarios.setSortingEnabled(False)
        self.tablaUsuarios.setRowCount(0)
        for fila, (usuario, datos) in enumerate(usuarios):
            valores = [
                datos["dni"],
                datos["nombre"],
                datos["tipo"],
                datos["vencimiento_membresia"],
                datos["estado"],
                "Sí" if usuario.puede_administrar() else "No",
            ]
            self.tablaUsuarios.insertRow(fila)
            for columna, valor in enumerate(valores):
                self.tablaUsuarios.setItem(fila, columna, QTableWidgetItem(valor))
        self.tablaUsuarios.setSortingEnabled(True)
        self.cantidadUsuariosLabel.setText(f"{len(usuarios)} usuarios")

    def _renovar_membresia(self):
        """Renueva por 3 meses la membresía del usuario seleccionado."""
        if not self.usuario.puede_administrar():
            return
        fila = self.tablaUsuarios.currentRow()
        if fila < 0:
            QMessageBox.information(
                self, "Renovar membresía", "Selecciona un usuario de la tabla."
            )
            return
        dni = self.tablaUsuarios.item(fila, 0).text()
        usuario = self.biblioteca.renovar_membresia(dni)
        QMessageBox.information(
            self,
            "Membresía renovada",
            f"Nuevo vencimiento de {usuario.nombre()}: "
            f"{usuario.vencimiento_membresia()}",
        )
        self._cargar_usuarios()
        if dni == self.usuario.dni():
            self._cargar_membresia()

    def _cargar_reporte(self):
        """Muestra el resumen, el historial de préstamos y el inventario."""
        self.reporteResumenLabel.setText(reportes.resumen_visible(self.biblioteca))
        self._llenar_tabla(
            self.tablaHistorialPrestamos,
            reportes.CABECERAS_HISTORIAL,
            reportes.historial_de_prestamos(self.biblioteca),
        )
        self._llenar_tabla(
            self.tablaInventarioLibros,
            reportes.CABECERAS_INVENTARIO,
            reportes.inventario_de_libros(self.biblioteca),
        )

    def _llenar_tabla(self, tabla, cabeceras, filas):
        """Carga una tabla de solo lectura con las filas que entrega el reporte."""
        tabla.setSortingEnabled(False)
        tabla.setRowCount(0)
        for fila, valores in enumerate(filas):
            tabla.insertRow(fila)
            for columna, valor in enumerate(valores):
                tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setStretchLastSection(True)
        tabla.setSortingEnabled(True)

    def _exportar_reporte(self):
        """Guarda el reporte completo en data/reporte.txt y avisa al usuario."""
        ruta, _ = reportes.exportar(self.biblioteca, "Sección")
        QMessageBox.information(
            self, "Reporte exportado", f"El reporte se guardó en:\n{ruta}"
        )

    def _configurar_navegacion(self):
        """Oculta las páginas de administración y conecta el menú lateral."""
        if not self.usuario.puede_administrar():
            for fila in FILAS_DE_ADMINISTRACION:
                self.navegacionListWidget.item(fila).setHidden(True)

        self.renovarMembresiaButton.setVisible(self.usuario.puede_administrar())
        self.navegacionListWidget.currentRowChanged.connect(self._cambiar_pagina)
        self.navegacionListWidget.setCurrentRow(FILA_INICIO)

    def _cambiar_pagina(self, fila):
        """Cambia la página visible y actualiza sus datos cuando corresponde."""
        if fila < 0:
            return
        if fila in FILAS_DE_ADMINISTRACION and not self.usuario.puede_administrar():
            self._volver_a_la_fila_actual()
            return

        self.paginasStackedWidget.setCurrentIndex(fila)
        if fila == FILA_CATALOGO:
            self.catalogo.buscar()
        elif fila == FILA_PRESTAMO:
            self.pagina_prestamo.actualizar()
        elif fila == FILA_DEVOLUCION:
            self.pagina_devolucion.actualizar()
        elif fila == FILA_MEMBRESIA:
            self._cargar_membresia()
        elif fila == FILA_USUARIOS:
            self._cargar_usuarios()
        elif fila == FILA_REPORTES:
            self._cargar_reporte()

    def _volver_a_la_fila_actual(self):
        """Restaura la selección del menú cuando se intenta abrir una página prohibida."""
        self.navegacionListWidget.blockSignals(True)
        self.navegacionListWidget.setCurrentRow(
            self.paginasStackedWidget.currentIndex()
        )
        self.navegacionListWidget.blockSignals(False)

    def _cargar_membresia(self):
        """Muestra los datos de la membresía del usuario conectado."""
        datos = self.usuario.datos_de_membresia()
        self.nombreValorLabel.setText(datos["nombre"])
        self.dniValorLabel.setText(datos["dni"])
        self.tipoValorLabel.setText(datos["tipo"])
        self.vencimientoValorLabel.setText(datos["vencimiento_membresia"])
        self.estadoValorLabel.setText(datos["estado"])
        self.permisosValorLabel.setText(
            "Administrador" if self.usuario.puede_administrar() else "Consulta y préstamo"
        )

    def cerrar_sesion(self):
        """Avisa al controlador para que vuelva a la pantalla de acceso."""
        self.sesion_cerrada.emit()
