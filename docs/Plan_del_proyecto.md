# Plan del proyecto — Sistema de Biblioteca y Sistema Académico

> Documento de trabajo del equipo. Reúne el estado real del repositorio, lo que falta, cómo se conectan las pantallas con la lógica y el orden en que conviene construir cada parte. Está pensado para que los cuatro integrantes puedan tomar tareas sin depender de memoria o de mensajes sueltos.

## Contenido

1. [Cómo usar este plan](#1-cómo-usar-este-plan)
2. [Visión y alcance](#2-visión-y-alcance)
3. [Estado actual del proyecto](#3-estado-actual-del-proyecto)
4. [Forma de trabajo del equipo](#4-forma-de-trabajo-del-equipo)
5. [Arquitectura objetivo](#5-arquitectura-objetivo)
6. [Modelo de dominio de la biblioteca](#6-modelo-de-dominio-de-la-biblioteca)
7. [Funcionalidades por módulo](#7-funcionalidades-por-módulo)
8. [Matrices y recursividad](#8-matrices-y-recursividad)
9. [Persistencia y manejo de archivos](#9-persistencia-y-manejo-de-archivos)
10. [Interfaces gráficas](#10-interfaces-gráficas)
11. [Backlog priorizado](#11-backlog-priorizado)
12. [Cronograma de trabajo](#12-cronograma-de-trabajo)
13. [Pruebas](#13-pruebas)
14. [Sistema académico del segundo entregable](#14-sistema-académico-del-segundo-entregable)
15. [Documentación y presentación](#15-documentación-y-presentación)
16. [Riesgos y cómo reducirlos](#16-riesgos-y-cómo-reducirlos)
17. [Checklist antes de cada entrega](#17-checklist-antes-de-cada-entrega)
18. [Anexos](#18-anexos)

---

## 1. Cómo usar este plan

Este documento no es una lista de deseos: es la guía de construcción del proyecto. Se usa así:

1. Antes de empezar una tarea, busca su código en el [backlog](#11-backlog-priorizado) y lee su criterio de aceptación.
2. Si la tarea toca lógica de negocio, trabaja primero en `core/` y deja la interfaz para después.
3. Si la tarea toca una pantalla, respeta los nombres de widgets de la [sección 10](#10-interfaces-gráficas) para que el código las encuentre sin cambios.
4. Al terminar, actualiza el checklist y avisa al equipo qué quedó probado.
5. Si aparece una decisión nueva, se agrega aquí. El plan debe seguir siendo la fuente de verdad del proyecto.

Reglas generales:

- Una tarea no se considera terminada solo porque “compila”: tiene que funcionar con los datos reales, mostrar mensajes claros y no romper lo anterior.
- Ninguna ventana lee archivos JSON directamente. Todo pasa por `Biblioteca`.
- Ninguna clase de negocio imprime en consola ni muestra `QMessageBox`. Devuelve datos o lanza excepciones; la interfaz decide cómo mostrarlos.
- Los nombres importantes describen el dominio: `Prestamo`, `prestar_ejemplar`, `mapa_de_estantes`, `historial_por_usuario`. No se usan nombres como `aux`, `dato1`, `matriz`, `x` o `temporal`.

---

## 2. Visión y alcance

### 2.1 Producto del primer entregable: biblioteca universitaria

El sistema debe gestionar libros, usuarios, membresías, préstamos y devoluciones de una biblioteca universitaria. El producto debe permitir:

- registrar libros con validación de datos;
- actualizar la información de un libro existente;
- listar, buscar y consultar libros por ISBN, título, autor o categoría;
- registrar, modificar, dar de baja, reactivar y renovar membresías;
- prestar ejemplares, controlando disponibilidad y límites por usuario;
- devolver ejemplares, actualizando la disponibilidad y calculando multas por retraso;
- generar reportes con matrices de disponibilidad, devoluciones pendientes, historial y penalizaciones;
- conservar la información en archivos JSON y dejar una bitácora de texto de las operaciones;
- demostrar clases, encapsulación, herencia, polimorfismo, excepciones, modularidad, matrices y recursividad.

El primer entregable debe poder ejecutarse de dos formas:

```bash
# Versión de consola
python3 main.py

# Versión gráfica
python3 main_gui.py
```

### 2.2 Producto del segundo entregable: sistema académico

El segundo contexto es un sistema de gestión de calificaciones y asistencia para docentes. Debe incluir:

- interfaz gráfica con PyQt5 y QtDesigner;
- registro de estudiantes, cursos, calificaciones y asistencias;
- componentes básicos y avanzados;
- archivos de texto y binarios;
- búsqueda y reemplazo de texto con expresiones regulares;
- reportes personalizados;
- documentación y presentación del funcionamiento.

La biblioteca no se tira: se conserva como base de arquitectura, estilo de código y ejemplos de POO. El sistema académico se construye como un módulo separado que reutiliza las decisiones que ya funcionan.

### 2.3 Fuera de alcance por ahora

Para no dispersar el trabajo:

- no se implementará autenticación con contraseña en la primera etapa;
- no se conectará a una base de datos externa;
- no se usarán APIs de internet;
- no se agregarán dependencias que no sean PyQt5 y la biblioteca estándar de Python;
- no se reescribirá el proyecto desde cero.

### 2.4 Cobertura del sílabo y de los criterios de evaluación

Esta tabla sirve para revisar que el proyecto no deje temas sin evidencia. No es una lista de notas: es un mapa de “dónde se ve” cada tema y “qué falta”.

| Tema del sílabo | Dónde se evidencia | Qué falta |
| --- | --- | --- |
| 01. Fundamentos de Python | `core/`, menús, `if`, `for`, `while`, listas y diccionarios | Más pruebas de casos límite |
| 02. Principios de POO | `Libro`, `Usuario`, `Administrador`, `Biblioteca`, atributos privados y constructores | `Prestamo` y jerarquía de usuarios |
| 03. Métodos y funciones | Métodos de lectura, fábricas, módulos, excepciones y métodos de cadena | Funciones de escritura y pruebas |
| 04. Matrices y recursividad | Búsquedas y filtros recursivos del catálogo | Cuatro matrices y recursión sobre matrices |
| 05. Herencia y polimorfismo | `Administrador(Usuario)`, `puede_administrar()`, `datos_de_membresia()` | Subclases `Estudiante` y `Docente` |
| 06. Interfaces básicas | `acceso.ui`, `principal.ui`, `catalogo.ui`, labels, line edits, text edits y push buttons | Formularios de operaciones |
| 07. Componentes avanzados | `QComboBox`, `QSpinBox`, `QTableWidget`, `QListWidget` y `QTextEdit` | `QCalendarWidget`, `QRadioButton` y `QCheckBox` de asistencia |
| 08. Manejo de archivos | Lectura de JSON, reportes `.txt` | Escritura de JSON, bitácora y archivo binario |
| 09. Procesamiento de texto | Búsqueda normalizada y reportes | Expresiones regulares y reemplazo de texto |

| Criterio de evaluación | Dónde se cubre | Tareas que lo completan |
| --- | --- | --- |
| Funcionalidad del sistema | Catálogo, búsqueda, acceso, roles y reporte | LIB, USR, PRE, PER |
| Aplicación de POO | Clases, encapsulación, herencia y polimorfismo | PRE-01, USR-01, jerarquía de usuarios |
| Uso de funciones y métodos | Métodos de dominio, parámetros, retornos y excepciones | LIB, USR, PRE, QA |
| Matrices y recursividad | Búsqueda recursiva y filtros | REP-01 a REP-07 |
| Interfaces gráficas | Acceso, panel, catálogo y navegación | LIB-04, USR-03, PRE-06, PRE-07, REP-08 |
| Manejo de archivos | Lectura JSON y exportación de reportes | PER-01, PER-02, PRE-08 |
| Procesamiento de texto | Búsqueda sin tildes y reportes | Sistema académico y búsqueda jerárquica |

---

## 3. Estado actual del proyecto

### 3.1 Estructura actual

```text
proyecto_parcial/
├── main.py                     entrada de la versión de consola
├── main_gui.py                 entrada de la versión gráfica
├── README.md
├── core/
│   ├── configuracion.py        rutas, secciones, estantes, archivos, reglas
│   ├── errores.py              ErrorBiblioteca, ErrorDeDatos, ErrorDeArchivo
│   ├── utilidades.py           DNI, ISBN, fechas, pausa
│   ├── libros.py               Libro, búsqueda y filtros recursivos
│   ├── usuarios.py             Usuario, Administrador y fábrica
│   ├── biblioteca.py           controlador del catálogo y usuarios
│   └── menu.py                 menú de consola
├── datos/
│   ├── libros.json             22 libros
│   ├── usuarios.json           13 usuarios
│   └── reportes/               se crea al exportar un reporte
├── ui/
│   ├── acceso.ui               pantalla de ingreso
│   ├── acceso.py               carga acceso.ui y valida el DNI
│   ├── principal.ui            panel principal
│   ├── principal.py            carga principal.ui y conecta la navegación
│   ├── catalogo.ui             catálogo con buscador y ficha
│   ├── catalogo.py             carga catalogo.ui y consulta a Biblioteca
│   └── __init__.py
├── recursos/
│   ├── imagenes/               imágenes de la interfaz
│   ├── iconos/                 iconos de botones y ventanas
│   └── README.md               cómo nombrar y cargar los recursos
├── docs/
│   ├── Plan_del_proyecto.md    este documento
│   ├── Guia_base.md
│   ├── Guia_base.ipynb
│   └── PDFs del sílabo y las rúbricas
└── tests/
    ├── test_biblioteca.py      pruebas del catálogo y usuarios
    ├── a.py                    apuntes de clase
    └── pr.py                   apuntes de clase
```

### 3.2 Lo que ya funciona

- **Clases y objetos:** `Libro`, `Usuario`, `Administrador` y `Biblioteca`.
- **Encapsulación:** atributos privados con `_` y métodos de lectura.
- **Herencia:** `Administrador(Usuario)`.
- **Polimorfismo:** `puede_administrar()` y `datos_de_membresia()` responden distinto según la clase.
- **Constructores con valores por defecto:** `Usuario(dni, nombre, tipo="Estudiante", ...)`.
- **Excepciones propias:** `ErrorBiblioteca`, `ErrorDeDatos` y `ErrorDeArchivo`.
- **Validaciones:** DNI de 8 dígitos, ISBN de 13 dígitos, fechas reales, sección, estante, ejemplares y disponibles.
- **Recursividad:** búsqueda y filtros del catálogo.
- **Lectura de JSON:** catálogo y usuarios, con mensaje claro si el archivo está mal escrito.
- **Menú de consola:** acceso, catálogo, búsqueda, ficha por ISBN, membresía y usuarios.
- **Interfaz gráfica:** acceso, panel principal, catálogo con búsqueda por ISBN/título/autor/categoría, filtro por categoría, filtro de disponibles, orden, límite de resultados y ficha formateada.
- **Roles:** el estudiante no ve las opciones de administración; el administrador sí.
- **Reporte:** resumen general, disponibilidad por sección y títulos por categoría, con exportación a `.txt`.
- **Pruebas automatizadas:** 14 casos del catálogo, búsquedas, usuarios y reglas de disponibilidad en `tests/test_biblioteca.py`.

### 3.3 Lo que falta

| Falta | Dónde se nota | Prioridad |
| --- | --- | --- |
| Clase `Prestamo` y archivo `prestamos.json` | No existe el ciclo completo de préstamo | Alta |
| Prestar y devolver desde el sistema | Solo se consulta el catálogo | Alta |
| Actualizar disponibilidad al prestar y devolver | Los ejemplares no cambian | Alta |
| Registrar y editar libros desde la interfaz | El catálogo solo se edita en el JSON | Alta |
| Alta, baja, reactivación y renovación de membresías | No hay operaciones de gestión | Alta |
| Cálculo de multas y tope | No hay fechas reales de préstamo | Alta |
| Persistencia de cambios | Solo se lee; no se guarda | Alta |
| Matrices de reportes | No existen las cuatro matrices del dominio | Alta |
| Recursividad sobre matrices | Solo hay recursión sobre listas | Media |
| Jerarquía de categorías | Las categorías son planas | Media |
| Bitácora de operaciones | No se registra el historial | Media |
| Formularios de libro, préstamo y devolución | Faltan pantallas | Media |
| Pruebas de préstamos y reportes | `tests/` cubre catálogo y usuarios, no circulación | Media |
| Sistema académico | Es el segundo entregable | Alta para la siguiente etapa |
| Presentación y documentación final | Pendiente | Media |

### 3.4 Deuda técnica que conviene resolver primero

1. **Separar apuntes de pruebas reales.** `tests/a.py` y `tests/pr.py` son ejercicios de clase. Se moverán a `docs/ejemplos/` o se dejarán fuera del entregable, y se creará `tests/test_biblioteca.py` con pruebas del dominio.
2. **Evitar que la interfaz tenga reglas de negocio.** La ventana solo debe pedir datos, llamar a `Biblioteca` y mostrar resultados.
3. **Interfaz sin estilos por ahora.** Se usa el aspecto básico de Qt. Los colores, tamaños y hojas de estilo se agregan al final, cuando la funcionalidad esté cerrada.
4. **Nombre, lema y rutas centralizados.** El nombre y el lema salen de `core/configuracion.py`; las imágenes e iconos se buscan con `ruta_de_imagen()` y `ruta_de_icono()`. No se repiten textos ni rutas en cada ventana.
5. **Nombres de widgets estables.** Una vez definido el contrato de `objectName`, no se cambia sin actualizar el `.py` correspondiente.
6. **Mensajes de error claros.** Todo error esperado se lanza como `ErrorBiblioteca` y se muestra en la interfaz; nunca se deja un traceback al usuario.
7. **No duplicar datos.** Las matrices y los reportes se calculan desde el catálogo y los préstamos; no se guardan en el JSON.

---

## 4. Forma de trabajo del equipo

### 4.1 Roles

Son cuatro desarrolladores. Los roles no son dueños absolutos del código: sirven para saber quién lidera cada frente y quién revisa.

| Rol | Responsabilidad principal | Entregables |
| --- | --- | --- |
| **Dev 1 — Dominio de libros** | `Libro`, catálogo, búsqueda, filtros, CRUD de libros y persistencia del catálogo | `core/libros.py`, formulario de libro, pruebas del catálogo |
| **Dev 2 — Usuarios y membresías** | `Usuario`, `Administrador`, alta/baja/reactivación/renovación, validaciones | `core/usuarios.py`, formulario de usuario, pruebas de membresías |
| **Dev 3 — Circulación y reportes** | `Prestamo`, préstamos, devoluciones, multas, matrices y recursividad | `core/prestamos.py`, reportes, pruebas de circulación |
| **Dev 4 — Interfaz e integración** | Ventanas `.ui`, conexión con `core/`, estilos, flujo entre pantallas, QA | `ui/`, `main_gui.py`, pruebas manuales, documentación |

Reglas de convivencia:

- Cada tarea tiene un responsable y un revisor.
- Nadie hace merge de su propia rama sin que otro la haya probado.
- Los cambios de dominio se aprueban con el Dev 3 y el Dev 1; los cambios de interfaz, con el Dev 4.
- Si una tarea bloquea a otra, se avisa en la reunión y se reparte de nuevo.

### 4.2 Flujo de Git

```bash
# actualizar la rama principal
git switch main
git pull origin main

# crear una rama por tarea
git switch -c feature/prestamos

# trabajar, probar y confirmar
git add .
git commit -m "Agrega registro de prestamos y actualiza disponibilidad"

# subir y pedir revision
git push -u origin feature/prestamos
```

Convenciones:

- Ramas: `feature/...`, `fix/...`, `docs/...`, `ui/...`.
- Commits en presente y en español: `Agrega`, `Corrige`, `Documenta`, `Conecta`.
- Un commit no mezcla lógica, estilos y documentación sin relación.
- Antes de hacer merge: ejecutar el sistema, probar el caso feliz y al menos un caso de error.

### 4.3 Convenciones de código

- Archivos y funciones en `snake_case`.
- Clases en `PascalCase`.
- Constantes en `MAYUSCULAS`.
- Atributos privados con `_` al inicio.
- Métodos de lectura con el nombre del dato: `libro.titulo()`, `usuario.dni()`.
- Mensajes al usuario en español, sin tildes dentro del código para evitar problemas de codificación, pero con tildes en los textos de la interfaz cuando se cargan desde `.ui` o desde cadenas con `utf-8`.
- Docstring corto en cada clase y método público.
- Una función hace una cosa; si necesita tres párrafos para explicarse, se divide.

### 4.4 Definition of Done

Una tarea está terminada cuando:

- [ ] El código funciona con los datos reales del proyecto.
- [ ] Tiene validaciones y mensajes de error claros.
- [ ] No rompe las pruebas existentes.
- [ ] Está probada desde la consola o desde la interfaz, según corresponda.
- [ ] El revisor la probó en su máquina.
- [ ] La documentación o el checklist se actualizaron.
- [ ] No quedan `print()` de depuración ni rutas absolutas personales.

### 4.5 Reuniones

- **Inicio de semana:** 20 minutos. Se reparten tareas del backlog y se revisan bloqueos.
- **Mitad de semana:** 15 minutos. Solo bloqueos y pruebas.
- **Cierre de semana:** 30 minutos. Demo de lo terminado, revisión de ramas y actualización del plan.
- **Regla:** si una decisión cambia el alcance, se escribe en este documento; no se decide solo por chat.

---

## 5. Arquitectura objetivo

### 5.1 Capas

```text
┌──────────────────────────────────────────────┐
│ ui/                                          │
│ Ventanas Qt, widgets, validación de formulario│
│ No leen JSON. No calculan multas.            │
└──────────────────────┬───────────────────────┘
                       │ llama métodos y recibe diccionarios
┌──────────────────────▼───────────────────────┐
│ core/                                        │
│ Biblioteca, Libro, Usuario, Prestamo,         │
│ reportes, reglas de negocio y excepciones     │
└──────────────────────┬───────────────────────┘
                       │ lee y escribe
┌──────────────────────▼───────────────────────┐
│ datos/                                       │
│ libros.json, usuarios.json, prestamos.json,   │
│ bitacora.txt, reportes/                       │
└──────────────────────────────────────────────┘
```

Regla de dependencias:

- `ui/` puede importar `core/`.
- `core/` no puede importar `ui/`.
- `core/` no muestra mensajes gráficos.
- `datos/` no contiene lógica.
- `main.py` y `main_gui.py` son puntos de entrada; no contienen reglas de negocio.

### 5.2 Estructura objetivo completa

```text
proyecto_parcial/
├── main.py
├── main_gui.py
├── core/
│   ├── configuracion.py
│   ├── errores.py
│   ├── utilidades.py
│   ├── libros.py
│   ├── usuarios.py
│   ├── prestamos.py          ← nuevo
│   ├── reportes.py           ← nuevo
│   ├── archivos.py           ← nuevo: guardar JSON, bitácora, reportes
│   ├── biblioteca.py
│   └── menu.py
├── ui/
│   ├── acceso.ui / acceso.py
│   ├── principal.ui / principal.py
│   ├── catalogo.ui / catalogo.py
│   ├── libro_form.ui / libro_form.py
│   ├── usuario_form.ui / usuario_form.py
│   ├── prestamo.ui / prestamo.py
│   ├── devolucion.ui / devolucion.py
│   └── reportes.ui / reportes.py
├── recursos/
│   ├── imagenes/
│   ├── iconos/
│   └── README.md
├── datos/
│   ├── libros.json
│   ├── usuarios.json
│   ├── prestamos.json
│   ├── bitacora.txt
│   └── reportes/
├── tests/
│   ├── test_biblioteca.py
│   ├── test_prestamos.py
│   ├── test_reportes.py
│   └── test_archivos.py
└── docs/
```

### 5.3 Cómo se conecta una pantalla con el núcleo

El patrón es siempre el mismo:

```python
# ui/catalogo.py
class VentanaCatalogo(QWidget):
    def __init__(self, biblioteca, parent=None):
        super().__init__(parent)
        self.biblioteca = biblioteca
        self.buscarButton.clicked.connect(self.buscar)

    def buscar(self):
        datos = self.biblioteca.buscar_avanzado(
            texto=self.buscarLineEdit.text(),
            campo=self.campoComboBox.currentData(),
            categoria=self.categoriaComboBox.currentData() or "",
            solo_disponibles=self.soloDisponiblesCheckBox.isChecked(),
        )
        self.llenar_tabla(datos)
```

Lo importante:

1. La ventana recibe `biblioteca` en el constructor.
2. La ventana no crea libros ni modifica JSON.
3. La ventana pide datos y los muestra.
4. Si `Biblioteca` lanza una excepción, la ventana la convierte en un mensaje para el usuario.
5. Los formularios entregan datos a `Biblioteca` y, si la operación sale bien, se cierran y actualizan la tabla.

---

## 6. Modelo de dominio de la biblioteca

### 6.1 Clases actuales

| Clase | Responsabilidad | Estado |
| --- | --- | --- |
| `Libro` | Datos, validaciones, disponibilidad y diccionarios para pantalla | Completa para consulta |
| `Usuario` | Datos de la cuenta, estado y vigencia | Completa para consulta |
| `Administrador` | Usuario con permisos y datos extra | Completa |
| `Biblioteca` | Catálogo, usuarios, búsquedas y resumen | Parcial |
| `Prestamo` | Préstamo, fechas, devolución y multa | Pendiente |
| `Reportes` | Matrices y cálculos de reportes | Pendiente |

### 6.2 Clases que hay que agregar

#### `Prestamo`

```python
class Prestamo:
    def __init__(self, codigo, isbn, dni, fecha_prestamo, fecha_limite,
                 fecha_devolucion=None):
        ...
```

Responsabilidades:

- guardar el código único del préstamo;
- guardar ISBN, DNI, fecha de préstamo y fecha límite;
- saber si está activo o devuelto;
- calcular días de retraso;
- calcular multa con tope;
- devolver un diccionario para el JSON y otro para pantalla.

Métodos mínimos:

| Método | Qué devuelve |
| --- | --- |
| `codigo()` | código del préstamo |
| `isbn()` | ISBN prestado |
| `dni()` | DNI del usuario |
| `fecha_prestamo()` | fecha en que salió |
| `fecha_limite()` | fecha máxima de devolución |
| `fecha_devolucion()` | fecha real o `None` |
| `esta_activo()` | `True` si no fue devuelto |
| `esta_vencido()` | `True` si sigue activo y pasó la fecha límite |
| `dias_de_retraso()` | días de retraso al día de hoy o a la devolución |
| `calcular_multa()` | monto con tope |
| `a_diccionario()` | datos para `prestamos.json` |
| `datos_para_pantalla()` | datos listos para tabla o reporte |

#### `Reportes`

No necesita guardar estado. Recibe el catálogo y los préstamos y devuelve matrices.

```python
class Reportes:
    def __init__(self, biblioteca):
        self.biblioteca = biblioteca

    def mapa_de_estantes(self):
        ...

    def agenda_de_devoluciones(self):
        ...

    def historial_por_usuario(self):
        ...

    def penalizaciones_por_usuario(self):
        ...
```

### 6.3 Relaciones

```text
Biblioteca 1 ─── * Libro
Biblioteca 1 ─── * Usuario
Biblioteca 1 ─── * Prestamo
Usuario    1 ─── * Prestamo
Libro      1 ─── * Prestamo
```

- Un libro puede tener muchos préstamos históricos, pero solo algunos activos.
- Un usuario puede tener varios préstamos históricos, con un máximo de préstamos activos.
- Un préstamo pertenece a un solo libro y a un solo usuario.
- La disponibilidad del libro se descuenta al prestar y se devuelve al devolver.

### 6.4 Herencia y polimorfismo

Se mantiene `Administrador(Usuario)`. Además se puede agregar una jerarquía pequeña para los tipos de usuario:

```text
Usuario
├── Estudiante
├── Docente
└── Administrador
```

Cada subclase puede sobrescribir:

- `dias_de_prestamo()`: por ejemplo, 15 para estudiante y 30 para docente;
- `maximo_de_prestamos()`: distinto según el rol;
- `datos_de_membresia()`: agrega información propia;
- `puede_administrar()`: solo el administrador devuelve `True`.

Eso permite demostrar polimorfismo sin duplicar código: la biblioteca llama `usuario.dias_de_prestamo()` y cada clase responde lo suyo.

### 6.5 Excepciones

| Excepción | Cuándo se usa |
| --- | --- |
| `ErrorBiblioteca` | Base de todos los errores del dominio |
| `ErrorDeDatos` | DNI, ISBN, fecha, sección, estante o campo inválido |
| `ErrorDeArchivo` | JSON mal escrito, archivo que no se puede leer o escribir |
| `ErrorDePrestamo` | Libro no disponible, límite alcanzado, préstamo ya devuelto |

Las excepciones nuevas heredan de `ErrorBiblioteca` para que la interfaz pueda atraparlas todas con un solo `except`.

---

## 7. Funcionalidades por módulo

### 7.1 Libros

| Operación | Método propuesto | Reglas |
| --- | --- | --- |
| Listar | `datos_del_catalogo()` | Devuelve todos los libros |
| Buscar | `buscar_avanzado(...)` | Por texto, campo, categoría, disponibilidad, orden y límite |
| Consultar | `datos_de_un_libro(isbn)` | Valida el ISBN y lanza error si no existe |
| Registrar | `registrar_libro(datos)` | Valida todos los campos y evita ISBN repetido |
| Actualizar | `actualizar_libro(isbn, cambios)` | Solo cambia los campos permitidos |
| Eliminar | `eliminar_libro(isbn)` | Solo si no tiene préstamos activos |
| Ajustar ejemplares | `ajustar_ejemplares(isbn, cantidad)` | No puede quedar menos de lo prestado |
| Guardar | `guardar_catalogo()` | Escribe `libros.json` de forma segura |

Criterios de aceptación:

- No se puede registrar un libro con ISBN repetido.
- No se puede actualizar un libro con datos inválidos.
- No se puede eliminar un libro con préstamos activos.
- Después de guardar, al reiniciar el programa el cambio sigue ahí.

### 7.2 Usuarios y membresías

| Operación | Método propuesto | Reglas |
| --- | --- | --- |
| Listar | `datos_de_los_usuarios()` | Devuelve todos con su estado |
| Buscar | `buscar_usuarios(texto)` | Por DNI, nombre o tipo |
| Crear | `registrar_usuario(datos)` | DNI único, tipo válido, fecha válida |
| Actualizar | `actualizar_usuario(dni, cambios)` | Nombre, tipo y vencimiento |
| Dar de baja | `dar_de_baja(dni)` | No puede tener préstamos activos |
| Reactivar | `reactivar_usuario(dni)` | Debe tener membresía vigente o renovarla |
| Renovar | `renovar_membresia(dni, nueva_fecha)` | La fecha debe ser futura |
| Guardar | `guardar_usuarios()` | Escribe `usuarios.json` |

Criterios de aceptación:

- Un usuario de baja no puede iniciar sesión.
- Un usuario con membresía vencida no puede prestar.
- La renovación actualiza la fecha y el estado.
- La tabla de usuarios se actualiza después de cada operación.

### 7.3 Préstamos

| Operación | Método propuesto | Reglas |
| --- | --- | --- |
| Prestar | `prestar_ejemplar(isbn, dni)` | Usuario activo, membresía vigente, libro disponible, límite no superado |
| Listar activos | `prestamos_activos()` | Solo los no devueltos |
| Listar por usuario | `prestamos_de_usuario(dni)` | Historial completo |
| Consultar | `prestamo(codigo)` | Lanza error si no existe |
| Guardar | `guardar_prestamos()` | Escribe `prestamos.json` |

Reglas del préstamo:

1. El usuario debe existir, estar activo y tener membresía vigente.
2. El libro debe existir y tener más de un ejemplar disponible.
3. El usuario no puede superar su máximo de préstamos activos.
4. Al prestar, `disponibles` baja en 1 y el préstamo queda activo.
5. Se registra la operación en la bitácora.
6. Se guardan los cambios antes de mostrar el resultado.

### 7.4 Devoluciones y multas

| Operación | Método propuesto | Reglas |
| --- | --- | --- |
| Devolver | `devolver_ejemplar(codigo)` | El préstamo debe existir y estar activo |
| Calcular multa | `calcular_multa(prestamo)` | Días de retraso × tarifa, con tope |
| Registrar devolución | `registrar_devolucion(codigo)` | Actualiza fechas, disponibilidad y bitácora |
| Historial | `historial_de_prestamos()` | Todos los préstamos, activos y devueltos |

Reglas de la multa:

- Solo se cobra si la devolución ocurre después de la fecha límite.
- La multa se calcula por día de retraso.
- Tiene un tope configurado en `configuracion.TOPE_DE_MULTA`.
- La multa se muestra con dos decimales.
- Si el usuario devuelve a tiempo, la multa es 0.

### 7.5 Búsqueda avanzada

La pantalla de catálogo ya permite:

- buscar en todo el catálogo;
- buscar solo por ISBN;
- buscar solo por título;
- buscar solo por autor;
- buscar solo por categoría;
- filtrar por categoría;
- mostrar solo libros disponibles para prestar;
- ordenar por título, autor, categoría o más disponibles;
- limitar la cantidad de resultados;
- ver la ficha formateada del libro seleccionado.

El método central es:

```python
biblioteca.buscar_avanzado(
    texto="cien",
    campo="titulo",
    categoria="Literatura",
    solo_disponibles=False,
    ordenar_por="titulo",
    limite=100,
)
```

La búsqueda no distingue mayúsculas ni tildes. Así, `anos` encuentra `años` y `VARGAS` encuentra `Vargas`.

### 7.6 Resumen y reportes

El resumen general ya existe:

```python
{
    "biblioteca": "Biblioteca General POSTDATA",
    "fecha_de_hoy": "2026-11-08",
    "titulos": 22,
    "ejemplares": 45,
    "disponibles": 41,
    "prestados": 4,
    "usuarios": 13,
}
```

Los reportes nuevos deben salir de matrices, no de listas paralelas. En la sección 8 está el diseño.

---

## 8. Matrices y recursividad

### 8.1 Matrices del dominio

Las matrices son vistas calculadas. No se guardan en JSON. Se construyen cuando el usuario pide un reporte.

| Nombre | Filas | Columnas | Qué muestra |
| --- | --- | --- | --- |
| `mapa_de_estantes` | 5 secciones | 3 estantes | Títulos, ejemplares y disponibles por ubicación |
| `agenda_de_devoluciones` | Días próximos (0 a 7) | Tipos de usuario | Préstamos que vencen o están vencidos |
| `historial_por_usuario` | Usuarios | Histórico, activos, devueltos | Movimiento de cada usuario |
| `penalizaciones_por_usuario` | Usuarios | Multa, días de retraso, estado | Situación de cada usuario |

Ejemplo de `mapa_de_estantes`:

```text
          Estante 1   Estante 2   Estante 3
A           10/11        1/2         0/0
B            8/8         3/3         0/0
C            7/7         4/4         0/0
D            4/4         2/2         0/0
E            6/6         0/0         0/0
```

Cada celda puede ser una tupla `(disponibles, ejemplares)` o un diccionario con esos datos. Lo importante es que la matriz se construya a partir de los objetos del catálogo.

### 8.2 Funciones recursivas

Se mantienen las funciones recursivas actuales:

- `buscar_por_texto(libros, texto, campo)`: caso base `len(libros) == 0`; paso recursivo con `libros[1:]`.
- `filtrar_por_categoria(libros, categoria)`: caso base lista vacía; paso recursivo con el resto.
- `filtrar_solo_disponibles(libros)`: caso base lista vacía; paso recursivo con el resto.
- `datos_del_catalogo(libros)`: convierte la lista de objetos en lista de diccionarios.

Se agregan:

| Función | Qué hace | Caso base | Paso recursivo |
| --- | --- | --- | --- |
| `buscar_en_categoria(categorias, nombre)` | Busca en una jerarquía de categorías | categoría sin hijos | recorre las subcategorías |
| `contar_disponibles_en_seccion(mapa, fila, columna)` | Recorre una fila de la matriz | columna fuera de rango | suma la celda y avanza una columna |
| `sumar_existencias(mapa, fila, columna)` | Suma ejemplares de una sección | fila fuera de rango | suma la fila y avanza una fila |
| `buscar_prestamo_por_codigo(prestamos, codigo)` | Busca un préstamo en una lista | lista vacía | compara el primero y sigue con el resto |

### 8.3 Cómo explicar la recursividad

Para cada función recursiva se debe poder señalar:

1. **Caso base:** cuándo se detiene.
2. **Paso recursivo:** cómo se acerca al caso base.
3. **Acumulación:** qué se va sumando o guardando.
4. **Por qué no desborda la pila:** porque en cada llamada la lista o la matriz se hace más pequeña.

No basta con que “funcione”. En la defensa se debe poder explicar con el código abierto.

### 8.4 Jerarquía de categorías

Para la búsqueda en jerarquía se propone esta estructura en `configuracion.py`:

```python
JERARQUIA_DE_CATEGORIAS = {
    "Literatura": ["Novela", "Cuento", "Poesía", "Ensayo"],
    "Ciencias": ["Física", "Biología", "Matemática"],
    "Tecnología": ["Programación", "Redes", "Base de datos"],
    "Arte": ["Pintura", "Música", "Patrimonio"],
    "Derecho": ["Civil", "Penal", "Constitucional"],
}
```

Cada libro podrá tener `categoria` y `subcategoria`. Si no se agrega `subcategoria` al JSON, la jerarquía se usa solo para búsquedas por nombre de categoría.

---

## 9. Persistencia y manejo de archivos

### 9.1 Archivos del sistema

| Archivo | Formato | Uso |
| --- | --- | --- |
| `datos/libros.json` | JSON | Catálogo |
| `datos/usuarios.json` | JSON | Usuarios y membresías |
| `datos/prestamos.json` | JSON | Préstamos y devoluciones |
| `datos/bitacora.txt` | Texto | Registro de operaciones |
| `datos/reportes/*.txt` | Texto | Reportes exportados |

### 9.2 Funciones de archivos

En `core/archivos.py`:

```python
def guardar_json(nombre_archivo, datos):
    ...

def leer_json(nombre_archivo):
    ...

def registrar_en_bitacora(mensaje):
    ...

def exportar_reporte(nombre, contenido):
    ...
```

Reglas:

- Usar `with open(...)` para cerrar siempre.
- Usar `encoding="utf-8"`.
- Escribir primero en un archivo temporal y luego reemplazar, para no perder datos si falla la escritura.
- Atrapar `OSError` y `json.JSONDecodeError` y relanzar como `ErrorDeArchivo`.
- La bitácora se abre en modo `a` para agregar sin borrar lo anterior.

### 9.3 Qué se guarda y cuándo

- Al prestar: `prestamos.json`, `libros.json` y `bitacora.txt`.
- Al devolver: `prestamos.json`, `libros.json` y `bitacora.txt`.
- Al registrar o actualizar un libro: `libros.json` y `bitacora.txt`.
- Al cambiar una membresía: `usuarios.json` y `bitacora.txt`.
- Al exportar un reporte: archivo `.txt` en `datos/reportes/`.

### 9.4 Archivos del sistema académico

Para el segundo entregable se usarán:

- `datos/estudiantes.json`;
- `datos/cursos.json`;
- `datos/calificaciones.txt` o `.csv`;
- `datos/asistencia.csv`;
- `datos/respaldo_academico.dat` en modo binario;
- `datos/reportes_academicos/`.

Se debe demostrar el uso de los modos `r`, `w`, `a` y `b`, además de generadores y cierres.

---

## 10. Interfaces gráficas

### 10.1 Estado actual de `ui/`

| Archivo `.ui` | Archivo `.py` | Clase | Estado |
| --- | --- | --- | --- |
| `acceso.ui` | `acceso.py` | `VentanaAcceso` | Funcional |
| `principal.ui` | `principal.py` | `VentanaPrincipal` | Funcional |
| `catalogo.ui` | `catalogo.py` | `VentanaCatalogo` | Funcional |
| `libro_form.ui` | `libro_form.py` | `VentanaLibro` | Pendiente |
| `usuario_form.ui` | `usuario_form.py` | `VentanaUsuario` | Pendiente |
| `prestamo.ui` | `prestamo.py` | `VentanaPrestamo` | Pendiente |
| `devolucion.ui` | `devolucion.py` | `VentanaDevolucion` | Pendiente |
| `reportes.ui` | `reportes.py` | `VentanaReportes` | Pendiente |

Cada `.ui` se carga con:

```python
from pathlib import Path
from PyQt5 import uic

uic.loadUi(str(Path(__file__).with_suffix(".ui")), self)
```

No se usa `pyuic5` para generar código intermedio: se carga el `.ui` directamente. Así el diseño se puede cambiar en QtDesigner sin tocar la lógica.

### 10.2 Flujo de navegación actual

```text
acceso.ui
   │ DNI válido y membresía vigente
   ▼
principal.ui
   ├── Inicio: resumen general
   ├── Catálogo: búsqueda, tabla y ficha
   ├── Mi membresía: datos y beneficios
   ├── Usuarios: solo administrador
   └── Reportes: solo administrador
```

Si el DNI no existe, está de baja o tiene la membresía vencida, la pantalla de acceso muestra el mensaje y no deja entrar.

### 10.3 Contrato de nombres de widgets

Estos nombres no se cambian sin actualizar el `.py` correspondiente.

#### `acceso.ui`

| `objectName` | Widget | Uso |
| --- | --- | --- |
| `tituloLabel` | `QLabel` | Nombre de la biblioteca |
| `subtituloLabel` | `QLabel` | Texto de ayuda |
| `dniLineEdit` | `QLineEdit` | DNI de 8 dígitos |
| `entrarButton` | `QPushButton` | Validar ingreso |
| `salirButton` | `QPushButton` | Cerrar la aplicación |
| `ayudaLabel` | `QLabel` | Mensaje de error o ayuda |

#### `principal.ui`

| `objectName` | Widget | Uso |
| --- | --- | --- |
| `bienvenidaLabel` | `QLabel` | Nombre del usuario |
| `tipoLabel` | `QLabel` | Tipo y estado |
| `navegacionListWidget` | `QListWidget` | Menú lateral |
| `cerrarSesionButton` | `QPushButton` | Volver al acceso |
| `paginasStackedWidget` | `QStackedWidget` | Cambio de páginas |
| `titulosValorLabel` | `QLabel` | Total de títulos |
| `ejemplaresValorLabel` | `QLabel` | Total de ejemplares |
| `disponiblesValorLabel` | `QLabel` | Ejemplares disponibles |
| `prestadosValorLabel` | `QLabel` | Ejemplares prestados |
| `usuariosValorLabel` | `QLabel` | Usuarios registrados |
| `catalogoContenedor` | `QWidget` | Contenedor de `VentanaCatalogo` |
| `nombreValorLabel` | `QLabel` | Nombre en membresía |
| `dniValorLabel` | `QLabel` | DNI en membresía |
| `tipoValorLabel` | `QLabel` | Tipo en membresía |
| `vencimientoValorLabel` | `QLabel` | Vencimiento |
| `estadoValorLabel` | `QLabel` | Estado de la cuenta |
| `permisosValorLabel` | `QLabel` | Permisos |
| `beneficiosLabel` | `QLabel` | Beneficios |
| `buscarUsuarioLineEdit` | `QLineEdit` | Buscar usuarios |
| `tablaUsuarios` | `QTableWidget` | Lista de usuarios |
| `cantidadUsuariosLabel` | `QLabel` | Cantidad encontrada |
| `reporteTextEdit` | `QTextEdit` | Reporte formateado |
| `exportarReporteButton` | `QPushButton` | Guardar reporte `.txt` |

#### `catalogo.ui`

| `objectName` | Widget | Uso |
| --- | --- | --- |
| `campoComboBox` | `QComboBox` | Todo, ISBN, título, autor o categoría |
| `buscarLineEdit` | `QLineEdit` | Texto de búsqueda |
| `categoriaComboBox` | `QComboBox` | Filtro por categoría |
| `ordenarComboBox` | `QComboBox` | Orden de resultados |
| `soloDisponiblesCheckBox` | `QCheckBox` | Solo disponibles para prestar |
| `limiteSpinBox` | `QSpinBox` | Máximo de resultados |
| `buscarButton` | `QPushButton` | Ejecutar búsqueda |
| `limpiarButton` | `QPushButton` | Restablecer filtros |
| `cantidadLibrosLabel` | `QLabel` | Cantidad encontrada |
| `tablaLibros` | `QTableWidget` | Resultados |
| `detalleTextEdit` | `QTextEdit` | Ficha formateada del libro |

### 10.4 Búsqueda en el catálogo

La pantalla permite buscar de forma directa por:

- **Todo:** ISBN, título, autor, categoría y sección.
- **ISBN:** coincidencia total o parcial.
- **Título:** coincidencia total o parcial.
- **Autor:** coincidencia total o parcial.
- **Categoría:** coincidencia total o parcial.

Además:

- el combo de categoría filtra por una categoría exacta;
- el check “Solo disponibles para prestar” aplica la regla del ejemplar que se queda;
- el combo de orden permite ordenar por título, autor, categoría o más disponibles;
- el `QSpinBox` limita la cantidad de filas;
- la tabla muestra ISBN, título, autor, categoría, disponibles y estado;
- la ficha lateral muestra además la sección, el estante, los ejemplares, los prestados y la ubicación completa;
- el tooltip de cada celda muestra el texto completo cuando la columna es angosta.

### 10.5 Reglas de la interfaz

- Por ahora no se usan hojas de estilo: se mantiene el aspecto básico de Qt. Los estilos se agregan al final.
- El nombre y el lema de la biblioteca se leen de `core/configuracion.py`; no se escriben de nuevo en las ventanas.
- Las imágenes e iconos van en `recursos/` y se cargan con `configuracion.ruta_de_imagen()` y `configuracion.ruta_de_icono()`.
- No se usan posiciones absolutas: todo va con layouts.
- Cada ventana tiene su clase y su archivo `.py` con el mismo nombre del `.ui`.
- La lógica de negocio no se escribe dentro del `.py` de la ventana.
- Los errores se muestran con `QMessageBox` o con un `QLabel` de estado, nunca con un traceback.
- Las acciones de administración se ocultan a los estudiantes, no solo se deshabilitan.
- Antes de cerrar una operación, se pide confirmación si la acción es destructiva.
- La ventana debe verse bien en 1366×768 y en 1920×1080.

### 10.6 Pantallas pendientes

| Pantalla | Componentes | Acciones |
| --- | --- | --- |
| `libro_form.ui` | `QLineEdit`, `QComboBox`, `QSpinBox`, `QPushButton` | Registrar y editar libro |
| `usuario_form.ui` | `QLineEdit`, `QComboBox`, `QCalendarWidget` | Registrar y editar usuario |
| `prestamo.ui` | `QLineEdit`, `QComboBox`, `QCalendarWidget`, `QLabel` | Elegir libro y usuario, confirmar préstamo |
| `devolucion.ui` | `QLineEdit`, `QTableWidget`, `QLabel` | Buscar préstamo, calcular multa y devolver |
| `reportes.ui` | `QTableWidget`, `QComboBox`, `QTextEdit`, `QPushButton` | Ver las cuatro matrices y exportar |

Con estas pantallas se cubren todos los componentes básicos y avanzados del sílabo: `QLabel`, `QLineEdit`, `QTextEdit`, `QPushButton`, `QRadioButton`, `QCheckBox`, `QSpinBox`, `QListWidget`, `QComboBox`, `QTableWidget` y `QCalendarWidget`.

---

## 11. Backlog priorizado

### Fase 0 — Estabilización

| ID | Tarea | Responsable | Criterio de aceptación |
| --- | --- | --- | --- |
| EST-01 | Revisar que `python3 main.py` y `python3 main_gui.py` arranquen desde la carpeta del proyecto | Dev 4 | Ambos comandos abren sin traceback |
| EST-02 | Ampliar pruebas y mover apuntes de `tests/` | Dev 1 | `python3 -m unittest` ejecuta pruebas del catálogo y usuarios |
| EST-03 | Revisar mensajes de error y tildes | Dev 2 | Los errores se muestran claros, sin traceback |
| EST-04 | Actualizar README con comandos y estructura | Dev 4 | README coincide con la realidad |
| EST-05 | Verificar que el JSON mal escrito se informe como `ErrorDeArchivo` | Dev 1 | El programa no termina con traceback de `json` |

### Fase 1 — Libros y usuarios

| ID | Tarea | Responsable | Depende de | Criterio de aceptación |
| --- | --- | --- | --- | --- |
| LIB-01 | Implementar `registrar_libro` | Dev 1 | EST-05 | ISBN repetido se rechaza; libro válido se guarda |
| LIB-02 | Implementar `actualizar_libro` | Dev 1 | LIB-01 | Se cambian solo campos válidos; se conserva el ISBN |
| LIB-03 | Implementar `eliminar_libro` | Dev 1 | LIB-01 | No se elimina con préstamos activos |
| LIB-04 | Crear `libro_form.ui` y `libro_form.py` | Dev 4 + Dev 1 | LIB-01 | Se registra y edita desde la interfaz |
| USR-01 | Implementar `registrar_usuario` | Dev 2 | EST-03 | DNI repetido se rechaza; tipo y fecha se validan |
| USR-02 | Implementar baja, reactivación y renovación | Dev 2 | USR-01 | El estado cambia y se refleja en la tabla |
| USR-03 | Crear `usuario_form.ui` y `usuario_form.py` | Dev 4 + Dev 2 | USR-01 | Se crea y edita desde la interfaz |
| USR-04 | Impedir préstamo a usuario de baja o vencido | Dev 2 + Dev 3 | USR-02 | La operación se rechaza con mensaje claro |
| PER-01 | Implementar `guardar_json` y `guardar_catalogo` | Dev 1 | LIB-01 | Al reiniciar se conservan los cambios |
| PER-02 | Implementar `guardar_usuarios` | Dev 2 | USR-01 | Al reiniciar se conservan los cambios |

### Fase 2 — Circulación

| ID | Tarea | Responsable | Depende de | Criterio de aceptación |
| --- | --- | --- | --- | --- |
| PRE-01 | Crear la clase `Prestamo` | Dev 3 | — | Calcula estado, retraso y multa |
| PRE-02 | Crear `prestamos.json` y cargarlo | Dev 3 | PRE-01 | Los préstamos se conservan al reiniciar |
| PRE-03 | Implementar `prestar_ejemplar` | Dev 3 | PRE-01, LIB-01, USR-01 | Descuenta disponibilidad y crea préstamo |
| PRE-04 | Implementar `devolver_ejemplar` | Dev 3 | PRE-03 | Suma disponibilidad y cierra el préstamo |
| PRE-05 | Implementar `calcular_multa` y tope | Dev 3 | PRE-01 | Multa correcta por día y tope respetado |
| PRE-06 | Crear `prestamo.ui` y `prestamo.py` | Dev 4 + Dev 3 | PRE-03 | Se presta desde la interfaz |
| PRE-07 | Crear `devolucion.ui` y `devolucion.py` | Dev 4 + Dev 3 | PRE-04 | Se devuelve y se muestra la multa |
| PRE-08 | Registrar operaciones en bitácora | Dev 3 | PER-01 | Cada préstamo y devolución deja línea en `bitacora.txt` |

### Fase 3 — Reportes, matrices y recursividad

| ID | Tarea | Responsable | Depende de | Criterio de aceptación |
| --- | --- | --- | --- | --- |
| REP-01 | `mapa_de_estantes` | Dev 3 | PRE-02 | Matriz 5×3 calculada desde el catálogo |
| REP-02 | `agenda_de_devoluciones` | Dev 3 | PRE-02 | Préstamos por vencer y vencidos por día |
| REP-03 | `historial_por_usuario` | Dev 3 | PRE-02 | Histórico, activos y devueltos por usuario |
| REP-04 | `penalizaciones_por_usuario` | Dev 3 | PRE-05 | Multa acumulada y días de retraso |
| REP-05 | `buscar_en_categoria` recursivo | Dev 1 | — | Recorre jerarquía y encuentra coincidencias |
| REP-06 | `contar_disponibles_en_seccion` recursivo | Dev 3 | REP-01 | Recorre la matriz sin bucles anidados |
| REP-07 | `sumar_existencias` recursivo | Dev 3 | REP-01 | Suma una sección completa |
| REP-08 | Crear `reportes.ui` y `reportes.py` | Dev 4 | REP-01 a REP-04 | Se ven las cuatro matrices y se exportan |
| REP-09 | Exportar reporte a `.txt` | Dev 4 | PER-01 | El archivo se crea en `datos/reportes/` |

### Fase 4 — Calidad y cierre

| ID | Tarea | Responsable | Criterio de aceptación |
| --- | --- | --- | --- |
| QA-01 | Pruebas de catálogo y búsqueda | Dev 1 | ISBN, título, autor, categoría, tildes y vacío |
| QA-02 | Pruebas de usuarios y membresías | Dev 2 | Alta, baja, renovación y vencimiento |
| QA-03 | Pruebas de préstamos y devoluciones | Dev 3 | Disponibilidad, límite, multa y tope |
| QA-04 | Pruebas de archivos | Dev 1 + Dev 2 | JSON válido, JSON roto, archivo inexistente |
| QA-05 | Prueba manual de todas las pantallas | Dev 4 | Flujo completo sin traceback |
| QA-06 | Revisión de nombres y documentación | Todos | Sin nombres genéricos ni comentarios obsoletos |
| QA-07 | Presentación del proyecto | Todos | Funcionamiento, diseño y beneficios |

---

## 12. Cronograma de trabajo

El cronograma se adapta a las semanas reales del curso. Esta es la secuencia recomendada.

### Semana 1 — Orden y base

- Revisar el plan con todo el equipo.
- Verificar que la consola y la interfaz arranquen.
- Resolver la deuda técnica de la Fase 0.
- Definir el contrato de nombres de widgets.
- Crear las ramas de trabajo.

**Entregable:** sistema actual estable, plan aprobado y tareas repartidas.

### Semana 2 — Libros y usuarios

- Implementar CRUD de libros.
- Implementar alta, baja, reactivación y renovación de usuarios.
- Crear formularios de libro y usuario.
- Guardar cambios en JSON.
- Pruebas de catálogo y membresías.

**Entregable:** se pueden registrar y editar libros y usuarios desde la interfaz.

### Semana 3 — Préstamos y devoluciones

- Crear `Prestamo`.
- Implementar préstamo, devolución y multa.
- Actualizar disponibilidad.
- Crear pantallas de préstamo y devolución.
- Registrar bitácora.
- Pruebas de circulación.

**Entregable:** ciclo completo de préstamo y devolución funcionando.

### Semana 4 — Reportes y cierre del primer entregable

- Implementar las cuatro matrices.
- Implementar recursividad sobre matrices.
- Crear pantalla de reportes.
- Exportar reportes a texto.
- Pruebas finales, documentación y presentación.
- Ensayo de la demostración.

**Entregable:** primer entregable completo y defendible.

### Semanas 5 a 8 — Sistema académico

- Diseñar las clases del sistema académico.
- Crear las pantallas con todos los componentes.
- Implementar archivos de texto y binarios.
- Implementar expresiones regulares.
- Generar reportes.
- Pruebas, documentación y presentación final.

**Entregable:** sistema académico completo y presentación.

---

## 13. Pruebas

### 13.1 Pruebas manuales mínimas

| Caso | Entrada | Resultado esperado |
| --- | --- | --- |
| Acceso correcto | DNI `11111111` | Abre el panel como estudiante |
| Acceso administrador | DNI `33333333` | Muestra Usuarios y Reportes |
| Usuario de baja | DNI `70778899` | Muestra mensaje y no entra |
| Membresía vencida | DNI `76789012` | Muestra fecha de vencimiento y no entra |
| DNI inexistente | DNI `99999999` | Muestra “No hay ningún usuario” |
| Búsqueda por ISBN | `9788437604947` | Devuelve “Cien años de soledad” |
| Búsqueda por título | `cien` | Devuelve el libro |
| Búsqueda por autor | `tolkien` | Devuelve “El Señor de los Anillos” |
| Búsqueda por categoría | `arte` | Devuelve 4 libros |
| Filtro disponibles | Check activo | Solo libros con más de un ejemplar |
| Libro sin disponibilidad | Filtro y selección | Muestra “Solo consulta” o “Sin ejemplares” |
| Exportar reporte | Botón Exportar | Crea un `.txt` legible |
| JSON mal escrito | Editar `libros.json` | Mensaje de `ErrorDeArchivo` sin traceback |

### 13.2 Pruebas automatizadas

Se usará `unittest` de la biblioteca estándar. Ejemplo:

```python
import unittest
from core.biblioteca import Biblioteca


class PruebasCatalogo(unittest.TestCase):
    def setUp(self):
        self.biblioteca = Biblioteca()

    def test_buscar_por_isbn(self):
        datos = self.biblioteca.buscar_avanzado("9788437604947", campo="ISBN")
        self.assertEqual(len(datos), 1)
        self.assertIn("Cien", datos[0]["titulo"])

    def test_buscar_sin_resultados(self):
        datos = self.biblioteca.buscar_avanzado("xyz", campo="titulo")
        self.assertEqual(datos, [])

    def test_filtro_disponibles(self):
        datos = self.biblioteca.buscar_avanzado(solo_disponibles=True)
        for libro in datos:
            self.assertGreater(libro["disponibles"], 1)


if __name__ == "__main__":
    unittest.main()
```

Comando:

```bash
python3 -m unittest discover -s tests -v
```

### 13.3 Pruebas de interfaz

No se automatizan al inicio. Se prueban manualmente:

- con un estudiante;
- con un administrador;
- con un usuario de baja;
- con un usuario vencido;
- con búsqueda vacía;
- con búsqueda sin resultados;
- con la ventana maximizada y en 1366×768;
- cerrando sesión y volviendo a entrar.

### 13.4 Pruebas de archivos

- Leer un JSON válido.
- Leer un JSON vacío.
- Leer un JSON inexistente.
- Leer un JSON con una coma faltante.
- Guardar y volver a leer.
- Escribir una bitácora y comprobar que no borra lo anterior.

---

## 14. Sistema académico del segundo entregable

### 14.1 Alcance

El sistema debe permitir a un docente:

- registrar estudiantes;
- crear cursos;
- registrar calificaciones por curso y por evaluación;
- registrar asistencia por fecha;
- justificar ausencias;
- generar reportes por estudiante, curso o periodo;
- guardar y recuperar la información desde archivos;
- buscar y reemplazar texto con expresiones regulares.

### 14.2 Clases propuestas

| Clase | Responsabilidad |
| --- | --- |
| `Estudiante` | Datos personales, código, cursos y estado |
| `Curso` | Nombre, código, periodo y lista de estudiantes |
| `Calificacion` | Nota, evaluación, fecha y estudiante |
| `Asistencia` | Fecha, estado, justificación y estudiante |
| `GestorAcademico` | Coordina estudiantes, cursos, notas y asistencias |
| `ArchivoAcademico` | Lee y escribe archivos de texto y binarios |
| `ReporteAcademico` | Promedios, asistencia y observaciones |

Se aplican los mismos principios:

- encapsulación con atributos privados;
- herencia de `Persona` a `Estudiante` y `Docente` si se necesita;
- polimorfismo en el cálculo de promedios o en el estado de asistencia;
- excepciones propias para datos inválidos;
- funciones con parámetros claros y valores de retorno.

### 14.3 Pantallas

| Pantalla | Componentes principales |
| --- | --- |
| `acceso.ui` | `QLabel`, `QLineEdit`, `QPushButton` |
| `principal.ui` | `QListWidget`, `QStackedWidget`, `QLabel` |
| `cursos.ui` | `QComboBox`, `QLineEdit`, `QTableWidget` |
| `estudiantes.ui` | `QLineEdit`, `QListWidget`, `QPushButton` |
| `calificaciones.ui` | `QComboBox`, `QSpinBox`, `QTableWidget`, `QTextEdit` |
| `asistencia.ui` | `QCalendarWidget`, `QRadioButton`, `QCheckBox`, `QTableWidget` |
| `reportes.ui` | `QComboBox`, `QTableWidget`, `QTextEdit`, `QPushButton` |

### 14.4 Archivos y expresiones regulares

- `estudiantes.json` y `cursos.json` para datos estructurados.
- `calificaciones.txt` con formato `codigo;curso;evaluacion;nota;fecha`.
- `asistencia.csv` con formato `codigo;fecha;estado;justificacion`.
- `respaldo_academico.dat` en modo binario con `pickle`.
- Búsqueda y reemplazo de nombres o códigos con `re`.
- Validación de correo, código de estudiante y nombres con expresiones regulares.
- Generadores para recorrer archivos grandes sin cargar todo en memoria.
- `with open(...)` en todas las operaciones.

### 14.5 Backlog resumido del sistema académico

| ID | Tarea | Criterio de aceptación |
| --- | --- | --- |
| ACA-01 | Clases `Estudiante`, `Curso`, `Calificacion`, `Asistencia` | Se crean con datos válidos y rechazan inválidos |
| ACA-02 | `GestorAcademico` | Registra, busca y actualiza estudiantes y cursos |
| ACA-03 | Pantalla de cursos | Se crea un curso y se lista |
| ACA-04 | Pantalla de estudiantes | Se registra y se asigna a un curso |
| ACA-05 | Pantalla de calificaciones | Se ingresa una nota y se actualiza la tabla |
| ACA-06 | Pantalla de asistencia | Se marca presente, ausente o justificado |
| ACA-07 | Archivos de texto | Se guarda y se recupera la información |
| ACA-08 | Archivo binario | Se crea un respaldo y se recupera |
| ACA-09 | Expresiones regulares | Se valida correo y código; se busca y reemplaza texto |
| ACA-10 | Reportes | Promedios y asistencia por estudiante y curso |
| ACA-11 | Pruebas | Casos felices y errores controlados |
| ACA-12 | Presentación | Máximo 15 diapositivas con funcionamiento y diseño |

---

## 15. Documentación y presentación

### 15.1 Documentación del código

- Cada módulo tiene un docstring al inicio.
- Cada clase explica qué representa.
- Cada método público explica qué recibe y qué devuelve.
- Los comentarios explican el “por qué”, no repiten el código.
- No se dejan comentarios obsoletos ni código comentado sin uso.

### 15.2 README

Debe incluir:

- nombre del proyecto;
- integrantes;
- descripción;
- requisitos;
- instalación de PyQt5;
- comandos de ejecución;
- estructura de carpetas;
- archivos de datos;
- usuarios de prueba;
- funcionalidades implementadas;
- pendientes.

### 15.3 Presentación

Para el primer entregable:

1. Portada.
2. Problema y objetivo.
3. Arquitectura del sistema.
4. Demostración de acceso y roles.
5. Demostración de catálogo y búsqueda.
6. Demostración de préstamo y devolución.
7. Matrices y recursividad.
8. POO: clases, encapsulación, herencia y polimorfismo.
9. Archivos y excepciones.
10. Pruebas realizadas.
11. Dificultades y aprendizajes.
12. Conclusiones.

Para el segundo entregable se agrega la demostración de componentes avanzados, archivos binarios, expresiones regulares y reportes académicos.

---

## 16. Riesgos y cómo reducirlos

| Riesgo | Impacto | Mitigación |
| --- | --- | --- |
| Que la interfaz tenga lógica duplicada | Cambios en dos lugares y errores | Toda regla va en `core/`; la UI solo muestra |
| Que se pierdan datos al guardar | Pérdida del trabajo | Guardar en archivo temporal y reemplazar |
| Que las matrices se desactualicen | Reportes incorrectos | Calcularlas siempre desde el catálogo y los préstamos |
| Que un compañero no pueda ejecutar el proyecto | Pérdida de tiempo | README con comandos y datos de prueba |
| Que se acumule trabajo al final | Entrega incompleta | Backlog por fases y demo semanal |
| Que se rompa el acceso por membresía | Usuarios no pueden entrar | Pruebas con los DNI de prueba |
| Que el JSON se edite a mano y quede inválido | El programa no arranca | Validar y mostrar `ErrorDeArchivo` claro |
| Que se cambien los `objectName` | La interfaz deja de encontrar widgets | Contrato de nombres y revisión en cada merge |

---

## 17. Checklist antes de cada entrega

### Código

- [ ] `python3 main.py` arranca y permite navegar.
- [ ] `python3 main_gui.py` arranca y permite entrar.
- [ ] No hay tracebacks con los datos de prueba.
- [ ] Los JSON se leen y se guardan correctamente.
- [ ] Las operaciones de préstamo y devolución actualizan disponibilidad.
- [ ] Las multas se calculan con tope.
- [ ] Las matrices se calculan desde los datos reales.
- [ ] Las funciones recursivas tienen caso base y paso recursivo.
- [ ] No hay rutas absolutas personales.
- [ ] No hay `print()` de depuración en `core/` ni en `ui/`.

### Interfaz

- [ ] Todos los botones hacen algo.
- [ ] Los errores se muestran con mensajes claros.
- [ ] El estudiante no ve opciones de administración.
- [ ] El administrador sí las ve.
- [ ] La búsqueda por ISBN, título, autor y categoría funciona.
- [ ] La tabla y la ficha se actualizan al cambiar de selección.
- [ ] La ventana se ve bien en 1366×768.
- [ ] Cerrar sesión vuelve al acceso.

### Documentación

- [ ] README actualizado.
- [ ] Plan actualizado.
- [ ] Integrantes y roles escritos.
- [ ] Usuarios de prueba documentados.
- [ ] Presentación preparada.
- [ ] El código está comentado en las partes importantes.

### Equipo

- [ ] Cada rama fue revisada por otra persona.
- [ ] Las tareas del backlog están marcadas.
- [ ] Se hizo una prueba completa antes de comprimir el `.zip`.
- [ ] El `.zip` incluye código, datos, documentación y presentación.

---

## 18. Anexos

### Anexo A. Comandos útiles

```bash
# instalar PyQt5
python3 -m pip install PyQt5

# ejecutar consola
cd proyecto_parcial
python3 main.py

# ejecutar interfaz
python3 main_gui.py

# ejecutar pruebas
python3 -m unittest discover -s tests -v

# revisar sintaxis de todos los módulos
python3 -m compileall core ui main.py main_gui.py

# ver el estado del repositorio
git status
git diff
```

### Anexo B. Usuarios de prueba

| DNI | Nombre | Tipo | Estado |
| --- | --- | --- | --- |
| `11111111` | P_ESTUDIANTE | Estudiante | Activo |
| `22222222` | P_DOCENTE | Docente | Activo |
| `33333333` | P_ADMINISTRADOR | Administrador | Activo |
| `78901234` | Valeria Sanchez | Administrador | Membresía vencida |
| `70778899` | Rosa Palomino | Estudiante | De baja |
| `76789012` | Diego Vargas | Docente | Membresía vencida |
| `99999999` | — | — | No existe |

### Anexo C. Glosario

| Término | Significado |
| --- | --- |
| POO | Programación Orientada a Objetos |
| Encapsulación | Proteger los datos dentro de una clase y exponer métodos |
| Herencia | Crear una clase a partir de otra |
| Polimorfismo | Un mismo método responde distinto según la clase |
| Matriz | Estructura de filas y columnas |
| Recursividad | Función que se llama a sí misma con un caso base |
| JSON | Formato de texto para guardar datos estructurados |
| Bitácora | Archivo de texto con el historial de operaciones |
| Préstamo activo | Préstamo que todavía no fue devuelto |
| Multa | Monto por devolver después de la fecha límite |

---

**Última actualización:** 8 de noviembre de 2026.  
**Mantenimiento:** el equipo actualiza este plan al cerrar cada semana de trabajo.
