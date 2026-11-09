# Sistema de Biblioteca — Programación Orientada a Objetos

Trabajo grupal de Programación Orientada a Objetos (IDAT, 2do ciclo). El proyecto modela una biblioteca universitaria con libros, usuarios, membresías, catálogo, búsqueda y una interfaz gráfica en PyQt5. La lógica de negocio está separada de las pantallas para que el sistema pueda crecer sin reescribir lo que ya funciona.

El plan completo de trabajo, el estado real del proyecto y las tareas pendientes están en:

- [`docs/Plan_del_proyecto.md`](docs/Plan_del_proyecto.md)

## Funcionalidades actuales

- Acceso con DNI, validando que el usuario exista, esté activo y tenga la membresía vigente.
- Panel principal con resumen de títulos, ejemplares, disponibles, prestados y usuarios.
- Catálogo con búsqueda por ISBN, título, autor o categoría.
- Filtro por categoría, filtro de libros disponibles y orden de resultados.
- Tabla con ISBN, título, autor, categoría, disponibles y estado.
- Ficha lateral con estante, ejemplares, prestados y ubicación completa.
- Ficha formateada del libro seleccionado con su ubicación completa.
- Membresía del usuario con vencimiento, estado y beneficios.
- Lista de usuarios y búsqueda por DNI, nombre o tipo (solo administradores).
- Reporte general, disponibilidad por sección y títulos por categoría.
- Exportación del reporte a un archivo `.txt`.
- Menú de consola con las mismas consultas principales.

## Requisitos

- Python 3.10 o superior.
- PyQt5.
- Los datos de ejemplo ya están incluidos en `datos/`.

Instalación de PyQt5:

```bash
python3 -m pip install PyQt5
```

## Cómo ejecutar

Desde la carpeta `proyecto_parcial/`:

```bash
# Versión gráfica
python3 main_gui.py

# Versión de consola
python3 main.py
```

> Importante: los comandos se ejecutan desde la carpeta que contiene `main.py`, `main_gui.py`, `core/`, `datos/` y `ui/`. Si se ejecutan desde otra carpeta, Python no encuentra los módulos.

## Estructura

```text
proyecto_parcial/
├── main.py                     entrada de la versión de consola
├── main_gui.py                 entrada de la versión gráfica
├── core/
│   ├── configuracion.py        rutas, secciones, estantes y reglas
│   ├── errores.py              excepciones del dominio
│   ├── utilidades.py           validaciones de DNI, ISBN y fechas
│   ├── libros.py               clase Libro, búsqueda y filtros recursivos
│   ├── usuarios.py             Usuario, Administrador y fábrica
│   ├── biblioteca.py           controlador del catálogo y usuarios
│   └── menu.py                 menú de consola
├── datos/
│   ├── libros.json             catálogo de ejemplo
│   ├── usuarios.json           usuarios de ejemplo
│   └── reportes/               reportes exportados
├── ui/
│   ├── acceso.ui / acceso.py
│   ├── principal.ui / principal.py
│   ├── catalogo.ui / catalogo.py
│   └── __init__.py
├── recursos/
│   ├── imagenes/               imágenes de la interfaz
│   ├── iconos/                 iconos de botones y ventanas
│   └── README.md
├── docs/
│   ├── Plan_del_proyecto.md
│   ├── Guia_base.md
│   ├── Guia_base.ipynb
│   └── PDFs del sílabo y las rúbricas
└── tests/
```

Cada archivo `.ui` tiene su archivo `.py` con el mismo nombre. El `.ui` solo contiene el diseño; el `.py` carga el diseño y conecta los botones con la lógica de `core/`.

## Imágenes e iconos

Guarda las imágenes en `recursos/imagenes/` y los iconos en `recursos/iconos/`. Las rutas se arman desde `core/configuracion.py` para no repetirlas en cada ventana:

```python
from core import configuracion

configuracion.ruta_de_imagen("logo_biblioteca.png")
configuracion.ruta_de_icono("libro.svg")
```

Por ahora la interfaz usa el aspecto básico de Qt, sin hoja de estilos. Los estilos y las imágenes se integran al final, cuando la funcionalidad esté cerrada.

## Usuarios de prueba

| DNI | Nombre | Tipo | Estado |
| --- | --- | --- | --- |
| `11111111` | P_ESTUDIANTE | Estudiante | Activo |
| `22222222` | P_DOCENTE | Docente | Activo |
| `33333333` | P_ADMINISTRADOR | Administrador | Activo |
| `78901234` | Valeria Sanchez | Administrador | Membresía vencida |
| `70778899` | Rosa Palomino | Estudiante | De baja |
| `76789012` | Diego Vargas | Docente | Membresía vencida |
| `99999999` | — | — | No existe |

## Arquitectura

```text
ui/        → ventanas y widgets (no leen JSON ni calculan reglas)
core/      → clases, reglas de negocio, búsquedas y excepciones
datos/     → archivos JSON y reportes
recursos/  → imágenes e iconos de la interfaz
main*.py   → puntos de entrada
```

Reglas del proyecto:

- Ninguna ventana lee archivos directamente: todo pasa por `Biblioteca`.
- Las clases de negocio no muestran mensajes gráficos.
- El nombre y el lema de la biblioteca salen de `core/configuracion.py`; no se repiten en las ventanas.
- Las rutas de imágenes e iconos también salen de `core/configuracion.py`.
- Por ahora la interfaz no usa estilos: se deja el aspecto básico de Qt. Los estilos se agregarán al final.
- Las matrices y los reportes se calculan desde los datos; no se guardan duplicados.
- Los nombres importantes describen el dominio: `Prestamo`, `prestar_ejemplar`, `mapa_de_estantes`, `historial_por_usuario`.

## Pendientes principales

- Clase `Prestamo` y archivo `prestamos.json`.
- Préstamo y devolución con actualización automática de disponibilidad.
- Cálculo de multas por retraso y tope de multa.
- Registro y edición de libros desde la interfaz.
- Alta, baja, reactivación y renovación de membresías.
- Matrices de disponibilidad, devoluciones pendientes, historial y penalizaciones.
- Formularios de libro, usuario, préstamo y devolución.
- Persistencia de todos los cambios.
- Pruebas automatizadas.
- Sistema académico del segundo entregable.

El detalle de cada pendiente, sus responsables y sus criterios de aceptación está en el plan del proyecto.
