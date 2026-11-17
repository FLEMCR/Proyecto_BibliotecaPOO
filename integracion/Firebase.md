# Firebase (integración opcional)

El proyecto funciona **completo sin Firebase**: `main.py` solo usa los JSON de `data/`. El módulo `integracion/firebase_sync.py` quedó preparado para subir y bajar esos mismos JSON cuando quieras, pero **no se importa desde `main.py`**. Así el proyecto local sigue siendo simple y la nube se agrega después.

## 1. Instalar la dependencia (solo cuando la uses)

```bash
pip install firebase-admin
```

No hace falta agregarla a `requirements.txt`. Si no está instalada, el módulo avisa con: `Falta firebase-admin. Instálalo con: pip install firebase-admin`.

## 2. Crear el proyecto en Firebase

1. Entrá a <https://console.firebase.google.com/> y creá un proyecto.
2. En **Firestore Database**, creá la base de datos (modo producción o prueba, según tu cuenta).
3. En **Configuración del proyecto → Cuentas de servicio**, generá una clave privada nueva. Firebase descarga un archivo `.json`.

## 3. Ubicar la credencial

Copiá el JSON descargado a:

```text
proyecto_parcial/config/firebase-service-account.json
```

También podés indicar otra ruta con la variable de entorno `FIREBASE_CREDENCIALES`:

```bash
export FIREBASE_CREDENCIALES=/ruta/a/mi-clave.json
```

**No subas ese archivo a Git**: contiene credenciales privadas. Agregá `config/firebase-service-account.json` a `.gitignore`.

## 4. Estructura que se crea en Firestore

El módulo usa la colección `biblioteca` y un documento por archivo:

```text
biblioteca/
├── libros.json      → { datos: [ ...libros... ] }
├── usuarios.json    → { datos: [ ...usuarios... ] }
└── prestamos.json   → { datos: [ ...préstamos... ] }
```

El campo `datos` es una lista con el mismo contenido que el JSON local, así que no hay que cambiar el formato ni las clases `Libro`, `Usuario` o `Prestamo`.

## 5. Funciones disponibles

```python
from integracion import firebase_sync

firebase_sync.subir_json("libros.json")   # sube un archivo, devuelve la cantidad de registros
firebase_sync.descargar_json("libros.json")  # baja y sobrescribe data/libros.json

firebase_sync.subir_todos()     # sube los tres JSON
firebase_sync.descargar_todos()  # baja los tres JSON
```

Ejemplo rápido desde la carpeta `proyecto_parcial/`:

```bash
python3 - <<'PY'
from integracion import firebase_sync
print(firebase_sync.subir_todos())
PY
```

`descargar_todos()` **sobrescribe** los archivos de `data/`. Si querés probar, hacé una copia primero:

```bash
cp -r data data_backup
```

## 6. Cómo conectarlo después a la interfaz

Cuando quieras agregar botones “Subir a la nube” y “Bajar de la nube”:

1. Agregá los botones en `ui/principal.ui`.
2. En `ui/principal.py`, importá el módulo **dentro del método del botón**, no arriba del archivo:

```python
def _subir_a_firebase(self):
    from integracion import firebase_sync
    firebase_sync.subir_todos()
    QMessageBox.information(self, "Firebase", "Datos subidos correctamente")
```

3. Después de bajar datos, recargá la memoria con `self.biblioteca.cargar_datos()` y actualizá la pantalla con `self._refrescar_datos()`.

Así Firebase sigue siendo opcional: si el usuario no instala `firebase-admin` ni tiene la credencial, la app local funciona igual.

## 7. Reglas de seguridad y cuidados

- En Firestore, empezá con reglas que solo permitan al dueño del proyecto leer y escribir; no dejes reglas públicas en producción.
- Nunca incluyas la cuenta de servicio en el repositorio ni en la presentación.
- Los documentos de Firestore tienen un límite cercano a **1 MiB**. Los JSON actuales son chicos, pero si el catálogo crece mucho habría que dividir los datos en varios documentos o colecciones.
- El módulo usa `firebase_admin.get_app()`, así que la app se inicializa una sola vez aunque llames varias funciones.

## 8. Resumen

| Archivo | Para qué sirve |
| --- | --- |
| `integracion/firebase_sync.py` | Subir/bajar los JSON con Firestore. |
| `docs/Firebase.md` | Esta guía. |
| `config/firebase-service-account.json` | Credencial privada (la creás vos, no va en el repo). |
| `main.py` | Sigue sin importar Firebase. |
