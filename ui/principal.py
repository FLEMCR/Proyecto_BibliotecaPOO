from pathlib import Path

from core import configuracion
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
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
        self._cargar_resumen()
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

    def _refrescar_datos(self):
        """Actualiza el resumen, el catálogo y los formularios después de un cambio."""
        self._cargar_resumen()
        self.catalogo.buscar()
        self.pagina_prestamo.actualizar()
        self.pagina_devolucion.actualizar()

    def _configurar_navegacion(self):
        """Oculta las páginas de administración y conecta el menú lateral."""
        if not self.usuario.puede_administrar():
            for fila in FILAS_DE_ADMINISTRACION:
                self.navegacionListWidget.item(fila).setHidden(True)

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

    def _volver_a_la_fila_actual(self):
        """Restaura la selección del menú cuando se intenta abrir una página prohibida."""
        self.navegacionListWidget.blockSignals(True)
        self.navegacionListWidget.setCurrentRow(
            self.paginasStackedWidget.currentIndex()
        )
        self.navegacionListWidget.blockSignals(False)

    def _cargar_resumen(self):
        """Muestra los totales de la biblioteca en las tarjetas de inicio."""
        datos = self.biblioteca.resumen()
        self.titulosValorLabel.setText(str(datos["titulos"]))
        self.ejemplaresValorLabel.setText(str(datos["ejemplares"]))
        self.disponiblesValorLabel.setText(str(datos["disponibles"]))
        self.prestadosValorLabel.setText(str(datos["prestados"]))
        self.usuariosValorLabel.setText(str(datos["usuarios"]))

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
