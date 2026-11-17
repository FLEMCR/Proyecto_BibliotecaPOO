# Sistema de Biblioteca — POO

Proyecto grupal de Programación Orientada a Objetos. Es una aplicación para gestionar una biblioteca universitaria: acceso por DNI, catálogo, préstamos, devoluciones, membresía y panel de administración. Los datos se guardan en archivos JSON y se recargan al iniciar.

## Entrada y ejecución

```bash
pip install -r requirements.txt
python3 main.py
```

`main.py` es el **único punto de entrada**. La hoja de estilos `assets/styles/app.qss` se carga automáticamente.

## Estructura

```
proyecto_parcial/
├── main.py                    Entrada única (PyQt5)
├── assets/styles/app.qss      Tema oscuro, organizado por secciones
├── core/
│   ├── configuracion.py       Rutas (pathlib), constantes y lectura/escritura JSON
│   ├── errores.py             Excepciones propias
│   ├── utilidades.py          Regex, normalización y validación de fechas
│   ├── libros.py              Clase Libro y fábrica
│   ├── usuarios.py            Usuario, Administrador (herencia) y fábrica
│   ├── prestamos.py           Clase Préstamo
│   ├── biblioteca.py          Controlador del sistema
│   └── reportes.py            Matrices, recursividad, generador y exportación
├── data/                      libros.json, usuarios.json, prestamos.json
├── docs/                      Plan, guías y material de exposición
├── tests/                     Pruebas unitarias (no versionadas)
└── ui/                        Cada ventana tiene .ui (Qt Designer) + .py (lógica)
```

## Funcionalidades

- **Inicio:** solo el saludo `Hola, nombre`, el tipo de usuario y el lema arriba; el resto del espacio queda libre para colocar una imagen o iconos SVG después.
- **Acceso:** DNI, alta de usuarios, validación de membresía y cuenta activa.
- **Catálogo:** búsqueda, filtros, orden, ficha del libro y botón **Registrar préstamo** que copia el ISBN a la pantalla de préstamos. Para administradores aparecen además **Nuevo libro**, **Editar libro** y **Eliminar libro** (este último solo si el libro no tiene préstamos activos).
- **Préstamos:** ISBN validado con regex, fecha límite automática de 15 días desde el inicio (sin calendario) y registro a nombre del usuario conectado; un préstamo vencido bloquea nuevos préstamos hasta devolverlo.
- **Devoluciones:** selección del préstamo activo y actualización del stock.
- **Administración:** alta, edición y baja de libros desde el catálogo, listado de usuarios con filtro, renovación de membresías y reportes.
- **Reportes:** resumen general arriba y dos tablas separadas: **historial de préstamos** (quién pidió qué libro, fechas y estado) e **inventario de libros** (ejemplares, prestados y disponibles). El resumen de Inicio se movió acá. Se puede exportar todo a `data/reporte.txt`.
- **Lema:** `Un libro es un viaje de ida y vuelta: llévalo contigo y devuélvelo cuando el viaje haya terminado.`

## Temas aplicados

POO (clases, encapsulación, herencia, polimorfismo, abstracción), PyQt5 y Qt Designer, componentes básicos y avanzados, señales y slots, QSS, `pathlib`, JSON, expresiones regulares, excepciones propias, matrices, recursividad, generadores y cierres.

## Usuarios de prueba

| DNI        | Nombre          | Tipo          |
| ---------- | --------------- | ------------- |
| `11111111` | `ESTUDIANTE`    | Estudiante    |
| `22222222` | `DOCENTE`       | Docente       |
| `99999999` | `ADMINISTRADOR` | Administrador |

El administrador principal tiene la membresía vigente hasta `2036-11-17` en `data/usuarios.json`. Desde **Usuarios** puede renovar el vencimiento de cualquier usuario (suma 3 meses).
