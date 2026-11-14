import json
from pathlib import Path

CARPETA_DEL_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS = CARPETA_DEL_PROYECTO / "data"
CARPETA_INTERFACES = CARPETA_DEL_PROYECTO / "ui"
CARPETA_ASSETS = CARPETA_DEL_PROYECTO / "assets"
CARPETA_ESTILOS = CARPETA_ASSETS / "styles"
ARCHIVO_ESTILOS = CARPETA_ESTILOS / "app.qss"

ARCHIVO_LIBROS = "libros.json"
ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_PRESTAMOS = "prestamos.json"

MESES_DE_MEMBRESIA = 3
MAXIMO_PRESTAMOS_POR_USUARIO = 1
DIAS_DE_PRESTAMO = 15

NOMBRE_BIBLIOTECA = "Biblioteca General POSTDATA"
LEMA = "Llevate el libro que quieras; Devuélvelo cuando puedas"

CATEGORIAS = [
    "Literatura",
    "Ciencias sociales",
    "Ciencias básicas",
    "Tecnología",
    "Arte",
]

SECCIONES = {
    "A": "Literatura",
    "B": "Ciencias sociales",
    "C": "Ciencias básicas",
    "D": "Tecnología",
    "E": "Arte",
}

ESTADOS_DE_PRESTAMO = ["activo", "devuelto"]

CANTIDAD_DE_ESTANTES = 3

TIPOS_DE_USUARIO = ["Estudiante", "Docente", "Administrador"]


def ruta_del_archivo(nombre_del_archivo):
    return CARPETA_DATOS / nombre_del_archivo


def leer_archivo(nombre_del_archivo):
    ruta = ruta_del_archivo(nombre_del_archivo)
    if not ruta.exists():
        return []
    contenido = ruta.read_text(encoding="utf-8").strip()
    if contenido == "":
        return []
    return json.loads(contenido)


def escribir_archivo(nombre_del_archivo, datos):
    """Escribe una lista o un diccionario en un archivo JSON del proyecto."""
    ruta = ruta_del_archivo(nombre_del_archivo)
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    ruta.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
