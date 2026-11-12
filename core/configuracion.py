import json
import os

CARPETA_DEL_PROYECTO = os.path.dirname(os.path.dirname(__file__))
CARPETA_DATOS = os.path.join(CARPETA_DEL_PROYECTO, "data")
CARPETA_INTERFACES = os.path.join(CARPETA_DEL_PROYECTO, "ui")
CARPETA_ASSETS = os.path.join(CARPETA_DEL_PROYECTO, "assets")
CARPETA_ESTILOS = os.path.join(CARPETA_ASSETS, "styles")
ARCHIVO_ESTILOS = os.path.join(CARPETA_ESTILOS, "app.qss")

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
    "Ciencias",
    "Tecnología",
    "Arte",
]

SECCIONES = {
    "A": "Literatura",
    "B": "Ciencias sociales",
    "C": "Ciencias",
    "D": "Tecnología",
    "E": "Arte",
}

ESTADOS_DE_PRESTAMO = ["activo", "devuelto"]

CANTIDAD_DE_ESTANTES = 3

TIPOS_DE_USUARIO = ["Estudiante", "Docente", "Administrador"]


def ruta_del_archivo(nombre_del_archivo):
    return os.path.join(CARPETA_DATOS, nombre_del_archivo)


def leer_archivo(nombre_del_archivo):
    ruta = ruta_del_archivo(nombre_del_archivo)
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
    if contenido == "":
        return []
    return json.loads(contenido)


def escribir_archivo(nombre_del_archivo, datos):
    """Escribe una lista o un diccionario en un archivo JSON del proyecto."""
    ruta = ruta_del_archivo(nombre_del_archivo)
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")
