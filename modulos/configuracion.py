import json
import os

from modulos import errores

CARPETA_DEL_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATOS = os.path.join(CARPETA_DEL_PROYECTO, "datos")
CARPETA_INTERFACES = os.path.join(CARPETA_DEL_PROYECTO, "interfaces")

ARCHIVO_LIBROS = "libros.json"
ARCHIVO_USUARIOS = "usuarios.json"

NOMBRE_BIBLIOTECA = "Biblioteca IDAT"
LEMA = ""

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


def leer_archivo(nombre_del_archivo):
    ruta = ruta_del_archivo(nombre_del_archivo)
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
    if contenido == "":
        return []
    try:
        return json.loads(contenido)
    except ValueError as error:
        raise errores.ErrorDeArchivo(
            "El archivo " + nombre_del_archivo + " esta mal escrito: " + str(error)
        )
