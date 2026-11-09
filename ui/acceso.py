from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

ruta_ui = Path(__file__).resolve().parent / "acceso.ui"


class Acceso(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(ruta_ui), self)
