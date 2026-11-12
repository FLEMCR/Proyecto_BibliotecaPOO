import sys

from core import configuracion, errores
from core.biblioteca import Biblioteca
from PyQt5.QtWidgets import QApplication, QMessageBox
from ui.acceso import VentanaAcceso
from ui.principal import VentanaPrincipal


def cargar_estilos(aplicacion):
    """Carga la hoja de estilos QSS del proyecto en la aplicación."""
    try:
        with open(configuracion.ARCHIVO_ESTILOS, "r", encoding="utf-8") as archivo:
            aplicacion.setStyleSheet(archivo.read())
    except OSError as error:
        print(f"No se pudo cargar el estilo: {error}", file=sys.stderr)


class AplicacionBiblioteca:
    """Coordina el acceso, el panel principal y el cierre de sesión."""

    def __init__(self):
        self.biblioteca = Biblioteca()
        self.acceso = VentanaAcceso(self.biblioteca)
        self.ventana_principal = None
        self.acceso.usuario_autenticado.connect(self.abrir_panel)
        self.acceso.rejected.connect(self.cerrar_aplicacion)

    def iniciar(self):
        """Muestra la ventana de acceso."""
        self.acceso.show()

    def abrir_panel(self, usuario):
        """Crea y muestra el panel principal para el usuario autenticado."""
        self.ventana_principal = VentanaPrincipal(self.biblioteca, usuario)
        self.ventana_principal.sesion_cerrada.connect(self.volver_al_acceso)
        self.ventana_principal.show()
        self.acceso.hide()

    def volver_al_acceso(self):
        """Destruye el panel y vuelve a mostrar la pantalla de acceso."""
        if self.ventana_principal is not None:
            self.ventana_principal.deleteLater()
            self.ventana_principal = None
        self.acceso.limpiar()
        self.acceso.show()
        self.acceso.raise_()
        self.acceso.activateWindow()

    def cerrar_aplicacion(self):
        """Sale de la aplicación solicitando QApplication.quit()."""
        aplicacion = QApplication.instance()
        if aplicacion is not None:
            aplicacion.quit()


def main():
    """Punto de entrada principal del sistema gráfico."""
    aplicacion = QApplication(sys.argv)
    aplicacion.setApplicationName(configuracion.NOMBRE_BIBLIOTECA)
    cargar_estilos(aplicacion)

    try:
        controlador = AplicacionBiblioteca()
    except errores.ErrorBiblioteca as error:
        QMessageBox.critical(
            None,
            "No se pudo iniciar la biblioteca",
            str(error),
        )
        return 1

    controlador.iniciar()
    return aplicacion.exec_()


if __name__ == "__main__":
    sys.exit(main())
