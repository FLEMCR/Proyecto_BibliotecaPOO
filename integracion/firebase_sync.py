"""Sincronización opcional de los JSON con Firebase Firestore.

Este archivo NO se importa desde ``main.py``: el proyecto sigue funcionando
solo con archivos locales. ``firebase-admin`` se importa recién cuando se llama
a una de estas funciones, así que no es una dependencia obligatoria.
"""

import os
from pathlib import Path

from core import configuracion

COLECCION = "biblioteca"

RUTA_CREDENCIALES = Path(
    os.environ.get(
        "FIREBASE_CREDENCIALES",
        configuracion.CARPETA_DEL_PROYECTO
        / "config"
        / "firebase-service-account.json",
    )
)

ARCHIVOS = (
    configuracion.ARCHIVO_LIBROS,
    configuracion.ARCHIVO_USUARIOS,
    configuracion.ARCHIVO_PRESTAMOS,
)


def _cliente():
    """Crea (una sola vez) el cliente de Firestore usando la cuenta de servicio."""
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError as exc:
        raise RuntimeError(
            "Falta firebase-admin. Instálalo con: pip install firebase-admin"
        ) from exc

    try:
        firebase_admin.get_app()
    except ValueError:
        if not RUTA_CREDENCIALES.is_file():
            raise FileNotFoundError(
                f"No se encontró la credencial en: {RUTA_CREDENCIALES}"
            ) from None
        firebase_admin.initialize_app(
            credentials.Certificate(str(RUTA_CREDENCIALES))
        )

    return firestore.client()


def subir_json(nombre_del_archivo):
    """Sube un JSON local a Firestore y devuelve la cantidad de registros."""
    datos = configuracion.leer_archivo(nombre_del_archivo)
    _cliente().collection(COLECCION).document(nombre_del_archivo).set(
        {"datos": datos}
    )
    return len(datos)


def descargar_json(nombre_del_archivo):
    """Baja un JSON desde Firestore, lo guarda en ``data/`` y lo devuelve."""
    documento = (
        _cliente().collection(COLECCION).document(nombre_del_archivo).get()
    )
    if not documento.exists:
        raise FileNotFoundError(
            f"No hay datos de {nombre_del_archivo} en la colección {COLECCION}"
        )
    datos = documento.to_dict().get("datos", [])
    configuracion.escribir_archivo(nombre_del_archivo, datos)
    return datos


def subir_todos():
    """Sube los tres JSON y devuelve un diccionario con las cantidades enviadas."""
    return {nombre: subir_json(nombre) for nombre in ARCHIVOS}


def descargar_todos():
    """Baja los tres JSON y devuelve un diccionario con las cantidades recibidas."""
    return {nombre: len(descargar_json(nombre)) for nombre in ARCHIVOS}
