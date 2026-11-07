# Plan para cumplir la rúbrica del parcial y preparar el final

> **Proyecto:** Sistema de Biblioteca Universitaria  
> **Curso:** Programación Orientada a Objetos (IDAT, 2.º ciclo)  
> **Estado actual:** 16/20 en la rúbrica del parcial  
> **Meta del parcial:** 20/20  
> **Meta del final:** 20/20 con el sistema de calificaciones y asistencia que pide la rúbrica final  
> **Fecha de este plan:** 2026-11-07  
> **Documento:** `docs/Plan_mejora_parcial_y_final.md`

---

## Contenido

1. [Resumen ejecutivo](#0-resumen-ejecutivo)
2. [Punto de partida: qué hay y qué no](#1-punto-de-partida-qué-hay-y-qué-no)
3. [Rúbrica del parcial: diagnóstico y plan para llegar a 20/20](#2-rúbrica-del-parcial-diagnóstico-y-plan-para-llegar-a-2020)
4. [Diseño de interfaces: qué ventanas debe haber y cómo se llaman](#3-diseño-de-interfaces-qué-ventanas-debe-haber-y-cómo-se-llaman)
5. [Lógica del sistema para el parcial](#4-lógica-del-sistema-para-el-parcial)
6. [Matrices y recursividad con nombres del dominio](#5-matrices-y-recursividad-con-nombres-del-dominio)
7. [Los 9 temas del sílabo aplicados al proyecto](#6-los-9-temas-del-sílabo-aplicados-al-proyecto)
8. [Plan de ejecución para la entrega del parcial](#7-plan-de-ejecución-para-la-entrega-del-parcial)
9. [Rúbrica del final: sistema de calificaciones y asistencia](#8-rúbrica-del-final-sistema-de-calificaciones-y-asistencia)
10. [Defensa oral: cómo explicar cada concepto](#9-defensa-oral-cómo-explicar-cada-concepto)
11. [Diccionario de nombres: cómo llamar a las cosas](#10-diccionario-de-nombres-cómo-llamar-a-las-cosas)
12. [Snippets listos para adaptar](#11-snippets-listos-para-adaptar)
13. [Siguientes pasos y decisiones](#12-siguientes-pasos-y-decisiones)

---

## 0. Resumen ejecutivo

El proyecto ya tiene una base muy buena de POO: clases, encapsulación, herencia, polimorfismo, excepciones, JSON y búsqueda recursiva. Eso se refleja en la nota: **POO y funciones están en nivel sobresaliente**. Lo que falta para llegar a 20/20 en el parcial es principalmente **funcionalidad completa** (préstamos, devoluciones, registro/actualización de libros y membresías) y **matrices/recursividad** con el nivel que pide la rúbrica.

Con las imágenes de la calificación, el 16 se puede leer así:

| Criterio | Puntaje actual | Puntaje máximo | Lectura |
|---|---:|---:|---|
| Implementaciones de funcionalidad | 4 | 5 | Funciona el catálogo, la búsqueda y la consulta, pero faltan préstamos, devoluciones, altas y actualizaciones. |
| Aplicación de conceptos de POO | 5 | 5 | Ya está en sobresaliente: clases, encapsulación, herencia y polimorfismo. |
| Uso de funciones y métodos | 4 | 4 | Ya está en sobresaliente: funciones, parámetros, retornos y excepciones. |
| Uso de matrices y recursividad | 3 | 2 | Hay recursividad de búsqueda, pero no hay matrices de reportes ni recursividad sobre matrices. |
| **Total** | **16** | **20** | Falta completar funcionalidad y llevar matrices/recursividad al nivel superior. |

> Si el profesor marcó otro casillero exacto, ajusta esa fila. La ruta de mejora es la misma: **completar las operaciones que faltan y demostrar matrices + recursividad con nombres del dominio de la biblioteca**.

La idea central del documento es esta:

1. **No cambiar el dominio del parcial.** El parcial es una biblioteca universitaria. Ahí se usan nombres como `Libro`, `Usuario`, `Prestamo`, `mapa_de_estantes`, `agenda_de_devoluciones`.
2. **No poner nombres genéricos.** En el código no debe aparecer `matriz1`, `funcion_recursiva`, `aux`, `dato`, `x` o `temporal` para las cosas importantes. Se usan nombres que se entiendan sin leer el comentario: `mapa_de_estantes`, `historial_por_usuario`, `buscar_en_categoria`, `contar_disponibles_en_seccion`.
3. **Las matrices son vistas, no datos duplicados.** No se guardan en el JSON. Se construyen cuando se pide un reporte, a partir del catálogo y de los préstamos. Así nunca quedan desactualizadas.
4. **La recursividad se demuestra con caso base y paso recursivo.** No basta con que “funcione”: hay que poder señalar el caso base, el paso y la acumulación, y explicar por qué no desborda la pila.
5. **El final es otro enunciado.** La rúbrica final pide un sistema de **calificaciones y asistencia** con PyQt5/QtDesigner, archivos y expresiones regulares. La biblioteca sirve como base de código y de conceptos, pero el entregable final debe cumplir ese otro contexto. En la sección 7 está el plan completo y, al final, el mapeo por si el profesor permite continuar con la biblioteca.

### Ruta de un vistazo

| Momento | Nota actual | Meta | Foco principal |
|---|---:|---:|---|
| Parcial (definitiva) | 16/20 | 20/20 | Préstamos, devoluciones, CRUD de libros y membresías, matrices y recursividad. |
| Final | — | 20/20 | PyQt5/QtDesigner, archivos de texto/binarios, expresiones regulares, POO y demostración. |

### Regla de nombres para todo el proyecto

| Concepto de la rúbrica | Nombre que se usa en el código | Por qué |
|---|---|---|
| Matriz de disponibilidad por sección y estante | `mapa_de_estantes` | Describe lo que representa: un mapa de la biblioteca. |
| Matriz de devoluciones pendientes | `agenda_de_devoluciones` | Suena a una agenda real, no a una matriz abstracta. |
| Matriz de historial por usuario | `historial_por_usuario` | Se entiende qué contiene y para quién. |
| Matriz de penalizaciones | `penalizaciones_por_usuario` | Dice exactamente qué se está contando. |
| Recursión para buscar por categoría | `buscar_en_categoria` | La acción es buscar, no “hacer recursión”. |
| Recursión para contar disponibles | `contar_disponibles_en_seccion` | La acción es contar ejemplares. |
| Recurs -parar existencias | `sumar_existencias` | La acción es sumar existencias. |
| Préstamo | `Prestamo` / `prestar_ejemplar` | Es el objeto y la operación del negocio. |
| Devolución | `devolver_ejemplar` | Es la operación inversa y se entiende sola. |
| Multa | `calcular_multa` | Es el cálculo que pide la rúbrica. |
| Bitácora | `registrar_en_bitacora` | Es el archivo de texto donde queda el historial. |

---

## 1. Punto de partida: qué hay y qué no

### 1.1 Inventario real del proyecto

```
proyecto_parcial/
├── main.py                  arranca el programa
├── README.md                resumen y pendientes
├── core/
│   ├── configuracion.py     rutas, secciones, estantes, lectura de JSON
│   ├── errores.py           ErrorBiblioteca y ErrorDeDatos
│   ├── utilidades.py        validar DNI/ISBN, fechas, pausa
│   ├── libros.py            clase Libro y búsqueda recursiva
│   ├── usuarios.py          Usuario y Administrador
│   ├── biblioteca.py        catálogo, usuarios, resumen
│   └── menu.py              menú de consola
├── datos/
│   ├── libros.json          22 libros
│   └── usuarios.json        13 usuarios
├── docs/
│   ├── Guia_base.md
│   ├── Guia_base.ipynb
│   ├── 1. Sílabo_IDAT_Programación Orientada a Objetos_18102024.pdf
│   ├── 3.1. Rúbrica Parcial_IDAT_POO.pdf
│   └── 3.2. Rúbrica Final_IDAT_Programación Orientada a Objetos_20122024.pdf
├── interfaces/              ¡existe en Git, pero está borrada del área de trabajo!
│   ├── acceso.ui
│   ├── catalogo.ui
│   ├── membresia.ui
│   ├── principal.ui
│   ├── usuarios.ui
│   ├── prueba_conexion.py
│   └── prueba_interfaz.py
├── ui/                      vacía por ahora
└── tests/
    ├── a.py
    └── pr.py
```

### 1.2 Lo que ya funciona

- **Clases y objetos:** `Libro`, `Usuario`, `Administrador` y `Biblioteca`.
- **Encapsulación:** atributos con `_` adelante y métodos de lectura (`titulo()`, `autor()`, `dni()`, etc.).
- **Herencia:** `Administrador(Usuario)`.
- **Polimorfismo:** `puede_administrar()` y `datos_de_membresia()` responden distinto según la clase.
- **Constructores con valores por defecto:** `Usuario(dni, nombre, tipo="Estudiante", ...)`.
- **Excepciones propias:** `ErrorBiblioteca` y `ErrorDeDatos`.
- **Validaciones:** DNI de 8 dígitos, ISBN de 13 dígitos, fechas reales, sección y estante válidos.
- **Recursividad:** `buscar_por_texto()` y `datos_del_catalogo()`.
- **Archivos JSON:** lectura del catálogo y de los usuarios.
- **Menú de consola:** acceso, catálogo, búsqueda, ficha por ISBN, membresía y lista de usuarios.
- **Interfaces QtDesigner:** hay cinco `.ui` ya diseñadas en el historial de Git: acceso, catálogo, membresía, principal y usuarios.

### 1.3 Lo que falta y explica el 16

| Falta | ¿Dónde se nota? | ¿Qué criterio de la rúbrica mejora? |
|---|---|---|
| Préstamos y devoluciones | No hay clase `Prestamo`, no hay opción en el menú, no se descuenta ni se devuelve disponibilidad. | Funcionalidad y POO. |
| Registro de libros desde el programa | El catálogo solo se edita a mano en el JSON. | Funcionalidad. |
| Actualización de libros | No hay métodos para cambiar título, autor, categoría, estante o ejemplares. | Funcionalidad y funciones. |
| Gestión de membresías | No se puede dar de alta, de baja, reactivar o renovar desde el menú. | Funcionalidad y POO. |
| Matrices de reportes | No existe ninguna matriz en el código actual. El README dice “tres matrices”, pero no están implementadas. | Matrices y recursividad. |
| Recursividad sobre matrices | Solo hay recursión sobre listas; falta recorrer filas y columnas. | Matrices y recursividad. |
| Historial y multas | No se guarda la fecha real del préstamo ni se calculan días de retraso. | Funcionalidad y POO. |
| Escritura de archivos | Solo se lee; no hay `guardar_archivo()` ni `prestamos.json`. | Funciones y funcionalidad. |
| Conexión de las interfaces | Las `.ui` están diseñadas, pero no conectadas a la lógica. | Final, y suma en el parcial. |
| Búsqueda por título/autor | La búsqueda actual sí busca en título, autor y categoría; falta una opción específica y ordenada. | Funcionalidad. |
| Tope de multa | No existe. | Funcionalidad. |
| Nombre y lema definitivos | Siguen con textos de prueba (`WAAAAAA`). | Presentación. |

### 1.4 Errores técnicos que hay que corregir antes de agregar cosas

1. **`main.py` no arranca desde la carpeta del proyecto.**
   - Error: `ModuleNotFoundError: No module named 'proyecto_parcial'`.
   - Causa: los imports son `from proyecto_parcial.core import ...`, pero al ejecutar `python3 main.py` dentro de `proyecto_parcial/`, Python busca un paquete `proyecto_parcial` dentro de esa misma carpeta y no lo encuentra.
   - Solución rápida para mañana, sin tocar imports:
     ```bash
     cd /mnt/Compartido/1IDT/CI2/programacion_orientada_a_objetos
     python3 -m proyecto_parcial.main
     ```
   - Solución más cómoda: crear un `run.py` en la carpeta del proyecto que agregue la carpeta padre al `sys.path`, o cambiar los imports a relativos (`from .core import ...`) y ejecutar con `python3 -m`.
   - Recomendación: dejar `main.py` con `if __name__ == "__main__": main()` y documentar el comando correcto en el README.

2. **`Libro.prestados()` devuelve un texto fijo.**
   ```python
   def prestados(self):
       return "Aun por hacer".upper()
   ```
   Debe ser:
   ```python
   def prestados(self):
       return self._ejemplares - self._disponibles
   ```

3. **`crear_libro()` no tiene valores por defecto en todos los campos.**
   - `categoria`, `seccion`, `estante`, `ejemplares` y `disponibles` usan `datos.get(...)` sin segundo argumento. Si el JSON viene incompleto, llega `None` y `int(None)` lanza `TypeError` en vez de `ErrorDeDatos`.
   - Solución: poner valores por defecto válidos o lanzar un `ErrorDeDatos` con un mensaje claro.

4. **`leer_archivo()` no atrapa JSON mal escrito.**
   - Si falta una coma, el programa termina con un traceback de `json`.
   - Solución: `try/except json.JSONDecodeError` y relanzar como `ErrorDeArchivo` o `ErrorDeDatos`.

5. **Hay tildes y erratas en el código.**
   - `año` en `convertir_fecha()`.
   - `más` en el mensaje de `Libro.revisar_datos()`.
   - `Preube` en `menu.py`.
   - `Opción` con tilde cuando el resto del código no la usa.
   - No es grave, pero un proyecto “sin errores” también se cuida en los detalles.

6. **El README y la guía hablan de `modulos/`, pero el código actual está en `core/`.**
   - Esto confunde al profesor y a los integrantes.
   - Solución: actualizar el README y la guía, o dejar una nota al inicio: “la versión actual usa `core/`; `modulos/` era la versión anterior”.

7. **Las interfaces están borradas del área de trabajo.**
   - Recuperarlas:
     ```bash
     cd /mnt/Compartido/1IDT/CI2/programacion_orientada_a_objetos/proyecto_parcial
     git restore interfaces/
     ```
   - `configuracion.py` ya apunta a `CARPETA_INTERFACES = .../interfaces`, así que conviene mantener esa carpeta y no mover los `.ui` a `ui/` sin actualizar la ruta.
   - `prueba_conexion.py` busca `formulario_libro.ui`, que no está en Git. Hay que crear ese formulario o cambiar el script para que use `catalogo.ui`.

---

## 3. Diseño de interfaces: qué ventanas debe haber y cómo se llaman

Esta sección responde a una pregunta concreta: **si tus compañeros van a diseñar las interfaces en QtDesigner, qué archivos deben crear, qué clase debe tener cada uno y qué `objectName` debe llevar cada componente para que el código Python lo encuentre sin cambios**.

### 3.1 Qué pide la rúbrica sobre interfaces

En el parcial la interfaz **no es obligatoria** (el entregable es un `.py`), pero suman presentación y dejan el terreno listo para el final. En el final sí es obligatoria y se califica así:

| Criterio del final | Componentes que deben aparecer | Dónde se usan en la biblioteca | Dónde se usan en el sistema académico |
|---|---|---|---|
| Interfaces gráficas básicas | `QLabel`, `QLineEdit`, `QTextEdit`, `QPushButton`, `QRadioButton`, `QCheckBox` | Acceso, catálogo, ficha, membresía, formularios. | Acceso, registro de estudiantes, observaciones, asistencia. |
| Componentes avanzados | `QSpinBox`, `QListWidget`, `QComboBox`, `QTableWidget`, `QCalendarWidget` | Estantes, ejemplares, filtros, tablas, fechas. | Notas, listas de alumnos, cursos, tablas de notas/asistencia, calendario. |
| Estructuras de secuencia | Flujo lógico entre ventanas y pasos | Acceso -> principal -> catálogo -> detalle -> volver. | Acceso -> principal -> curso -> calificaciones -> guardar -> reporte. |
| Estructuras de selección | `if`/`elif`/`else` en la lógica de la interfaz | Mostrar opciones de administrador solo si corresponde. | Mostrar notas, asistencia o reportes según el rol. |
| POO en la interfaz | Clases por ventana, encapsulación, herencia | `VentanaAcceso`, `VentanaPrincipal`, etc. | `VentanaCalificaciones`, `VentanaAsistencia`, etc. |

### 3.2 Qué hacer con las `.ui` que ya existen

Las cinco interfaces actuales (`acceso.ui`, `principal.ui`, `catalogo.ui`, `usuarios.ui`, `membresia.ui`) tienen una estructura rescatable: `QMainWindow` -> `centralwidget` -> layouts -> tarjetas -> botones. El problema es que se generaron con IA y **no se ven bien**. No hace falta botarlas todas: se pueden limpiar y renombrar. Lo que sí hay que hacer es:

1. **Recuperarlas del historial de Git** (están borradas del área de trabajo):
   ```bash
   cd /mnt/Compartido/1IDT/CI2/programacion_orientada_a_objetos/proyecto_parcial
   git restore interfaces/
   ```
2. **Separar el estilo del diseño.** Hoy cada `.ui` tiene un `styleSheet` enorme escrito a mano. Eso hace que se vea distinto en cada ventana y sea difícil de mantener. Crear un solo archivo `interfaces/estilos.qss` y cargarlo al arrancar:
   ```python
   from pathlib import Path

   def cargar_estilos(ventana):
       ruta = Path(__file__).resolve().parent / "estilos.qss"
       if ruta.exists():
           ventana.setStyleSheet(ruta.read_text(encoding="utf-8"))
   ```
3. **Usar layouts, no posiciones absolutas.** En QtDesigner, seleccionar la ventana y aplicar `Lay out` (Vertical/Horizontal/Grid/Form). Si un widget queda con geometría fija, se rompe al cambiar de resolución.
4. **Nombrar los widgets exactamente como los espera el código.** Si un compañero le pone `lineEdit_2` al DNI, el código no lo encuentra. La tabla de la sección 3.4 es el contrato.
5. **No poner lógica dentro del `.ui`.** Las conexiones `clicked -> método` se hacen en Python, no en QtDesigner. Así el diseño se puede cambiar sin romper la lógica.
6. **Revisar en dos tamaños:** 1024x768 y 1366x768. Si en alguno se corta un botón, falta un layout o un `QSpacerItem`.

### 3.3 Convención de nombres

| Tipo de elemento | Convención | Ejemplos |
|---|---|---|
| Archivo `.ui` | `snake_case.ui` | `acceso.ui`, `libro_form.ui`, `reportes.ui` |
| Clase de la ventana | `PascalCase`, empieza con `Ventana` | `VentanaAcceso`, `VentanaPrestamo` |
| Ventana principal | `VentanaPrincipal` | `principal.ui` |
| Formulario modal | `Ventana` + sustantivo | `VentanaLibro`, `VentanaPrestamo` |
| `QLabel` | `...Label` | `tituloLabel`, `estadoValorLabel`, `ayudaLabel` |
| `QLineEdit` | `...LineEdit` | `dniLineEdit`, `isbnLineEdit`, `buscarLineEdit` |
| `QTextEdit` | `...TextEdit` | `observacionesTextEdit`, `reporteTextEdit` |
| `QPushButton` | `...Button` | `entrarButton`, `guardarButton`, `volverButton` |
| `QRadioButton` | `...RadioButton` | `presenteRadioButton`, `ausenteRadioButton` |
| `QCheckBox` | `...CheckBox` | `soloDisponiblesCheckBox`, `justificadoCheckBox` |
| `QSpinBox` | `...SpinBox` | `estanteSpinBox`, `ejemplaresSpinBox`, `notaSpinBox` |
| `QComboBox` | `...ComboBox` | `categoriaComboBox`, `cursoComboBox` |
| `QListWidget` | `...ListWidget` | `estudiantesListWidget`, `resultadosListWidget` |
| `QTableWidget` | `...TableWidget` o `tabla...` | `tablaLibros`, `tablaUsuarios`, `tablaReporte` |
| `QCalendarWidget` | `...CalendarWidget` | `fechaPrestamoCalendarWidget`, `fechaAsistenciaCalendarWidget` |
| Grupo de botones | `...ButtonGroup` | `estadoAsistenciaButtonGroup` |

**Regla de oro:** el nombre debe decir qué dato guarda o qué acción dispara. `lineEdit_2` no dice nada; `dniLineEdit` sí.

### 3.4 Juego de ventanas para el parcial (biblioteca)

Estos son los archivos que deben existir en `interfaces/`. Los cinco primeros ya están en Git; los cuatro últimos hay que crearlos.

| Archivo `.ui` | Clase | Tipo | Para qué sirve | Prioridad |
|---|---|---|---|---|
| `acceso.ui` | `VentanaAcceso` | `QMainWindow` | Ingreso con DNI. | Alta |
| `principal.ui` | `VentanaPrincipal` | `QMainWindow` | Panel principal con accesos a catálogo, usuarios, membresía, préstamos, devoluciones y reportes. | Alta |
| `catalogo.ui` | `VentanaCatalogo` | `QMainWindow` | Listar, buscar y ver libros. | Alta |
| `usuarios.ui` | `VentanaUsuarios` | `QMainWindow` | Listar, buscar y gestionar usuarios. | Alta |
| `membresia.ui` | `VentanaMembresia` | `QMainWindow` | Ver la membresía del usuario conectado. | Alta |
| `libro_form.ui` | `VentanaLibro` | `QDialog` | Registrar o editar un libro. | Alta |
| `prestamo.ui` | `VentanaPrestamo` | `QDialog` | Registrar un préstamo. | Alta |
| `devolucion.ui` | `VentanaDevolucion` | `QDialog` | Registrar una devolución y calcular multa. | Alta |
| `reportes.ui` | `VentanaReportes` | `QMainWindow` | Ver las matrices y exportarlas. | Media |
| `estilos.qss` | — | Hoja de estilo | Colores, tipografía, espaciado y estados. | Media |

### 3.5 Especificación de cada ventana

#### `acceso.ui` — `VentanaAcceso`

**Propósito:** que el usuario entre con su DNI y que el sistema valide existencia, estado y vigencia.

| `objectName` | Widget | Configuración | Texto / uso |
|---|---|---|---|
| `tituloLabel` | `QLabel` | Fuente grande, negrita | “Biblioteca Universitaria” |
| `subtituloLabel` | `QLabel` | Texto secundario | “Ingresa tu DNI para continuar” |
| `dniLineEdit` | `QLineEdit` | `maxLength = 8`, `placeholderText = "8 dígitos"`, `QIntValidator(0, 99999999)` | DNI |
| `entrarButton` | `QPushButton` | `default = True` | “Ingresar” |
| `salirButton` | `QPushButton` | Estilo secundario | “Salir” |
| `ayudaLabel` | `QLabel` | Texto pequeño, rojo si hay error | “Usa el DNI registrado” |

**Señales que se conectan en Python:**

| Señal | Método | Qué hace |
|---|---|---|
| `entrarButton.clicked` | `VentanaAcceso.entrar` | Valida el DNI y abre `VentanaPrincipal`. |
| `dniLineEdit.returnPressed` | `VentanaAcceso.entrar` | Permite entrar con Enter. |
| `salirButton.clicked` | `VentanaAcceso.close` | Cierra la aplicación. |

**Criterio de aceptación:** un DNI inválido muestra un `QMessageBox` con el mensaje del `ErrorDeDatos`; un DNI de baja o vencido muestra su mensaje; un DNI válido abre el panel con el nombre y el tipo del usuario.

#### `principal.ui` — `VentanaPrincipal`

**Propósito:** ser el menú central. Debe mostrar el resumen y habilitar solo lo que el rol permite.

| `objectName` | Widget | Configuración | Texto / uso |
|---|---|---|---|
| `bienvenidaLabel` | `QLabel` | Fuente mediana | “Hola, {nombre} ({tipo})” |
| `resumenLabel` | `QLabel` | Texto secundario | “22 títulos, 13 usuarios, 4 préstamos activos” |
| `catalogoButton` | `QPushButton` | Tarjeta grande | “LIBROS / Ver catálogo” |
| `buscarMenuButton` | `QPushButton` | Tarjeta grande | “BUSCAR / Buscar por título o autor” |
| `usuariosButton` | `QPushButton` | Tarjeta grande, solo admin | “USUARIOS / Gestionar usuarios” |
| `membresiaButton` | `QPushButton` | Tarjeta grande | “MEMBRESÍA / Ver mi membresía” |
| `prestamosButton` | `QPushButton` | Tarjeta grande | “PRÉSTAMOS / Registrar préstamo” |
| `devolucionesButton` | `QPushButton` | Tarjeta grande | “DEVOLUCIONES / Registrar devolución” |
| `reportesButton` | `QPushButton` | Tarjeta grande, solo admin | “REPORTES / Matrices y resumen” |
| `cerrarSesionButton` | `QPushButton` | Estilo secundario | “Cerrar sesión” |

**Lógica de visibilidad:**

```python
self.usuariosButton.setVisible(usuario.puede_administrar())
self.reportesButton.setVisible(usuario.puede_administrar())
```

**Criterio de aceptación:** un estudiante no ve “Usuarios” ni “Reportes”; un administrador sí. Cada botón abre la ventana correcta y “Cerrar sesión” vuelve a `VentanaAcceso`.

#### `catalogo.ui` — `VentanaCatalogo`

**Propósito:** listar el catálogo, buscar por texto y abrir la ficha de un libro.

| `objectName` | Widget | Configuración | Texto / uso |
|---|---|---|---|
| `buscarLineEdit` | `QLineEdit` | `placeholderText = "Título, autor, ISBN o categoría"` | Búsqueda |
| `categoriaComboBox` | `QComboBox` | Primera opción “Todas las categorías” | Filtro por categoría |
| `soloDisponiblesCheckBox` | `QCheckBox` | Desmarcado por defecto | “Solo disponibles para prestar” |
| `buscarButton` | `QPushButton` | — | “Buscar” |
| `limpiarButton` | `QPushButton` | Estilo secundario | “Mostrar todos” |
| `tablaLibros` | `QTableWidget` | 10 columnas, `alternatingRowColors = True`, selección por fila | Resultados |
| `verButton` | `QPushButton` | — | “Ver detalles” |
| `volverButton` | `QPushButton` | Estilo secundario | “Volver al menú” |
| `ayudaLabel` | `QLabel` | Texto pequeño | “Doble clic para ver la ficha” |

**Columnas de `tablaLibros`:**

1. ISBN
2. Título
3. Autor
4. Categoría
5. Sección
6. Estante
7. Ejemplares
8. Disponibles
9. Prestados
10. Estado

**Señales:**

| Señal | Método | Qué hace |
|---|---|---|
| `buscarButton.clicked` | `buscar` | Llama a `biblioteca.buscar(texto)`. |
| `limpiarButton.clicked` | `mostrar_todos` | Llama a `biblioteca.datos_del_catalogo()`. |
| `verButton.clicked` | `ver_detalle` | Abre la ficha del libro seleccionado. |
| `tablaLibros.cellDoubleClicked` | `ver_detalle` | Mismo comportamiento con doble clic. |
| `volverButton.clicked` | `close` | Vuelve al panel principal. |

**Criterio de aceptación:** la tabla se llena con 22 libros, la búsqueda por “arte” devuelve 4, la búsqueda vacía no rompe y el botón “Mostrar todos” restaura la lista.

#### `usuarios.ui` — `VentanaUsuarios`

**Propósito:** listar, buscar y gestionar membresías. Solo para administradores.

| `objectName` | Widget | Configuración | Texto / uso |
|---|---|---|---|
| `buscarLineEdit` | `QLineEdit` | `placeholderText = "DNI, nombre o tipo"` | Búsqueda |
| `tipoComboBox` | `QComboBox` | “Todos”, “Estudiante”, “Docente”, “Administrador” | Filtro |
| `buscarButton` | `QPushButton` | — | “Buscar” |
| `limpiarButton` | `QPushButton` | Estilo secundario | “Mostrar todos” |
| `tablaUsuarios` | `QTableWidget` | 6 columnas, selección por fila | Resultados |
| `nuevoButton` | `QPushButton` | — | “Nuevo usuario” |
| `editarButton` | `QPushButton` | — | “Editar” |
| `bajaButton` | `QPushButton` | Estilo de peligro | “Dar de baja” |
| `reactivarButton` | `QPushButton` | — | “Reactivar” |
| `renovarButton` | `QPushButton` | — | “Renovar membresía” |
| `volverButton` | `QPushButton` | Estilo secundario | “Volver al menú” |

**Columnas de `tablaUsuarios`:**

1. DNI
2. Nombre
3. Tipo
4. Vencimiento
5. Estado
6. Préstamos activos

**Criterio de aceptación:** se puede crear un usuario, darlo de baja, reactivarlo y renovarlo; la tabla se actualiza después de cada operación; un usuario de baja no puede entrar al sistema.

#### `membresia.ui` — `VentanaMembresia`

**Propósito:** mostrar la membresía del usuario conectado, con sus beneficios.

| `objectName` | Widget | Texto / uso |
|---|---|---|
| `nombreValorLabel` | `QLabel` | Nombre del usuario |
| `dniValorLabel` | `QLabel` | DNI |
| `tipoValorLabel` | `QLabel` | Estudiante / Docente / Administrador |
| `vencimientoValorLabel` | `QLabel` | Fecha de vencimiento |
| `estadoValorLabel` | `QLabel` | Activo / De baja / Vencida |
| `beneficiosLabel` | `QLabel` | “3 préstamos, 15 días, 0 % de descuento” |
| `volverButton` | `QPushButton` | “Volver al menú” |

**Criterio de aceptación:** los datos coinciden con el usuario que inició sesión y el estado se calcula con `date.today()`.