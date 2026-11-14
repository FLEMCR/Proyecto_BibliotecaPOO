# Parcial de POO - Sistema de Biblioteca

Trabajo grupal del parcial de Programación Orientada a Objetos (IDAT, 2do ciclo). Es un sistema de biblioteca universitaria con interfaz gráfica en PyQt5: acceso por DNI, registro de usuarios, catálogo de libros, préstamos, devoluciones y panel de administración. Los datos se guardan en archivos JSON que se leen al arrancar y se actualizan al operar el sistema.

## Resumen

El proyecto aplica POO con clases, encapsulación, herencia, polimorfismo, excepciones propias, lectura y escritura de JSON, y recorrido recursivo del catálogo.

## Estructura

```
proyecto_parcial/
├── main.py                     Punto de entrada único (interfaz gráfica)
├── README.md                   Descripción del proyecto
├── requirements.txt            Dependencias
├── assets/
│   ├── images/                 Íconos e imágenes
│   └── styles/
│       └── app.qss             Tema oscuro de la aplicación
├── core/
│   ├── configuracion.py        Rutas, categorías, secciones y archivos JSON
│   ├── errores.py              Excepciones personalizadas
│   ├── utilidades.py           Validaciones de DNI, ISBN y fechas
│   ├── libros.py               Clase Libro, validaciones y fábrica
│   ├── usuarios.py             Clases Usuario y Administrador
│   ├── prestamos.py            Clase Prestamo
│   ├── biblioteca.py           Controlador central del sistema
│   └── reportes.py             Espacio para reportes
├── data/
│   ├── libros.json             Catálogo de libros
│   ├── usuarios.json           Usuarios registrados
│   └── prestamos.json          Préstamos registrados
├── docs/
│   └── Plan_proyecto.md        Plan y documentación del proyecto
└── ui/
    ├── acceso.py / .ui         Ventana de acceso
    ├── registro.py / .ui       Registro de usuarios
    ├── principal.py / .ui      Panel principal
    ├── catalogo.py / .ui       Catálogo y ficha del libro
    ├── prestamo.py / .ui       Página de préstamos
    ├── devolucion.py / .ui     Página de devoluciones
    └── libro_form.py / .ui     Alta y edición de libros
```

## Cómo ejecutar

```bash
pip install -r requirements.txt
python3 main.py
```

`main.py` es la única entrada del sistema. La hoja de estilos se carga automáticamente desde `assets/styles/app.qss`.

## Credenciales de prueba

| DNI        | Nombre            | Tipo          |
| ---------- | ----------------- | ------------- |
| `11111111` | `P_ESTUDIANTE`    | Estudiante    |
| `22222222` | `P_DOCENTE`       | Docente       |
| `33333333` | `P_ADMINISTRADOR` | Administrador |

## Funcionalidades

- Acceso con DNI, validación de cuenta activa y membresía vigente.
- Autorregistro de estudiantes y docentes con membresía de 3 meses.
- Panel de inicio con resumen de títulos, ejemplares, disponibles, prestados y usuarios.
- Catálogo con búsqueda por campo, filtro por categoría, orden y disponibilidad.
- Préstamo y devolución de ejemplares con actualización de stock.
- Alta y edición de libros para administradores.
- Página de membresía del usuario conectado.

## Datos

Los archivos de `data/` se pueden editar a mano. El sistema los vuelve a leer al arrancar y guarda los cambios realizados desde la interfaz.
