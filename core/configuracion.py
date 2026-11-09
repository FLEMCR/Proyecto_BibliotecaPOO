import json
import os

CARPETA_DEL_PROYECTO = os.path.dirname(os.path.dirname(__file__))
CARPETA_DATOS = os.path.join(CARPETA_DEL_PROYECTO, "datos")
CARPETA_UI = os.path.join(CARPETA_DEL_PROYECTO, "ui")
CARPETA_INTERFACES = CARPETA_UI
CARPETA_REPORTES = os.path.join(CARPETA_DATOS, "reportes")
CARPETA_RECURSOS = os.path.join(CARPETA_DEL_PROYECTO, "recursos")
CARPETA_IMAGENES = os.path.join(CARPETA_RECURSOS, "imagenes")
CARPETA_ICONOS = os.path.join(CARPETA_RECURSOS, "iconos")

ARCHIVO_LIBROS = "libros.json"
ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_PRESTAMOS = "prestamos.json"
ARCHIVO_BITACORA = "bitacora.txt"

DIAS_DE_PRESTAMO = 15
MAXIMO_PRESTAMOS_POR_USUARIO = 2
MULTA_POR_DIA_DE_RETRASO = 1.5
TOPE_DE_MULTA = 30.0

NOMBRE_BIBLIOTECA = "Biblioteca General POSTDATA"
LEMA = "Llevate el libro que quieras; Devuélvelo cuando puedas"

SECCIONES = {
    "A": "Literatura",
    "B": "Ciencias sociales",
    "C": "Ciencias e ingenieria",
    "D": "Tecnologia",
    "E": "Arte",
}

CANTIDAD_DE_ESTANTES = 3

TIPOS_DE_USUARIO = ["Estudiante", "Docente", "Administrador"]


def ruta_del_archivo(nombre_del_archivo):
    return os.path.join(CARPETA_DATOS, nombre_del_archivo)


def ruta_de_imagen(nombre_de_la_imagen):
    """Devuelve la ruta de una imagen guardada en recursos/imagenes."""
    return os.path.join(CARPETA_IMAGENES, nombre_de_la_imagen)


def ruta_de_icono(nombre_del_icono):
    """Devuelve la ruta de un icono guardado en recursos/iconos."""
    return os.path.join(CARPETA_ICONOS, nombre_del_icono)


def leer_archivo(nombre_del_archivo):
    ruta = ruta_del_archivo(nombre_del_archivo)
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
    except OSError as error:
        from core import errores

        raise errores.ErrorDeArchivo(f"No se pudo leer el archivo {ruta}: {error}")
    if contenido == "":
        return []
    try:
        return json.loads(contenido)
    except json.JSONDecodeError as error:
        from core import errores

        raise errores.ErrorDeArchivo(
            f"El archivo {nombre_del_archivo} tiene un JSON mal escrito "
            f"(linea {error.lineno}, columna {error.colno})"
        )
