# Parcial de POO - Sistema de Biblioteca

Trabajo grupal del parcial de Programación Orientada a Objetos (IDAT, 2do ciclo). Es un sistema de biblioteca universitaria que corre en consola: catálogo de libros, miembros con membresía, consulta por categoría con una función recursiva, tres matrices de datos y un menú de gestión para el administrador. Los datos están en dos archivos JSON, se pueden editar a mano y el programa los vuelve a leer al arrancar.

## Resumen

El proyecto cuenta con una base sólida de POO: clases, encapsulación, herencia, polimorfismo, excepciones propias, lectura de JSON y búsqueda recursiva.

## Estructura
proyecto_parcial/
├── main.py                     Punto de entrada principal
├── README.md                   Documentación y plan del proyecto
├── core/
│   ├── configuracion.py        Rutas, secciones, estantes y lectura de JSON
│   ├── errores.py              Excepciones personalizadas (ErrorBiblioteca, ErrorDeDatos)
│   ├── utilidades.py           Validaciones de DNI, ISBN, fechas y pausas
│   ├── libros.py               Clase Libro, validaciones y funciones recursivas
│   ├── usuarios.py             Clases Usuario, Administrador y fábrica de usuarios
│   ├── biblioteca.py           Controlador central (catálogo, usuarios y resumen)
│   └── menu.py                 Interfaz de consola y opciones de navegación
├── datos/
│   ├── libros.json             Catálogo de libros
│   └── usuarios.json           Usuarios registrados
└── interfaces/                 Diseños UI y estilos (QtDesigner)

## Nombres sugeridos

| Concepto de la rúbrica | Nombre sugerido en el código |
|---|---|
| Matriz de disponibilidad por sección y estante | `mapa_de_estantes` |
| Matriz de devoluciones pendientes | `agenda_de_devoluciones` |
| Matriz de historial por usuario | `historial_por_usuario` |
| Matriz de penalizaciones | `penalizaciones_por_usuario` |
| Recursión para buscar por categoría | `buscar_en_categoria` |
| Recursión para contar disponibles | `contar_disponibles_en_seccion` |
| Recursión para sumar existencias | `sumar_existencias` |
| Préstamo | `Prestamo` / `prestar_ejemplar` |
| Devolución | `devolver_ejemplar` |
| Multa | `calcular_multa` |
| Bitácora | `registrar_en_bitacora` |

## Pendientes

- Prestar y devolver libros mediante el gestor y las opciones del menú.
- Historial y multas por retraso guardando la fecha real de cada préstamo y calculando los días de retraso.
- Registrar y actualizar libros directamente desde el menú del programa.
- Dar de alta, dar de baja, reactivar o renovar la membresía de un miembro desde las opciones del menú.
- Búsqueda específica de libros por título o autor.
- Establecer un tope de multa por préstamo.
- Definir el nombre y el lema definitivos en `configuracion.py`.

## Pendientes final

- Diseñar y conectar las interfaces gráficas con PyQt5 y QtDesigner (incluyendo componentes avanzados como `QSpinBox`, `QComboBox`, `QTableWidget` y `QCalendarWidget`).
- Implementar la persistencia avanzada con archivos de texto o binarios para el registro de calificaciones y asistencia.
- Aplicar expresiones regulares para validaciones avanzadas de formato en los campos de entrada de la interfaz académica.
- Estructurar el sistema bajo principios sólidos de POO separados por clases de ventana y lógica de negocio.
