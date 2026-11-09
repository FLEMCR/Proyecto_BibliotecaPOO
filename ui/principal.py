"""Panel principal del sistema de biblioteca."""

import html
import os
from collections import Counter
from datetime import date
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QTableWidgetItem

from core import configuracion, libros
from ui.catalogo import VentanaCatalogo


class VentanaPrincipal(QMainWindow):
    """Reúne el resumen, el catálogo, la membresía y las vistas de administración."""

    sesion_cerrada = pyqtSignal()

    def __init__(self, biblioteca, usuario, parent=None):
        super().__init__(parent)
        uic.loadUi(str(Path(__file__).with_suffix(".ui")), self)
        self.biblioteca = biblioteca
        self.usuario = usuario
        self.es_admin = usuario.puede_administrar()
        self._cerrando_por_sesion = False

        self.catalogo = VentanaCatalogo(self.biblioteca, self)
        self.catalogoContenedor.layout().addWidget(self.catalogo)

        self._configurar_marca()
        self._configurar_usuario()
        self._configurar_navegacion()
        self._cargar_inicio()
        self._cargar_membresia()
        self._cargar_usuarios()
        self._cargar_reporte()

    def _configurar_marca(self):
        self.setWindowTitle(
            f"{configuracion.NOMBRE_BIBLIOTECA} | Panel principal"
        )
        self.marcaLabel.setText(configuracion.NOMBRE_BIBLIOTECA)
        self.marcaLabel.setWordWrap(True)
        self.marcaSubtituloLabel.setText(configuracion.LEMA)
        self.marcaSubtituloLabel.setWordWrap(True)

    def _configurar_usuario(self):
        self.bienvenidaLabel.setText(f"Hola, {self.usuario.nombre()}")
        self.tipoLabel.setText(
            f"{self.usuario.tipo()} · {self.usuario.estado()}"
        )
        if self.es_admin:
            self.avisoTextoLabel.setText(
                "Como administrador puedes consultar el catálogo, revisar tu "
                "membresía, ver a todos los usuarios y generar reportes."
            )
        else:
            self.avisoTextoLabel.setText(
                "Usa el catálogo para buscar por ISBN, título, autor o categoría. "
                "En Mi membresía puedes revisar tu vencimiento y tus beneficios."
            )

    def _configurar_navegacion(self):
        if not self.es_admin:
            self.navegacionListWidget.item(3).setHidden(True)
            self.navegacionListWidget.item(4).setHidden(True)
        self.navegacionListWidget.currentRowChanged.connect(self._cambiar_pagina)
        self.cerrarSesionButton.clicked.connect(self.cerrar_sesion)
        self.irCatalogoButton.clicked.connect(
            lambda: self.navegacionListWidget.setCurrentRow(1)
        )
        self.irMembresiaButton.clicked.connect(
            lambda: self.navegacionListWidget.setCurrentRow(2)
        )
        self.buscarUsuarioButton.clicked.connect(self._filtrar_usuarios)
        self.buscarUsuarioLineEdit.returnPressed.connect(self._filtrar_usuarios)
        self.actualizarReporteButton.clicked.connect(self._cargar_reporte)
        self.exportarReporteButton.clicked.connect(self._exportar_reporte)
        self.navegacionListWidget.setCurrentRow(0)

    def _cambiar_pagina(self, fila):
        if fila < 0:
            return
        if fila in (3, 4) and not self.es_admin:
            return
        self.paginasStackedWidget.setCurrentIndex(fila)
        if fila == 1:
            self.catalogo.buscar()
        elif fila == 2:
            self._cargar_membresia()
        elif fila == 3:
            self._cargar_usuarios()
        elif fila == 4:
            self._cargar_reporte()

    def _cargar_inicio(self):
        resumen = self.biblioteca.resumen()
        self.titulosValorLabel.setText(str(resumen["titulos"]))
        self.ejemplaresValorLabel.setText(str(resumen["ejemplares"]))
        self.disponiblesValorLabel.setText(str(resumen["disponibles"]))
        self.prestadosValorLabel.setText(str(resumen["prestados"]))
        self.usuariosValorLabel.setText(str(resumen["usuarios"]))
        self.statusBar().showMessage(
            f"Datos actualizados al {resumen['fecha_de_hoy']}"
        )

    def _cargar_membresia(self):
        datos = self.usuario.datos_de_membresia()
        self.nombreValorLabel.setText(datos["nombre"])
        self.dniValorLabel.setText(datos["dni"])
        self.tipoValorLabel.setText(datos["tipo"])
        self.vencimientoValorLabel.setText(datos["vencimiento_membresia"])
        self.estadoValorLabel.setText(datos["estado"])
        self.permisosValorLabel.setText(
            "Administrador" if self.es_admin else "Consulta y préstamo"
        )
        self.beneficiosLabel.setText(
            "Hasta "
            f"{configuracion.MAXIMO_PRESTAMOS_POR_USUARIO} préstamos simultáneos, "
            f"{configuracion.DIAS_DE_PRESTAMO} días por préstamo y renovación "
            "sujeta a disponibilidad."
        )

    def _cargar_usuarios(self):
        if not self.es_admin:
            return
        self._filtrar_usuarios()

    def _filtrar_usuarios(self):
        if not self.es_admin:
            return
        buscado = libros.normalizar_texto(self.buscarUsuarioLineEdit.text())
        datos = []
        for usuario in self.biblioteca.datos_de_los_usuarios():
            texto = " ".join(
                [
                    str(usuario["dni"]),
                    str(usuario["nombre"]),
                    str(usuario["tipo"]),
                    str(usuario["estado"]),
                ]
            )
            if buscado in libros.normalizar_texto(texto):
                datos.append(usuario)

        self.tablaUsuarios.setSortingEnabled(False)
        self.tablaUsuarios.clearContents()
        self.tablaUsuarios.setRowCount(len(datos))
        for fila, usuario in enumerate(datos):
            valores = [
                usuario["dni"],
                usuario["nombre"],
                usuario["tipo"],
                usuario["vencimiento_membresia"],
                usuario["estado"],
                usuario.get("puede_administrar", "No"),
            ]
            for columna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))
                if columna in (0, 3, 5):
                    item.setTextAlignment(Qt.AlignCenter)
                self.tablaUsuarios.setItem(fila, columna, item)
        self.tablaUsuarios.setSortingEnabled(True)
        self.cantidadUsuariosLabel.setText(
            f"{len(datos)} usuario(s) encontrado(s)"
        )

    def _cargar_reporte(self):
        if not self.es_admin:
            return
        resumen = self.biblioteca.resumen()
        por_seccion = {}
        por_categoria = Counter()
        for libro in self.biblioteca.todos_los_libros():
            seccion = libro.seccion()
            if seccion not in por_seccion:
                por_seccion[seccion] = {
                    "nombre": configuracion.SECCIONES.get(seccion, seccion),
                    "titulos": 0,
                    "ejemplares": 0,
                    "disponibles": 0,
                    "prestados": 0,
                }
            datos = por_seccion[seccion]
            datos["titulos"] += 1
            datos["ejemplares"] += libro.ejemplares()
            datos["disponibles"] += libro.disponibles()
            datos["prestados"] += libro.prestados()
            por_categoria[libro.categoria()] += 1

        filas_seccion = ""
        for seccion in sorted(por_seccion):
            datos = por_seccion[seccion]
            filas_seccion += (
                "<tr>"
                f"<td><b>{html.escape(seccion)}</b> · {html.escape(datos['nombre'])}</td>"
                f"<td align='center'>{datos['titulos']}</td>"
                f"<td align='center'>{datos['ejemplares']}</td>"
                f"<td align='center'>{datos['disponibles']}</td>"
                f"<td align='center'>{datos['prestados']}</td>"
                "</tr>"
            )
        filas_categoria = ""
        for categoria, cantidad in sorted(por_categoria.items()):
            filas_categoria += (
                "<tr>"
                f"<td>{html.escape(categoria)}</td>"
                f"<td align='center'>{cantidad}</td>"
                "</tr>"
            )

        self.reporteTextEdit.setHtml(
            f"""
            <div style="font-family:'Segoe UI'; color:#1f2937;">
              <h2 style="margin:0; color:#111827;">Reporte general de la biblioteca</h2>
              <p style="color:#6b7280; margin:4px 0 18px 0;">
                Fecha del reporte: {resumen['fecha_de_hoy']}
              </p>
              <table cellspacing="0" cellpadding="8" width="100%">
                <tr style="background:#eff6ff; color:#1d4ed8;">
                  <td><b>Títulos</b></td><td><b>Ejemplares</b></td>
                  <td><b>Disponibles</b></td><td><b>Prestados</b></td>
                  <td><b>Usuarios</b></td>
                </tr>
                <tr align="center">
                  <td>{resumen['titulos']}</td><td>{resumen['ejemplares']}</td>
                  <td>{resumen['disponibles']}</td><td>{resumen['prestados']}</td>
                  <td>{resumen['usuarios']}</td>
                </tr>
              </table>
              <h3 style="margin-top:22px; color:#111827;">Disponibilidad por sección</h3>
              <table cellspacing="0" cellpadding="6" width="100%">
                <tr style="background:#f3f4f6;">
                  <td><b>Sección</b></td><td><b>Títulos</b></td>
                  <td><b>Ejemplares</b></td><td><b>Disponibles</b></td>
                  <td><b>Prestados</b></td>
                </tr>
                {filas_seccion}
              </table>
              <h3 style="margin-top:22px; color:#111827;">Títulos por categoría</h3>
              <table cellspacing="0" cellpadding="6" width="100%">
                <tr style="background:#f3f4f6;">
                  <td><b>Categoría</b></td><td><b>Títulos</b></td>
                </tr>
                {filas_categoria}
              </table>
              <p style="margin-top:18px; color:#6b7280; font-size:12px;">
                Reporte generado automáticamente con los datos actuales del catálogo.
              </p>
            </div>
            """
        )
        self.statusBar().showMessage("Reporte actualizado")

    def _exportar_reporte(self):
        if not self.es_admin:
            return
        os.makedirs(configuracion.CARPETA_REPORTES, exist_ok=True)
        nombre = f"reporte_{date.today().isoformat()}.txt"
        ruta_sugerida = os.path.join(configuracion.CARPETA_REPORTES, nombre)
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar reporte",
            ruta_sugerida,
            "Archivos de texto (*.txt);;Todos los archivos (*)",
        )
        if not ruta:
            return
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("REPORTE GENERAL DE LA BIBLIOTECA\n")
                archivo.write("=" * 60 + "\n\n")
                archivo.write(self.reporteTextEdit.toPlainText())
        except OSError as error:
            QMessageBox.critical(
                self, "No se pudo guardar", f"No se pudo escribir el archivo:\n{error}"
            )
            return
        self.statusBar().showMessage(f"Reporte guardado en {ruta}", 6000)
        QMessageBox.information(
            self, "Reporte guardado", f"El reporte se guardó correctamente en:\n{ruta}"
        )

    def cerrar_sesion(self):
        respuesta = QMessageBox.question(
            self,
            "Cerrar sesión",
            "¿Deseas cerrar la sesión y volver a la pantalla de acceso?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if respuesta == QMessageBox.Yes:
            self._cerrando_por_sesion = True
            self.sesion_cerrada.emit()
            self.close()

    def closeEvent(self, evento):
        if self._cerrando_por_sesion:
            evento.accept()
            return
        respuesta = QMessageBox.question(
            self,
            "Cerrar la aplicación",
            "¿Deseas cerrar sesión y salir del panel?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if respuesta == QMessageBox.Yes:
            self._cerrando_por_sesion = True
            self.sesion_cerrada.emit()
            evento.accept()
        else:
            evento.ignore()
