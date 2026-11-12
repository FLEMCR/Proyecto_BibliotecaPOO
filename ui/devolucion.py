from datetime import date
from pathlib import Path

from core import errores
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

ruta_ui = Path(__file__).resolve().parent / "devolucion.ui"


class VentanaDevolucion(QWidget):
    """Página para devolver uno de los préstamos activos del usuario conectado."""

    datos_actualizados = pyqtSignal()

    def __init__(self, biblioteca, usuario, parent=None):
        super().__init__(parent)
        uic.loadUi(str(ruta_ui), self)
        self.biblioteca = biblioteca
        self.usuario = usuario
        self._prestamos_activos = []

        self.prestamoComboBox.currentIndexChanged.connect(self._mostrar_detalle)
        self.devolverButton.clicked.connect(self.devolver)
        self.cancelarButton.clicked.connect(self.actualizar)
        self.actualizar()

    def actualizar(self):
        """Recarga los préstamos activos del usuario conectado."""
        self.usuarioLabel.setText(
            f"{self.usuario.nombre()} · DNI {self.usuario.dni()}"
        )
        self._prestamos_activos = [
            prestamo
            for prestamo in self.biblioteca.prestamos_de_usuario(self.usuario.dni())
            if prestamo.esta_activo()
        ]

        self.prestamoComboBox.blockSignals(True)
        self.prestamoComboBox.clear()
        for prestamo in self._prestamos_activos:
            self.prestamoComboBox.addItem(
                f"{self._titulo_del_prestamo(prestamo)} — ISBN {prestamo.isbn()}",
                prestamo.isbn(),
            )
        if len(self._prestamos_activos) == 0:
            self.prestamoComboBox.addItem("Sin préstamos activos", None)
        self.prestamoComboBox.blockSignals(False)

        self.devolverButton.setEnabled(len(self._prestamos_activos) > 0)
        if len(self._prestamos_activos) == 0:
            self._limpiar_detalle()
            self._mensaje("No tienes préstamos activos para devolver.")
            return

        self._mostrar_detalle()
        self._mensaje("Selecciona un préstamo para ver los detalles antes de devolverlo.")

    def _titulo_del_prestamo(self, prestamo):
        """Devuelve el título del libro de un préstamo o su ISBN si no existe."""
        try:
            return self.biblioteca.libro(prestamo.isbn()).titulo()
        except errores.ErrorBiblioteca:
            return prestamo.isbn()

    def _prestamo_seleccionado(self):
        """Retorna el préstamo elegido en el combo, o None."""
        isbn = self.prestamoComboBox.currentData()
        for prestamo in self._prestamos_activos:
            if prestamo.isbn() == isbn:
                return prestamo
        return None

    def _mostrar_detalle(self):
        """Muestra las fechas y el estado del préstamo seleccionado."""
        prestamo = self._prestamo_seleccionado()
        if prestamo is None:
            self._limpiar_detalle()
            return

        self.fechaLimiteLabel.setText(
            f"Fecha límite del préstamo: {prestamo.fecha_limite()}"
        )
        self.fechaDevolucionLabel.setText(
            f"Fecha de devolución: {date.today()}"
        )
        if prestamo.esta_vencido():
            self.estadoPrestamoLabel.setText("Estado: Vencido")
        else:
            self.estadoPrestamoLabel.setText("Estado: En plazo")

    def devolver(self):
        """Registra la devolución del préstamo elegido."""
        prestamo = self._prestamo_seleccionado()
        if prestamo is None:
            self._mensaje("No hay un préstamo activo seleccionado.", error=True)
            return

        try:
            self.biblioteca.devolver(prestamo.isbn(), self.usuario.dni())
        except errores.ErrorBiblioteca as error:
            self._mensaje(str(error), error=True)
            return

        self.actualizar()
        self._mensaje("Devolución registrada. Ya puedes pedir otro libro.")
        self.datos_actualizados.emit()

    def _limpiar_detalle(self):
        """Restablece los textos de detalle cuando no hay préstamo activo."""
        self.fechaLimiteLabel.setText("Fecha límite del préstamo: —")
        self.fechaDevolucionLabel.setText(f"Fecha de devolución: {date.today()}")
        self.estadoPrestamoLabel.setText("Estado: —")

    def _mensaje(self, texto, error=False):
        """Muestra una ayuda en la etiqueta de estado del formulario."""
        self.ayudaDevolucionLabel.setText(texto)

    def showEvent(self, evento):
        """Refresca los préstamos activos al entrar a la página."""
        super().showEvent(evento)
        self.actualizar()
