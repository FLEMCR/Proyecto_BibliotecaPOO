import json
import os

# Aqui avanzaré la conexion con el json para que se lea en el python

ruta_json = os.path.join((__file__), "datos.json")
# print(ruta_json)


def leer_json():
    with open(ruta_json, "r", encoding="utf-8") as leer_datos:
        datos_json = json.load(leer_datos)
    return datos_json


# Ajustes para referenciarlos en los demas modulos

limite_prestamo = {"estudiante": 3, "docente": 5}
tipo_miembro = [
    "Estudiante",
    "Docente",
    "Invitado",
]  # Si se les ocurre mas modifiquen noma, aunque la idea era que cuando no se registren entren como invitado y que puedan registrarse como docente o estudiante.
nombre_biblioteca = "Biblioteca POO"  # Cambien el nombre por el momento lo dejo así
