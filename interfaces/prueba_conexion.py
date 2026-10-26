from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class FormularioLibro(QMainWindow):
    def __init__(self):
        super().__init__()

        ruta_ui = Path(__file__).resolve().parent / "formulario_libro.ui"
        uic.loadUi(ruta_ui, self)

        self.comboBox.clear()
        self.comboBox.addItems(["Accion", "Ciencia Ficcion", "Accion", "Drama"])

        self.pushButton.clicked.connect(self.registrar_libro)

        self.libros = []

    def registrar_libro(self):
        nombre = self.lineEdit.text().strip()
        autor = self.lineEdit_2.text().strip()
        codigo = self.lineEdit_3.text().strip()
        categoria = self.comboBox.currentText().strip()

        invalidos = [None, "", " "]

        libro = {
            "Nombre": nombre,
            "Autor": autor,
            "Codigo": codigo,
            "Categoria": categoria,
        }

        if any(invalido in libro.values() for invalido in invalidos):
            QMessageBox.warning(self, "Mensaje de ERROR", "Coloca los datos requeridos")
        else:
            QMessageBox.information(
                self, "Libro registrado", f"El libro {nombre} ha sido registrado"
            )
            self.libros.append(libro)
            for libro in self.libros:
                self.textEdit.setText(f"El nombre del libro es: {libro['Nombre']}")
                self.textEdit.append(f"El autor del libro es: {libro['Autor']}")
                self.textEdit.append(f"El codigo del libro es: {libro['Codigo']}")
                self.textEdit.append(f"La categoria del libro es: {libro['Categoria']}")
