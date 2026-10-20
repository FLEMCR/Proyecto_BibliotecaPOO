import json
import os

CARPETA_DATOS = os.path.join(os.path.dirname(__file__), "datos")

ARCHIVOS = {
    "libros": "libros.json",
    "miembros": "miembros.json",
    "prestamos": "h_prestamos.json",
}

nombre_biblioteca = "Biblioteca POO HAY QUE CAMBIAR NOMBREEEEEE"
lema = "FRASE A USAR WAAAAAA"

limite_libros = {"estudiante": 3, "docente": 5, "administrador": 5, "invitado": 0}
dias_prestamo = {"estudiante": 14, "docente": 21, "administrador": 21, "invitado": 0}
multa_por_dia = {
    "estudiante": 0.50,
    "docente": 0.50,
    "administrador": 0.00,
    "invitado": 0.00,
}


def ruta_json(nombre):
    if ARCHIVOS.get(nombre) is None:
        raise KeyError("archivo desconocido: ", str(nombre))
    return os.path.join(CARPETA_DATOS, ARCHIVOS[nombre])


def leer_json(nombre):
    ruta = ruta_json(nombre)
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
    if not contenido:
        return []
    return json.loads(contenido)


def guardar_json(nombre, datos):
    ruta = ruta_json(nombre)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")
    return True


def cargar_todos():
    return {nombre: leer_json(nombre) for nombre in ARCHIVOS}
