from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

ruta_ui = Path(__file__).resolve().parent / "principal.ui"


class Acceso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(ruta_ui), self)
