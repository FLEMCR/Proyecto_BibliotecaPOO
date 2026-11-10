# Plan del proyecto — Sistema de Biblioteca

> **Proyecto:** Biblioteca General POSTDATA  
> **Curso:** Programación Orientada a Objetos  
> **Documento:** `docs/plan_proyecto.md`  
> **Última actualización:** 2026-11-10  
> **Entradas del sistema:** `main_interfaz.py` (interfaz gráfica) y `main.py` (consola)  
> **Datos:** `datos/libros.json`, `datos/usuarios.json` y `datos/prestamos.json`

Este documento reemplaza al plan anterior. Su objetivo es servir como guía de trabajo para terminar el sistema, conectar las interfaces con la lógica existente y agregar lo que falta sin duplicar código.

---

## Contenido

1. [Cómo usar este plan](#1-cómo-usar-este-plan)
2. [Objetivo y alcance](#2-objetivo-y-alcance)
3. [Estado actual](#3-estado-actual)
4. [Arquitectura y reglas del proyecto](#4-arquitectura-y-reglas-del-proyecto)
5. [Estructura actual y estructura final](#5-estructura-actual-y-estructura-final)
6. [Contrato de interfaces y componentes](#6-contrato-de-interfaces-y-componentes)
7. [Lógica del core](#7-lógica-del-core)
8. [Matrices y recursividad](#8-matrices-y-recursividad)
9. [Guía de implementación por funcionalidad](#9-guía-de-implementación-por-funcionalidad)
10. [Plan de trabajo por fases](#10-plan-de-trabajo-por-fases)
11. [Pruebas manuales](#11-pruebas-manuales)
12. [Convenciones y definición de terminado](#12-convenciones-y-definición-de-terminado)
13. [Decisiones del equipo y pendientes](#13-decisiones-del-equipo-y-pendientes)
14. [Orden recomendado para empezar](#14-orden-recomendado-para-empezar)

---

## 1. Cómo usar este plan

- Cada tarea se marca con `[ ]` al empezar y `[x]` al terminar.
- El orden de las fases no es obligatorio, pero sí recomendable: primero se estabiliza la base, luego se conecta la interfaz y al final se agregan préstamos, reportes y estilos.
- La lógica de negocio va en `core/`. La interfaz solo muestra datos y llama métodos de `core/`.
- Los archivos `.ui` contienen únicamente el diseño. Las conexiones `clicked`, `currentRowChanged`, etc. se hacen en Python.
- Los textos visibles, rutas y reglas configurables se toman de `core/configuracion.py`; no se duplican en las ventanas.
- La carpeta `tests/` es de uso local y está ignorada por Git. No forma parte de la estructura entregable ni de las decisiones del sistema.
- Este documento no califica el avance: solo describe el estado, lo que falta y cómo hacerlo.

### Estados usados

| Estado | Significado |
| --- | --- |
| ✅ | Ya funciona y está conectado. |
| 🟡 | Existe una base, pero falta conectarlo o completarlo. |
| ⬜ | Todavía no existe. |

---

## 2. Objetivo y alcance

### 2.1 Objetivo

Completar un sistema de biblioteca con dos formas de uso:

1. **Interfaz gráfica** con PyQt5 y archivos `.ui` de QtDesigner.
2. **Consola** como respaldo para probar la lógica sin interfaz.

Ambas entradas deben compartir exactamente el mismo núcleo (`core/`). No debe existir una versión de la lógica para consola y otra para la interfaz.

### 2.2 Alcance funcional

| Módulo | Qué debe permitir |
| --- | --- |
| Acceso | Ingresar con DNI, validar que el usuario exista, esté activo y tenga membresía vigente. |
| Registro | Crear una cuenta nueva desde el acceso con DNI, nombre y tipo, con membresía de 3 meses. |
| Inicio | Ver el resumen general de la biblioteca en tiempo real. |
| Catálogo | Listar, buscar, filtrar, ordenar y ver la ficha de cada libro. |
| Membresía | Ver los datos y el estado de la membresía del usuario conectado. |
| Usuarios | Listar y buscar usuarios; solo el administrador puede gestionarlos. |
| Libros | Registrar, editar y eliminar libros; los cambios deben guardarse en el JSON. |
| Préstamos | Prestar un solo ejemplar por usuario y bloquear otro préstamo hasta que se devuelva. |
| Devoluciones | Devolver el ejemplar, actualizar stock y liberar al usuario para un nuevo préstamo. |
| Reportes | Mostrar matrices de disponibilidad, devoluciones, historial y préstamos por sección. |
| Persistencia | Leer y escribir JSON; registrar movimientos en una bitácora de texto. |
| Administración | Dar de baja, reactivar y renovar membresías. |

### 2.3 Decisiones del equipo

Estas reglas ya están decididas y deben respetarse en el código y en la interfaz:

1. **No se cobran multas.** El sistema no calcula dinero ni bloquea por deuda. Si un préstamo pasa de la fecha límite, solo se muestra como vencido en los reportes; no genera multa.
2. **Un solo préstamo activo por usuario.** Mientras el usuario no devuelva el libro que tiene, no puede pedir otro. El límite es 1, no 3.
3. **No se implementan beneficios de membresía por ahora.** La página “Mi membresía” solo muestra nombre, DNI, tipo, vencimiento y estado. Los beneficios quedan descartados para esta etapa.
4. **La devolución libera al usuario.** Cuando se registra la devolución, el stock sube y el usuario queda habilitado para pedir otro libro.
5. **El registro desde el acceso crea la membresía por 3 meses.** La fecha de vencimiento se calcula con `sumar_meses(fecha_de_alta, 3)`; no se usa `timedelta(days=90)` porque los meses no tienen la misma cantidad de días. El autorregistro solo permite `Estudiante` o `Docente`, nunca `Administrador`.

Estas decisiones simplifican la lógica, evitan cálculos que no se piden y mantienen el foco en el flujo de registro, préstamo y devolución.

### 2.4 Requisitos que el proyecto debe demostrar

| Requisito | Dónde se cumple |
| --- | --- |
| Clases y objetos | `Libro`, `Usuario`, `Administrador`, `Prestamo`, `Biblioteca` y las ventanas. |
| Encapsulación | Atributos con `_` y métodos de lectura (`titulo()`, `dni()`, `estado()`, etc.). |
| Herencia | `Administrador(Usuario)`. |
| Polimorfismo | `puede_administrar()` y `datos_de_membresia()` cambian según el tipo de usuario. |
| Constructores y valores por defecto | `Usuario(...)`, `Libro(...)` y las ventanas que reciben `biblioteca` y `usuario`. |
| Funciones y métodos | Validaciones, búsquedas, reportes, préstamos y devoluciones. |
| Parámetros y retornos | Todas las operaciones del núcleo devuelven datos listos para la interfaz. |
| Excepciones propias | `ErrorBiblioteca`, `ErrorDeDatos` y las nuevas excepciones de archivo, préstamo y membresía. |
| Recursividad | Búsqueda por texto y funciones de reportes sobre listas y matrices. |
| Matrices | Reportes de estantes, devoluciones, historial y préstamos por sección. |
| Archivos JSON | Lectura y escritura de libros, usuarios y préstamos. |
| Archivo de texto | Bitácora de movimientos y exportación de reportes. |
| PyQt5 / QtDesigner | Ventanas, formularios, tablas, combos, listas, spin boxes y calendario si se usa. |
| Expresiones regulares | Validación de DNI, ISBN y fechas si se implementa como mejora. |

---

## 3. Estado actual

### 3.1 Lo que ya funciona ✅

- **Núcleo de la biblioteca:** carga de libros y usuarios desde JSON.
- **Clases del dominio:** `Libro`, `Usuario`, `Administrador` y `Biblioteca`.
- **Validaciones:** DNI de 8 dígitos, ISBN de 13 dígitos, fechas reales, sección y estante válidos.
- **Búsqueda recursiva:** `buscar_por_texto()` y `datos_del_catalogo()`.
- **Resumen general:** títulos, ejemplares, disponibles, prestados y usuarios.
- **Consola:** `main.py` arranca y permite acceder, ver catálogo, buscar, consultar por ISBN, ver membresía y listar usuarios.
- **Acceso gráfico:** `ui/acceso.py` valida DNI, cuenta activa y membresía vigente, y emite `usuario_autenticado`.
- **Coordinación acceso → panel:** `main_interfaz.py` crea `VentanaAcceso`, escucha la señal y abre `VentanaPrincipal`.
- **Cierre de sesión mínimo:** `VentanaPrincipal` emite `sesion_cerrada` y el controlador vuelve al acceso.

### 3.2 Lo que está a medias 🟡

| Elemento | Estado actual | Qué falta |
| --- | --- | --- |
| `ui/principal.py` | Solo muestra el nombre y conecta “Cerrar sesión”. | Navegación, resumen, membresía, usuarios, reportes, visibilidad por rol y cierre controlado. |
| `ui/principal.ui` | Tiene las cinco páginas y los widgets principales. | `catalogoPage` está vacío; `layoutAccesosRapidos` no tiene botones; algunos textos están fijos. |
| `ui/catalogo.ui` | Diseño completo con filtros, tabla y ficha. | No tiene `ui/catalogo.py` ni está incrustado en el panel. |
| `main_interfaz.py` | Abre y cierra ventanas. | Manejo del cierre de la ventana principal y limpieza del acceso. |
| `ui/acceso.py` | Valida y muestra errores con `QMessageBox`. | Enter para ingresar, validator de DNI, mensaje inline en `ayudaLabel`, foco inicial y botón de registro. |
| Consola | Funciona con el catálogo actual. | No conoce préstamos, devoluciones, CRUD ni membresías. |

### 3.3 Lo que falta ⬜

- Clase `Prestamo` y archivo `core/prestamos.py`.
- Operaciones de préstamo y devolución con actualización de stock.
- Bloqueo de un segundo préstamo mientras el usuario tenga uno activo.
- Registro del estado “vencido” sin cálculo de multa.
- Registro, edición y eliminación de libros desde la interfaz.
- Registro de usuarios nuevos desde la pantalla de acceso, con membresía de 3 meses.
- Registro, edición, baja, reactivación y renovación de usuarios.
- Cálculo de vencimientos con `sumar_meses()` y `MESES_DE_MEMBRESIA`.
- Persistencia de escritura: hoy solo se lee JSON.
- `datos/prestamos.json` con contenido y estructura definida.
- `core/reportes.py` con matrices y recursividad sobre matrices.
- `ui/catalogo.py` y su integración en `catalogoPage`.
- Formularios `libro_form.ui`, `prestamo.ui` y `devolucion.ui`.
- Botones de acción en las páginas de usuarios y reportes.
- Estilos, íconos e imágenes (se dejan para el final).
- Actualización del `README.md` con las instrucciones nuevas.

### 3.4 Problemas técnicos que conviene corregir primero

| Prioridad | Problema | Efecto | Corrección propuesta |
| --- | --- | --- | --- |
| Alta | `core/biblioteca.py` usa `from core import ...` y otros módulos usan imports relativos. | Funciona al ejecutar desde la carpeta del proyecto, pero falla si se ejecuta como paquete. | Unificar a imports relativos (`from . import ...`) y agregar `core/__init__.py` y `ui/__init__.py`. |
| Alta | `main.py` llama a `main()` sin `if __name__ == "__main__":`. | Se ejecuta al importar el archivo. | Envolver la llamada en la condición. |
| Alta | `crear_libro()` usa `datos.get(...)` sin valor por defecto en varios campos. | Un JSON incompleto produce `TypeError` en lugar de `ErrorDeDatos`. | Poner valores por defecto o validar antes de construir el `Libro`. |
| Alta | `leer_archivo()` no captura errores de JSON. | Un JSON mal escrito muestra un traceback. | Capturar `json.JSONDecodeError` y lanzar `ErrorDeArchivo`. |
| Alta | No existe función para escribir archivos. | Ningún cambio del usuario se guarda. | Agregar `escribir_archivo()` en `configuracion.py`. |
| Media | `VentanaPrincipal` no implementa `closeEvent`. | Al cerrar con la X, la ventana desaparece pero la aplicación puede quedar sin ventanas visibles. | Implementar `closeEvent` y decidir si cierra la app o vuelve al acceso. |
| Media | `cerrar_sesion()` solo emite la señal; no cierra la ventana. | El panel puede quedar visible hasta que el controlador lo elimine. | Cerrar la ventana después de emitir la señal o hacer que el controlador la oculte. |
| Media | `principal.ui` tiene el nombre y el lema escritos a mano. | Se duplican textos que ya están en `configuracion.py`. | Cargarlos desde `configuracion.NOMBRE_BIBLIOTECA` y `configuracion.LEMA`. |
| Media | `Libro.se_puede_prestar()` devuelve `True` solo si `disponibles > 1`. | El último ejemplar nunca se presta. | Decidir la regla y documentarla. Si se permite prestar el último, cambiar a `> 0`. |
| Media | `VentanaAcceso` no tiene validator ni Enter. | Se pueden escribir letras y hay que usar el botón. | Agregar `QIntValidator`, `maxLength` y `returnPressed`. |
| Baja | Variables con tildes o nombres poco claros (`año`). | Dificulta la lectura y puede causar errores de codificación. | Renombrar a `anio`, `mes`, `dia`. |
| Baja | `pausa()` y varias funciones de `menu.py` solo sirven a la consola. | Código que no usa la interfaz. | Mantenerlos mientras exista `main.py`; si se retira la consola, eliminarlos. |

---

## 4. Arquitectura y reglas del proyecto

### 4.1 Capas

```
┌─────────────────────────────────────────────┐
│ Entradas                                    │
│ main_interfaz.py        main.py             │
│ (PyQt5)                 (consola)           │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│ Interfaz (ui/)                              │
│ VentanaAcceso, VentanaPrincipal,            │
│ VentanaCatalogo, formularios                │
└──────────────────┬──────────────────────────┘
                   │ llamadas a métodos
┌──────────────────▼──────────────────────────┐
│ Núcleo (core/)                              │
│ Biblioteca, Libro, Usuario, Administrador,  │
│ Prestamo, reportes, validaciones            │
└──────────────────┬──────────────────────────┘
                   │ lectura / escritura
┌──────────────────▼──────────────────────────┐
│ Datos (datos/)                              │
│ libros.json, usuarios.json, prestamos.json, │
│ bitacora.txt                                │
└─────────────────────────────────────────────┘
```

### 4.2 Reglas

1. **La interfaz no abre archivos JSON.** Solo llama métodos de `Biblioteca`.
2. **El núcleo no importa PyQt5.** `core/` debe poder usarse desde la consola.
3. **Los `.ui` no contienen lógica.** Las conexiones se hacen en el `.py` de cada ventana.
4. **Un dato se escribe una sola vez.** El nombre de la biblioteca, el lema, las rutas y las reglas van en `configuracion.py`.
5. **Los nombres de los widgets son un contrato.** Si cambia un `objectName` en el `.ui`, hay que actualizar el `.py`.
6. **Cada ventana recibe sus dependencias.** `VentanaPrincipal(biblioteca, usuario)` y `VentanaCatalogo(biblioteca, parent)`; no se usan variables globales.
7. **Las operaciones importantes devuelven datos o lanzan excepciones.** La interfaz decide cómo mostrarlos.
8. **El stock nunca queda negativo.** Prestar descuenta, devolver suma y ambas operaciones validan antes de guardar.

### 4.3 Flujo de navegación

```
main_interfaz.py
      │
      ▼
VentanaAcceso ── usuario_autenticado ──► VentanaPrincipal
      ▲   │                                  │
      │   └── abre ──► VentanaRegistro        ├── Inicio
      │                                      ├── Catálogo (catalogo.ui incrustado)
      └──────── sesion_cerrada ◄─────────────┤── Mi membresía
                                             ├── Usuarios (solo admin)
                                             └── Reportes (solo admin)
```

`VentanaRegistro` se abre como diálogo desde el acceso; al aceptar, vuelve al acceso y deja el DNI listo para ingresar. Los formularios de libro, préstamo y devolución se abren como diálogos desde la página correspondiente y vuelven a ella al guardar o cancelar.

---

## 5. Estructura actual y estructura final

### 5.1 Estructura actual

```
proyecto_parcial/
├── main.py                     # entrada de consola
├── main_interfaz.py            # entrada de la interfaz gráfica
├── README.md
├── core/
│   ├── biblioteca.py           # controlador: catálogo, usuarios y resumen
│   ├── configuracion.py        # rutas, secciones, estantes y lectura de JSON
│   ├── errores.py              # ErrorBiblioteca y ErrorDeDatos
│   ├── libros.py               # Libro, fábrica y búsqueda recursiva
│   ├── menu.py                 # menú de consola
│   ├── usuarios.py             # Usuario, Administrador y fábrica
│   └── utilidades.py           # DNI, ISBN, fechas y textos
├── datos/
│   ├── libros.json             # 22 libros
│   ├── prestamos.json          # vacío por ahora
│   └── usuarios.json           # 13 usuarios
├── docs/
│   ├── Guia_base.ipynb
│   ├── Guia_base.md
│   ├── plan_proyecto.md        # este documento
│   └── (sílabo y rúbricas en PDF)
└── ui/
    ├── acceso.py               # VentanaAcceso
    ├── acceso.ui
    ├── catalogo.ui             # sin archivo .py todavía
    ├── principal.py            # VentanaPrincipal incompleta
    └── principal.ui
```

### 5.2 Estructura final propuesta

Las marcas indican qué se conserva, qué se modifica y qué se crea.

```
proyecto_parcial/
├── main_interfaz.py            [modificar] entrada principal de la GUI
├── main.py                     [opcional]  consola de respaldo
├── README.md                   [modificar]
├── core/
│   ├── __init__.py             [nuevo]     paquete importable
│   ├── biblioteca.py           [modificar] operaciones de negocio
│   ├── configuracion.py        [modificar] rutas, reglas y escritura
│   ├── errores.py              [modificar] nuevas excepciones
│   ├── libros.py               [modificar] CRUD y búsqueda avanzada
│   ├── menu.py                 [opcional]  se retira si no se usa la consola
│   ├── prestamos.py            [nuevo]     Prestamo y control de préstamo único
│   ├── reportes.py             [nuevo]     matrices y recursividad
│   ├── usuarios.py             [modificar] gestión de membresías
│   └── utilidades.py           [modificar] fechas y validaciones
├── datos/
│   ├── bitacora.txt            [nuevo, generado]
│   ├── libros.json             [modificar] se escribe desde el sistema
│   ├── prestamos.json          [modificar] préstamo activo e historial
│   └── usuarios.json           [modificar] altas, bajas y renovaciones
├── docs/
│   ├── Guia_base.ipynb
│   ├── Guia_base.md
│   ├── plan_proyecto.md
│   └── (sílabo y rúbricas en PDF)
├── recursos/                   [opcional]
│   ├── iconos/
│   └── imagenes/
└── ui/
    ├── __init__.py             [nuevo]     paquete importable
    ├── acceso.py               [modificar] validación y Enter
    ├── acceso.ui               [modificar] textos desde configuración
    ├── catalogo.py             [nuevo]     VentanaCatalogo
    ├── catalogo.ui             [conservar]
    ├── devolucion.py           [nuevo]     diálogo de devolución
    ├── devolucion.ui           [nuevo]
    ├── estilos.qss             [opcional]  estilos globales
    ├── libro_form.py           [nuevo]     diálogo de alta/edición
    ├── libro_form.ui           [nuevo]
    ├── prestamo.py             [nuevo]     diálogo de préstamo
    ├── prestamo.ui             [nuevo]
    ├── principal.py            [modificar] navegación y páginas
    ├── principal.ui            [modificar] contenedor del catálogo
    ├── registro.py             [nuevo]     diálogo de registro de usuario
    └── registro.ui             [nuevo]
```

### 5.3 Qué se conserva, qué se modifica y qué se retira

| Archivo o elemento | Acción | Motivo |
| --- | --- | --- |
| `core/configuracion.py` | Modificar | Agregar escritura de archivos y constantes de préstamos. |
| `core/biblioteca.py` | Modificar | Es el punto de entrada de la lógica; debe crecer ordenadamente. |
| `core/libros.py` | Modificar | Agregar `buscar_avanzado`, CRUD y defaults seguros. |
| `core/usuarios.py` | Modificar | Agregar renovación y cambios de estado. |
| `core/menu.py` | Conservar o retirar | Se conserva mientras la consola sea útil; se retira si la GUI cubre todo. |
| `ui/principal.py` | Modificar | Es el panel central y hoy está incompleto. |
| `ui/catalogo.ui` | Conservar | El diseño ya sirve; solo falta su `.py`. |
| `ui/catalogo.py` | Crear | Conecta el diseño con `Biblioteca`. |
| `ui/acceso.py` | Modificar | Agregar el botón y la apertura del registro. |
| `ui/acceso.ui` | Modificar | Agregar `registrarBtn` junto a `entrarBtn`. |
| `ui/registro.ui` | Crear | Formulario de autorregistro de usuarios. |
| `ui/registro.py` | Crear | Valida y envía los datos a `Biblioteca.registrar_usuario()`. |
| `docs/Plan_mejora_parcial_y_final.md` | Reemplazado | Su contenido quedó integrado en este plan. |
| Textos fijos de marca en los `.ui` | Modificar | Deben venir de `configuracion.py`. |
| `tests/a.py` y `tests/pr.py` | Uso local | Son pruebas sueltas; no forman parte del entregable. |
| `tests/test_biblioteca.py` | Uso local | Está desactualizado respecto al núcleo actual; se ajusta cuando se implementen las funciones nuevas. |

### 5.4 Criterio para retirar código

Un archivo o función se retira solo si:

- ya no lo usa ninguna entrada (`main.py` o `main_interfaz.py`),
- su lógica está cubierta por otra función del núcleo,
- y no forma parte de la demostración de los requisitos del curso.

No se retira `menu.py` mientras `main.py` siga siendo una entrada válida. Si al final la interfaz gráfica es la única entrada, se pueden eliminar `menu.py`, `main.py` y `utilidades.pausa()` en una sola fase de limpieza.

---

## 6. Contrato de interfaces y componentes

Esta sección es la más importante para conectar los `.ui` con los `.py`. Cada tabla indica el `objectName` que ya existe o que debe crearse, qué hace y qué método del núcleo usa.

### 6.1 Cómo se carga un `.ui`

Todas las ventanas usan el mismo patrón:

```python
from pathlib import Path
from PyQt5 import uic

class VentanaEjemplo(QWidget):
    def __init__(self, biblioteca, parent=None):
        super().__init__(parent)
        uic.loadUi(str(Path(__file__).with_suffix(".ui")), self)
        self.biblioteca = biblioteca
        self._conectar_senales()
```

Reglas:

- `uic.loadUi()` se llama una vez en el constructor.
- Los `objectName` del `.ui` quedan como atributos (`self.dniLineEdit`, `self.tablaLibros`, etc.).
- Las señales se conectan después de cargar el `.ui`.
- La ventana no guarda datos en atributos globales; recibe `biblioteca` y, si corresponde, `usuario`.

### 6.2 `acceso.ui` — `VentanaAcceso` (QDialog) ✅

**Propósito:** validar el ingreso y avisar al controlador.

| `objectName` | Widget | Uso |
| --- | --- | --- |
| `dniLineEdit` | `QLineEdit` | DNI de 8 dígitos. |
| `entrarBtn` | `QPushButton` | Valida e ingresa. |
| `registrarBtn` | `QPushButton` | Abre el formulario de registro de un usuario nuevo. |
| `salirBtn` | `QPushButton` | Cierra la aplicación. |
| `ayudaLabel` | `QLabel` | Mensaje de ayuda o error. |
| `tituloLabel` | `QLabel` | Nombre de la biblioteca. |
| `subtituloLabel` | `QLabel` | Texto de bienvenida. |
| `lemaLabel` | `QLabel` | Lema de la biblioteca. |

**Señales actuales:**

| Señal | Método | Qué hace |
| --- | --- | --- |
| `entrarBtn.clicked` | `validar_usuario()` | Busca el DNI, valida estado y vigencia, emite `usuario_autenticado`. |
| `registrarBtn.clicked` | `abrir_registro()` | Abre `VentanaRegistro`; al aceptar, deja el DNI escrito para ingresar. |
| `salirBtn.clicked` | `reject()` | Cierra el diálogo; el controlador termina la aplicación. |

**Mejoras pendientes:**

- Agregar `QIntValidator(0, 99999999)` y `maxLength = 8`.
- Conectar `dniLineEdit.returnPressed` con `validar_usuario()`.
- Mostrar el error en `ayudaLabel` antes de abrir un `QMessageBox`.
- Enfocar el campo al abrir y al limpiar.
- Cargar `tituloLabel` y `lemaLabel` desde `configuracion.py`.
- Agregar el botón `registrarBtn` y el método `abrir_registro()` (ver sección 6.5 y 9.3).

**Criterio de aceptación:** un DNI inexistente, de baja o vencido muestra un mensaje claro y no abre el panel; un DNI válido abre `VentanaPrincipal` con el usuario correcto.

### 6.3 `principal.ui` — `VentanaPrincipal` (QMainWindow) 🟡

**Propósito:** ser el panel central y cambiar de página sin abrir ventanas nuevas.

#### Barra lateral

| `objectName` | Widget | Uso |
| --- | --- | --- |
| `marca1Label` | `QLabel` | Nombre de la biblioteca. |
| `marca2Label` | `QLabel` | Lema o texto corto. |
| `bienvenidaLabel` | `QLabel` | “Hola, {nombre}”. |
| `tipoLabel` | `QLabel` | Tipo y estado del usuario. |
| `navegacionListWidget` | `QListWidget` | Filas 0 a 4: Inicio, Catálogo, Mi membresía, Usuarios, Reportes. |
| `cerrarSesionButton` | `QPushButton` | Vuelve al acceso. |

#### Páginas del `paginasStackedWidget`

| Índice | Página | Contenido | Acceso |
| --- | --- | --- | --- |
| 0 | `inicioPage` | Tarjetas de resumen y accesos rápidos. | Todos. |
| 1 | `catalogoPage` | `catalogo.ui` incrustado. | Todos. |
| 2 | `membresiaPage` | Datos de la membresía. | Todos. |
| 3 | `usuariosPage` | Tabla y búsqueda de usuarios. | Solo administrador. |
| 4 | `reportesPage` | Reporte y exportación. | Solo administrador. |

#### Widgets de la página de inicio

| `objectName` | Uso |
| --- | --- |
| `titulosValorLabel` | Cantidad de títulos. |
| `ejemplaresValorLabel` | Cantidad de ejemplares. |
| `disponiblesValorLabel` | Ejemplares disponibles. |
| `prestadosValorLabel` | Ejemplares prestados. |
| `usuariosValorLabel` | Cantidad de usuarios. |
| `layoutAccesosRapidos` | Contenedor para botones de acceso rápido. |

#### Widgets de membresía

| `objectName` | Uso |
| --- | --- |
| `nombreValorLabel` | Nombre del usuario. |
| `dniValorLabel` | DNI. |
| `tipoValorLabel` | Tipo de usuario. |
| `vencimientoValorLabel` | Fecha de vencimiento. |
| `estadoValorLabel` | Estado calculado. |
| `permisosValorLabel` | “Administrador” o “Consulta y préstamo”. |

#### Widgets de usuarios

| `objectName` | Uso |
| --- | --- |
| `buscarUsuarioLineEdit` | Filtro por DNI, nombre o tipo. |
| `buscarUsuarioButton` | Aplica el filtro. |
| `cantidadUsuariosLabel` | Cantidad de resultados. |
| `tablaUsuarios` | Tabla de usuarios. |

#### Widgets de reportes

| `objectName` | Uso |
| --- | --- |
| `actualizarReporteButton` | Recalcula las matrices. |
| `exportarReporteButton` | Guarda el reporte en un archivo. |
| `reporteTextEdit` | Muestra el reporte en HTML. |

#### Lógica que debe implementar `principal.py`

```python
def _configurar_navegacion(self):
    if not self.usuario.puede_administrar():
        self.navegacionListWidget.item(3).setHidden(True)
        self.navegacionListWidget.item(4).setHidden(True)
    self.navegacionListWidget.currentRowChanged.connect(self._cambiar_pagina)
    self.cerrarSesionButton.clicked.connect(self.cerrar_sesion)

def _cambiar_pagina(self, fila):
    if fila < 0:
        return
    if fila in (3, 4) and not self.usuario.puede_administrar():
        return
    self.paginasStackedWidget.setCurrentIndex(fila)
    if fila == 1:
        self.catalogo.buscar()
    elif fila == 2:
        self._cargar_membresia()
    elif fila == 3:
        self._cargar_usuarios()
    elif fila == 4:
        self._cargar_reporte()
```

**Criterio de aceptación:**

- El estudiante no ve “Usuarios” ni “Reportes”.
- El administrador sí los ve y puede abrirlos.
- El resumen muestra los datos reales.
- “Mi membresía” muestra el usuario conectado.
- “Cerrar sesión” vuelve al acceso.
- Cerrar con la X no deja la aplicación invisible.

### 6.4 `catalogo.ui` — `VentanaCatalogo` (QWidget) ⬜

**Propósito:** listar, buscar y ver la ficha de los libros dentro de `catalogoPage`.

| `objectName` | Widget | Uso |
| --- | --- | --- |
| `buscarLineEdit` | `QLineEdit` | Texto de búsqueda. |
| `campoComboBox` | `QComboBox` | Todo, ISBN, Título, Autor o Categoría. |
| `categoriaComboBox` | `QComboBox` | Filtro por categoría. |
| `ordenarComboBox` | `QComboBox` | Título, autor, categoría o disponibilidad. |
| `soloDisponiblesCheckBox` | `QCheckBox` | Solo libros prestables. |
| `buscarButton` | `QPushButton` | Aplica los filtros. |
| `limpiarButton` | `QPushButton` | Restablece los filtros. |
| `tablaLibros` | `QTableWidget` | Resultados. |
| `detalleTextEdit` | `QTextEdit` | Ficha del libro seleccionado. |
| `cantidadLibrosLabel` | `QLabel` | Cantidad de resultados. |

**Columnas actuales de la tabla:** ISBN, Título, Autor, Categoría, Disponibles y Estado. La ficha del panel derecho puede mostrar sección, estante, ejemplares, disponibles y prestados con `datos_de_un_libro()`.

**Integración en el panel:**

```python
# ui/principal.py
from ui.catalogo import VentanaCatalogo

self.catalogo = VentanaCatalogo(self.biblioteca, self)
self.layoutCatalogoContenedor.addWidget(self.catalogo)
```

**Señales:**

| Señal | Método | Qué hace |
| --- | --- | --- |
| `buscarButton.clicked` | `buscar()` | Pide los resultados a `Biblioteca`. |
| `buscarLineEdit.returnPressed` | `buscar()` | Busca con Enter. |
| `limpiarButton.clicked` | `limpiar_filtros()` | Vuelve al catálogo completo. |
| `categoriaComboBox.currentIndexChanged` | `buscar()` | Filtra al cambiar la categoría. |
| `tablaLibros.itemSelectionChanged` | `mostrar_detalle()` | Actualiza la ficha. |

**Criterio de aceptación:**

- Al abrir la página se ven los 22 libros.
- Buscar “arte” devuelve los 4 libros de la categoría Arte.
- “Limpiar” restaura la lista completa.
- Seleccionar una fila actualiza la ficha.
- Una búsqueda sin resultados no rompe la ventana.

### 6.5 `registro.ui` — `VentanaRegistro` (QDialog) ⬜

**Propósito:** que una persona nueva pueda crear su cuenta desde la pantalla de acceso sin que un administrador tenga que crearla a mano.

**Por qué es un `QDialog`:** es un formulario breve, modal, que se abre desde el acceso, se completa y devuelve `Accepted` o `Rejected`. No necesita barra de estado ni menús. Se abre con `exec_()` porque el acceso necesita esperar el resultado para saber si debe dejar el DNI escrito.

| `objectName` | Widget | Uso |
| --- | --- | --- |
| `dniLineEdit` | `QLineEdit` | DNI nuevo, 8 dígitos. |
| `nombreLineEdit` | `QLineEdit` | Nombre completo. |
| `tipoComboBox` | `QComboBox` | Solo `Estudiante` o `Docente`; nunca `Administrador`. |
| `membresiaLabel` | `QLabel` | Explica que la membresía dura 3 meses y muestra la fecha estimada de vencimiento. |
| `ayudaRegistroLabel` | `QLabel` | Mensaje de error o confirmación. |
| `registrarButton` | `QPushButton` | Valida, crea el usuario y cierra. |
| `cancelarButton` | `QPushButton` | Cierra sin crear nada. |

**Señales:**

| Señal | Método | Qué hace |
| --- | --- | --- |
| `registrarButton.clicked` | `registrar()` | Valida los campos y llama a `Biblioteca.registrar_usuario()`. |
| `cancelarButton.clicked` | `reject()` | Cierra el diálogo sin guardar. |
| `dniLineEdit.returnPressed` | `registrar()` | Permite confirmar con Enter. |

**Reglas del registro:**

1. El DNI debe tener 8 dígitos numéricos y no debe existir ya.
2. El nombre no puede quedar vacío.
3. El tipo solo puede ser `Estudiante` o `Docente`.
4. El usuario se crea con `activo = True`.
5. El vencimiento se calcula sumando **3 meses** a la fecha del registro (`MESES_DE_MEMBRESIA = 3`).
6. Al terminar, no se abre el panel automáticamente: se cierra el diálogo, se escribe el DNI en `dniLineEdit` del acceso y se muestra “Registro completado. Ya puedes ingresar.”.
7. Un administrador puede reutilizar este mismo diálogo desde la página de usuarios, pero ahí sí se permite elegir `Administrador`.

**Métodos del núcleo:** `utilidades.sumar_meses()`, `Biblioteca.registrar_usuario()` y `Biblioteca.guardar_usuarios()`.

**Criterio de aceptación:** un DNI nuevo se guarda en `usuarios.json` con vencimiento a 3 meses; un DNI repetido muestra un error y no duplica el registro; no se puede crear un administrador desde el acceso.

> **Nota sobre botones:** se usan dos `QPushButton` con nombre propio (`registrarButton` y `cancelarButton`) para poder conectarlos uno por uno desde Python. `QDialogButtonBox` también sirve, pero sus botones estándar se conectan con `accepted` y `rejected`, no con un nombre individual. Para este proyecto conviene el botón con nombre explícito.

### 6.6 Página de membresía 🟡

No necesita un `.ui` aparte porque ya es `membresiaPage` dentro de `principal.ui`.

```python
datos = self.usuario.datos_de_membresia()
self.nombreValorLabel.setText(datos["nombre"])
self.dniValorLabel.setText(datos["dni"])
self.tipoValorLabel.setText(datos["tipo"])
self.vencimientoValorLabel.setText(datos["vencimiento_membresia"])
self.estadoValorLabel.setText(datos["estado"])
self.permisosValorLabel.setText(
    "Administrador" if self.usuario.puede_administrar() else "Consulta y préstamo"
)
```

**Criterio de aceptación:** los datos coinciden con el usuario que inició sesión y el estado se calcula con la fecha actual.

### 6.7 Página de usuarios 🟡

Solo para administradores. Se llena con `biblioteca.datos_de_los_usuarios()`.

| Columna | Dato |
| --- | --- |
| DNI | `dni` |
| Nombre | `nombre` |
| Tipo | `tipo` |
| Vencimiento | `vencimiento_membresia` |
| Estado | `estado` |
| Administra | `puede_administrar` (si existe) |

**Acciones que conviene agregar como botones:**

- `nuevoUsuarioButton`: abre un formulario de alta.
- `renovarMembresiaButton`: pide una fecha y actualiza.
- `darDeBajaButton`: cambia `activo` a `False`.
- `reactivarButton`: cambia `activo` a `True`.

**Criterio de aceptación:** el administrador puede buscar, renovar, dar de baja y reactivar; la tabla se actualiza después de cada operación; un usuario de baja no puede entrar.

### 6.8 Página de reportes 🟡

Se llena con las funciones de `core/reportes.py` y se muestra en `reporteTextEdit`.

| Botón | Acción |
| --- | --- |
| `actualizarReporteButton` | Recalcula las matrices y el resumen. |
| `exportarReporteButton` | Guarda el contenido en `datos/reportes/` o en la ruta que elija el usuario. |

**Criterio de aceptación:** los totales del reporte coinciden con el resumen, las matrices se ven como tablas y la exportación genera un archivo legible.

### 6.9 `libro_form.ui` — `VentanaLibro` (QDialog) ⬜

Formulario para registrar o editar un libro. Se abre desde el catálogo solo si el usuario es administrador.

| `objectName` | Widget | Uso |
| --- | --- | --- |
| `isbnLineEdit` | `QLineEdit` | ISBN de 13 dígitos. |
| `tituloLineEdit` | `QLineEdit` | Título. |
| `autorLineEdit` | `QLineEdit` | Autor. |
| `categoriaComboBox` | `QComboBox` | Categoría del libro. |
| `seccionComboBox` | `QComboBox` | Sección A–E. |
| `estanteSpinBox` | `QSpinBox` | Estante 1–3. |
| `ejemplaresSpinBox` | `QSpinBox` | Total de ejemplares. |
| `disponiblesSpinBox` | `QSpinBox` | Ejemplares disponibles. |
| `guardarButton` | `QPushButton` | Guarda y cierra. |
| `cancelarButton` | `QPushButton` | Cancela. |

**Métodos del núcleo:** `Biblioteca.registrar_libro(datos)` y `Biblioteca.actualizar_libro(isbn, datos)`.

**Criterio de aceptación:** el libro nuevo aparece en la tabla y sigue ahí después de cerrar y abrir el programa; un ISBN repetido muestra un error.

### 6.10 `prestamo.ui` — `VentanaPrestamo` (QDialog) ⬜

Formulario para prestar un ejemplar.

| `objectName` | Widget | Uso |
| --- | --- | --- |
| `dniLineEdit` | `QLineEdit` | Usuario que recibe el préstamo. |
| `isbnLineEdit` | `QLineEdit` | Libro a prestar. |
| `tituloLibroLabel` | `QLabel` | Título encontrado. |
| `disponiblesLabel` | `QLabel` | Stock actual. |
| `prestamoActivoLabel` | `QLabel` | Aviso si el usuario ya tiene un libro prestado. |
| `fechaLimiteLabel` | `QLabel` | Fecha calculada de devolución. |
| `prestarButton` | `QPushButton` | Registra el préstamo. |
| `cancelarButton` | `QPushButton` | Cancela. |

**Método del núcleo:** `Biblioteca.prestar(isbn, dni)`.

**Reglas:** membresía vigente, usuario activo, stock suficiente y **ningún préstamo activo**. Si el usuario ya tiene un libro, el formulario debe mostrar `prestamoActivoLabel` y deshabilitar `prestarButton` hasta que lo devuelva. Al prestar, `disponibles` baja en 1 y se crea un registro en `prestamos.json`.

**Criterio de aceptación:** el stock baja, el préstamo aparece en el historial y no se puede prestar un segundo libro mientras el primero siga activo. Si no hay ejemplares, también se bloquea.

### 6.11 `devolucion.ui` — `VentanaDevolucion` (QDialog) ⬜

Formulario para devolver un ejemplar.

| `objectName` | Widget | Uso |
| --- | --- | --- |
| `dniLineEdit` | `QLineEdit` | Usuario que devuelve. |
| `isbnLineEdit` | `QLineEdit` | Libro devuelto. |
| `fechaLimiteLabel` | `QLabel` | Fecha límite del préstamo. |
| `fechaDevolucionLabel` | `QLabel` | Fecha de hoy. |
| `estadoPrestamoLabel` | `QLabel` | “En plazo” o “Vencido”. |
| `devolverButton` | `QPushButton` | Registra la devolución. |
| `cancelarButton` | `QPushButton` | Cancela. |

**Método del núcleo:** `Biblioteca.devolver(isbn, dni)`.

**Reglas:** debe existir un préstamo activo para ese libro y usuario; al devolver, `disponibles` sube en 1, el préstamo se marca como devuelto y el usuario queda libre para pedir otro. No se calcula ni se muestra multa.

**Criterio de aceptación:** el stock sube, el préstamo deja de estar activo y el usuario puede volver a prestar. Si la fecha límite ya pasó, se marca “Vencido”, pero no se cobra nada.

### 6.12 Convención de nombres para widgets

| Tipo | Sufijo | Ejemplo |
| --- | --- | --- |
| `QLabel` | `Label` | `estadoValorLabel` |
| `QLineEdit` | `LineEdit` | `dniLineEdit` |
| `QTextEdit` | `TextEdit` | `detalleTextEdit` |
| `QPushButton` | `Button` o `Btn` | `buscarButton`, `entrarBtn` |
| `QComboBox` | `ComboBox` | `categoriaComboBox` |
| `QSpinBox` | `SpinBox` | `ejemplaresSpinBox` |
| `QCheckBox` | `CheckBox` | `soloDisponiblesCheckBox` |
| `QListWidget` | `ListWidget` | `navegacionListWidget` |
| `QTableWidget` | `tabla...` | `tablaLibros`, `tablaUsuarios` |
| `QStackedWidget` | `...StackedWidget` | `paginasStackedWidget` |

**Regla de oro:** si un widget tiene un nombre genérico (`lineEdit_2`, `pushButton_3`), el código no sabe qué dato guarda ni qué acción dispara. Se renombra en QtDesigner antes de conectarlo.

### 6.13 Por qué se usa cada tipo de ventana y widget

Esta sección explica las decisiones de Qt para que no se elijan componentes por costumbre. La regla general es usar el componente más simple que resuelva la necesidad y no abrir una ventana nueva si basta con cambiar de página.

#### QMainWindow, QDialog y QWidget

| Necesidad | Componente | Por qué se usa | Por qué no otro |
| --- | --- | --- | --- |
| Ventana principal de la aplicación | `QMainWindow` | Tiene un `centralwidget`, barra de estado (`statusBar`) y espacio para menús o barras de herramientas. Es la ventana que contiene el panel completo. | `QWidget` no trae barra de estado ni menús; `QDialog` está pensado para tareas breves y no para ser la ventana principal. |
| Pantalla de acceso o formulario de un solo paso | `QDialog` | Se puede abrir con `exec_()` y devolver `Accepted` o `Rejected`; permite modalidad y botones de aceptar/cancelar. | `QMainWindow` agrega menús y barra de estado que no se necesitan; `QWidget` obliga a manejar a mano el cierre, la modalidad y el resultado. |
| Página que se incrusta dentro de otra ventana | `QWidget` | Es un lienzo reutilizable que se agrega a un layout. No tiene marco propio ni botones de ventana. | `QMainWindow` no está pensado para incrustarse; `QDialog` se comporta como una ventana emergente y no como una página. |
| Varias pantallas dentro de una sola ventana | `QStackedWidget` | Cambia de página sin abrir ni cerrar ventanas; conserva el estado de cada página y evita parpadeos. | Abrir varias `QMainWindow` duplica ventanas y complica el cierre; `QTabWidget` muestra pestañas que no encajan con el menú lateral actual. |

**En el proyecto:**

- `VentanaPrincipal` es `QMainWindow` porque es la ventana que contiene todo y puede usar `statusBar().showMessage(...)`.
- `VentanaAcceso` es `QDialog` porque es una pantalla de entrada con una acción concreta: validar el DNI. En el código actual se muestra con `show()` para que el controlador escuche la señal; también podría usarse `exec_()` si se prefiere modal.
- `VentanaRegistro` es `QDialog` porque es un formulario breve que se abre desde el acceso y devuelve un resultado.
- `VentanaCatalogo` será `QWidget` porque se incrusta en `catalogoPage`.
- `VentanaLibro`, `VentanaPrestamo` y `VentanaDevolucion` serán `QDialog` porque son formularios que se abren, se completan y devuelven un resultado.

**Ejemplo de `QDialog` modal:**

```python
dialogo = VentanaPrestamo(self.biblioteca, self.usuario, parent=self)
if dialogo.exec_() == QDialog.Accepted:
    self._actualizar_despues_del_prestamo()
```

**Ejemplo de `QWidget` incrustado:**

```python
self.catalogo = VentanaCatalogo(self.biblioteca, self)
self.layoutCatalogoContenedor.addWidget(self.catalogo)
```

**Ejemplo de `QMainWindow`:**

```python
class VentanaPrincipal(QMainWindow):
    def __init__(self, biblioteca, usuario):
        super().__init__()
        uic.loadUi("principal.ui", self)
        self.statusBar().showMessage("Sesión iniciada")
```

#### Contenedores y navegación

| Componente | Para qué se usa en el proyecto | Por qué | Alternativas descartadas |
| --- | --- | --- | --- |
| `QStackedWidget` | Cambiar entre Inicio, Catálogo, Membresía, Usuarios y Reportes. | Mantiene las cinco páginas cargadas y solo cambia la visible; el índice coincide con la fila del menú. | Abrir cinco ventanas independientes, que se acumulan y pierden el estado. |
| `QListWidget` | Menú lateral de navegación. | Muestra las opciones siempre visibles y permite ocultar filas de administración con `item.setHidden(True)`. | `QComboBox` esconde las opciones; `QTabWidget` cambia el diseño y no permite ocultar pestañas tan fácilmente. |
| `QFrame` | Tarjetas de resumen, avisos y separadores visuales. | Agrupa visualmente sin agregar un título obligatorio. | `QGroupBox` sirve para grupos con título; para una tarjeta simple es más pesado. |
| `QSplitter` | Separar la tabla del catálogo y la ficha del libro. | El usuario puede ensanchar la tabla o la ficha según lo que necesite. | Un layout fijo obliga a dejar tamaños que no siempre son cómodos. |
| `QVBoxLayout`, `QHBoxLayout`, `QFormLayout`, `QGridLayout` | Organizar widgets. | Se adaptan al tamaño de la ventana y evitan posiciones absolutas. | `setGeometry` fijo se rompe al cambiar de resolución. |

**Ejemplo de navegación:**

```python
def _cambiar_pagina(self, fila):
    if fila < 0:
        return
    self.paginasStackedWidget.setCurrentIndex(fila)
```

**Ejemplo de menú lateral:**

```python
if not self.usuario.puede_administrar():
    self.navegacionListWidget.item(3).setHidden(True)  # Usuarios
    self.navegacionListWidget.item(4).setHidden(True)  # Reportes
```

#### Entradas y filtros

| Componente | Para qué se usa en el proyecto | Por qué | Alternativas descartadas |
| --- | --- | --- | --- |
| `QLineEdit` | DNI, ISBN, búsqueda y campos de una sola línea. | Es liviano, tiene `placeholderText`, `maxLength` y se puede validar con `QValidator`. | `QTextEdit` es para varias líneas y no tiene validadores de una línea. |
| `QComboBox` | Campo de búsqueda, categoría y orden. | Ahorra espacio y limita las opciones a valores válidos. | `QListWidget` ocuparía mucho espacio; varios `QRadioButton` serían incómodos si hay muchas categorías. |
| `QCheckBox` | “Solo disponibles”. | Representa una decisión booleana simple. | Dos `QRadioButton` para sí/no son más verbosos. |
| `QSpinBox` | Estante, ejemplares y disponibles en el formulario de libro. | Solo permite números dentro de un rango y evita validar texto a mano. | `QLineEdit` obliga a convertir y validar; `QSlider` no muestra el número exacto. |
| `QCalendarWidget` | Renovación de membresía o fecha de devolución. | Evita escribir fechas a mano y reduce errores de formato. | `QLineEdit` con fecha es más liviano, pero exige validación y es más fácil equivocarse. |

**Ejemplo de combo:**

```python
self.campoComboBox.addItem("Todo el catálogo", "Todo")
self.campoComboBox.addItem("Título", "titulo")
self.campoComboBox.addItem("Autor", "autor")
```

**Ejemplo de spin box:**

```python
self.estanteSpinBox.setMinimum(1)
self.estanteSpinBox.setMaximum(configuracion.CANTIDAD_DE_ESTANTES)
```

#### Datos y salida

| Componente | Para qué se usa en el proyecto | Por qué | Alternativas descartadas |
| --- | --- | --- | --- |
| `QTableWidget` | Tabla de libros y tabla de usuarios. | Muestra varias columnas, encabezados, selección por fila y ordenamiento sin escribir un modelo de datos. | `QListWidget` solo tiene una columna; `QTableView` con un modelo es más potente, pero innecesario para 22 libros y 13 usuarios. |
| `QTextEdit` | Ficha del libro y reporte general. | Permite texto largo con formato HTML, scroll y selección. | `QLabel` se corta con textos largos; `QPlainTextEdit` no interpreta HTML. |
| `QLabel` | Títulos, valores de resumen y mensajes cortos. | Es el componente correcto para texto estático y etiquetas de datos. | `QTextEdit` para un título es demasiado pesado y editable si no se configura. |
| `QMessageBox` | Errores críticos, confirmaciones y avisos. | Bloquea la acción y obliga al usuario a leer el mensaje. | `print()` no se ve en la interfaz; un `QLabel` es mejor para ayudas simples, pero no para confirmar una acción. |
| `QFileDialog` | Exportar el reporte. | Permite elegir la ruta y el nombre del archivo. | Una ruta fija obliga a buscar el archivo a mano y puede fallar por permisos. |

**Ejemplo de tabla:**

```python
self.tablaLibros.setRowCount(len(datos))
for fila, libro in enumerate(datos):
    self.tablaLibros.setItem(fila, 0, QTableWidgetItem(libro["isbn"]))
    self.tablaLibros.setItem(fila, 1, QTableWidgetItem(libro["titulo"]))
```

**Ejemplo de texto con formato:**

```python
self.detalleTextEdit.setHtml(f"<h2>{libro['titulo']}</h2><p>{libro['autor']}</p>")
```

**Ejemplo de confirmación:**

```python
respuesta = QMessageBox.question(
    self,
    "Cerrar sesión",
    "¿Deseas volver a la pantalla de acceso?",
    QMessageBox.Yes | QMessageBox.No,
)
```

#### Acciones

| Componente | Para qué se usa en el proyecto | Por qué | Alternativas descartadas |
| --- | --- | --- | --- |
| `QPushButton` | Entrar, buscar, limpiar, prestar, devolver, guardar y cerrar sesión. | Es el control estándar para una acción clara y visible. | `QToolButton` es mejor para iconos sin texto; `QCommandLinkButton` es para asistentes, no para acciones comunes. |
| `QDialogButtonBox` | Botones de aceptar/cancelar en formularios. | Ordena los botones según la plataforma y devuelve `Accepted` o `Rejected`. | Dos `QPushButton` sueltos funcionan, pero hay que alinear y conectar todo a mano. |

#### Criterio rápido de decisión

| Si necesitas... | Usa... |
| --- | --- |
| Una ventana principal con barra de estado | `QMainWindow` |
| Un login o formulario que devuelve un resultado | `QDialog` |
| Una página para incrustar | `QWidget` |
| Cambiar entre páginas sin abrir ventanas | `QStackedWidget` |
| Un menú lateral visible | `QListWidget` |
| Una tabla con columnas | `QTableWidget` |
| Texto largo con formato | `QTextEdit` |
| Una etiqueta corta | `QLabel` |
| Una entrada de texto de una línea | `QLineEdit` |
| Elegir entre opciones fijas | `QComboBox` |
| Activar o desactivar una opción | `QCheckBox` |
| Un número dentro de un rango | `QSpinBox` |
| Una fecha | `QCalendarWidget` |
| Confirmar o avisar algo importante | `QMessageBox` |
| Elegir dónde guardar un archivo | `QFileDialog` |

La idea no es usar todos los componentes, sino elegir el que mejor representa el dato y la acción. Por ejemplo: para “solo disponibles” se usa un `QCheckBox` porque es una decisión de sí/no; para la categoría se usa un `QComboBox` porque son opciones cerradas; para el reporte se usa un `QTextEdit` porque es texto largo con formato.

### 6.14 Cómo armar los layouts y qué nombres usar

Esta sección es la receta para editar los `.ui` en QtDesigner. La idea es que cualquier integrante del equipo abra el archivo y vea la misma estructura: un layout raíz, un formulario para los datos, una zona de mensajes y una fila de botones.

#### Reglas generales de construcción

1. El widget raíz ya tiene su clase (`QDialog`, `QWidget` o `QMainWindow`); no se cambia.
2. Todo el contenido va dentro de un layout raíz. Nunca se usan posiciones absolutas.
3. Los datos se ordenan con `QFormLayout` (etiqueta a la izquierda, campo a la derecha).
4. Los botones van en un `QHBoxLayout` al final, con `addStretch()` antes para empujarlos a la derecha.
5. Los mensajes de error van en un `QLabel` con `wordWrap` activado, debajo de los campos.
6. Cada widget que se use desde Python lleva un `objectName` claro; los decorativos pueden quedar sin nombre.
7. Los botones nuevos usan el sufijo `Button` (`registrarButton`). Los que ya existen con `Btn` (`entrarBtn`, `salirBtn`) se conservan para no romper `acceso.py`.

#### `acceso.ui` (modificar)

```text
QDialog VentanaAcceso
└── QVBoxLayout layoutPrincipal
    ├── QFrame tarjetaFrame
    │   └── QVBoxLayout layoutTarjeta
    │       ├── QLabel tituloLabel
    │       ├── QLabel subtituloLabel
    │       ├── QLabel dniLabel
    │       ├── QLineEdit dniLineEdit
    │       ├── QLabel ayudaLabel
    │       ├── QPushButton entrarBtn
    │       ├── QPushButton registrarBtn      ← nuevo
    │       └── QPushButton salirBtn
    └── QLabel lemaLabel
```

`registrarBtn` se coloca debajo de `entrarBtn`, con el texto “Registrarme”. No hace falta un layout nuevo: el `layoutTarjeta` ya es vertical.

#### `registro.ui` (nuevo)

```text
QDialog VentanaRegistro
└── QVBoxLayout layoutRegistro
    ├── QLabel tituloRegistroLabel
    ├── QFormLayout formularioRegistro
    │   ├── QLabel dniLabel          → QLineEdit dniLineEdit
    │   ├── QLabel nombreLabel       → QLineEdit nombreLineEdit
    │   └── QLabel tipoLabel         → QComboBox tipoComboBox
    ├── QLabel membresiaLabel
    ├── QLabel ayudaRegistroLabel
    └── QHBoxLayout layoutBotonesRegistro
        ├── (stretch)
        ├── QPushButton registrarButton
        └── QPushButton cancelarButton
```

- `tipoComboBox` se llena en Python con `["Estudiante", "Docente"]`; en Designer puede quedar vacío.
- `membresiaLabel` se actualiza al abrir con la fecha calculada: “Membresía por 3 meses: vence el 2027-02-10”.
- `registrarButton` debe ser el botón por defecto (`setDefault(True)`) y `cancelarButton` el de escape.

#### `libro_form.ui` (nuevo)

```text
QDialog VentanaLibro
└── QVBoxLayout layoutLibro
    ├── QLabel tituloFormularioLabel
    ├── QFormLayout formularioLibro
    │   ├── ISBN        → QLineEdit isbnLineEdit
    │   ├── Título      → QLineEdit tituloLineEdit
    │   ├── Autor       → QLineEdit autorLineEdit
    │   ├── Categoría   → QComboBox categoriaComboBox
    │   ├── Sección     → QComboBox seccionComboBox
    │   ├── Estante     → QSpinBox estanteSpinBox
    │   ├── Ejemplares  → QSpinBox ejemplaresSpinBox
    │   └── Disponibles → QSpinBox disponiblesSpinBox
    ├── QLabel ayudaLibroLabel
    └── QHBoxLayout layoutBotonesLibro
        ├── (stretch)
        ├── QPushButton guardarButton
        └── QPushButton cancelarButton
```

Al abrir en modo edición, `isbnLineEdit` se deshabilita (`setEnabled(False)`) porque el ISBN es la clave del libro y no se cambia.

#### `prestamo.ui` (nuevo)

```text
QDialog VentanaPrestamo
└── QVBoxLayout layoutPrestamo
    ├── QLabel tituloPrestamoLabel
    ├── QFormLayout formularioPrestamo
    │   ├── DNI del usuario → QLineEdit dniLineEdit
    │   └── ISBN del libro  → QLineEdit isbnLineEdit
    ├── QLabel tituloLibroLabel
    ├── QLabel disponiblesLabel
    ├── QLabel prestamoActivoLabel
    ├── QLabel fechaLimiteLabel
    ├── QLabel ayudaPrestamoLabel
    └── QHBoxLayout layoutBotonesPrestamo
        ├── (stretch)
        ├── QPushButton prestarButton
        └── QPushButton cancelarButton
```

#### `devolucion.ui` (nuevo)

```text
QDialog VentanaDevolucion
└── QVBoxLayout layoutDevolucion
    ├── QLabel tituloDevolucionLabel
    ├── QFormLayout formularioDevolucion
    │   ├── DNI del usuario → QLineEdit dniLineEdit
    │   └── ISBN del libro  → QLineEdit isbnLineEdit
    ├── QLabel fechaLimiteLabel
    ├── QLabel fechaDevolucionLabel
    ├── QLabel estadoPrestamoLabel
    ├── QLabel ayudaDevolucionLabel
    └── QHBoxLayout layoutBotonesDevolucion
        ├── (stretch)
        ├── QPushButton devolverButton
        └── QPushButton cancelarButton
```

#### `catalogo.ui` (modificar)

La cabecera actual (`layoutCabeceraCatalogo`) tiene el título y la cantidad. Debajo se agrega una fila de acciones para administradores:

```text
QVBoxLayout layoutCatalogo
├── QHBoxLayout layoutCabeceraCatalogo   (ya existe)
├── QHBoxLayout layoutAccionesCatalogo   ← nuevo
│   ├── QPushButton nuevoLibroButton
│   ├── QPushButton editarLibroButton
│   ├── QPushButton eliminarLibroButton
│   ├── (stretch)
│   ├── QPushButton prestarLibroButton
│   └── QPushButton devolverLibroButton
├── QFrame filtrosFrame                  (ya existe)
└── QSplitter splitterCatalogo           (ya existe)
```

Los tres primeros botones solo se muestran si `usuario.puede_administrar()`. `prestarLibroButton` y `devolverLibroButton` pueden estar visibles para todos, porque un usuario común también puede pedir y devolver.

#### `principal.ui` (modificar)

En `usuariosPage`, debajo de `layoutCabeceraUsuarios`, se agrega:

```text
QVBoxLayout layoutUsuarios
├── QHBoxLayout layoutCabeceraUsuarios   (ya existe: título, búsqueda, buscar)
├── QHBoxLayout layoutAccionesUsuarios   ← nuevo
│   ├── QPushButton nuevoUsuarioButton
│   ├── QPushButton renovarMembresiaButton
│   ├── QPushButton darDeBajaButton
│   ├── QPushButton reactivarButton
│   └── (stretch)
├── QLabel cantidadUsuariosLabel         (ya existe)
└── QTableWidget tablaUsuarios           (ya existe)
```

En `inicioPage`, el layout `layoutAccesosRapidos` ya existe y está vacío. Ahí se agregan los botones de acceso directo:

```text
QHBoxLayout layoutAccesosRapidos
├── QPushButton catalogoRapidoButton
├── QPushButton prestamoRapidoButton
├── QPushButton devolucionRapidaButton
└── QPushButton membresiaRapidaButton
```

#### Tabla de nombres y uso desde Python

| `objectName` en Designer | Atributo en Python | Conexión típica |
| --- | --- | --- |
| `registrarBtn` | `self.registrarBtn` | `clicked.connect(self.abrir_registro)` |
| `registrarButton` | `self.registrarButton` | `clicked.connect(self.registrar)` |
| `cancelarButton` | `self.cancelarButton` | `clicked.connect(self.reject)` |
| `nuevoLibroButton` | `self.nuevoLibroButton` | `clicked.connect(self._nuevo_libro)` |
| `prestarButton` | `self.prestarButton` | `clicked.connect(self.prestar)` |
| `devolverButton` | `self.devolverButton` | `clicked.connect(self.devolver)` |
| `nuevoUsuarioButton` | `self.nuevoUsuarioButton` | `clicked.connect(self._nuevo_usuario)` |
| `renovarMembresiaButton` | `self.renovarMembresiaButton` | `clicked.connect(self._renovar_membresia)` |
| `layoutAccesosRapidos` | `self.layoutAccesosRapidos` | `addWidget(...)` si se crea en código |

**Ejemplo de por qué el nombre importa:**

```python
# Si el botón se llama registrarButton en el .ui, en Python se usa así:
self.registrarButton.clicked.connect(self.registrar)

# Si se deja como pushButton_2, el código queda ilegible:
self.pushButton_2.clicked.connect(self.registrar)
```

#### Detalles de QtDesigner que conviene revisar

- Aplicar el layout raíz con “Lay out vertically” o “Lay out horizontally”; si aparece el ícono rojo de layout faltante, no está aplicado.
- Poner `minimumWidth` a los formularios (por ejemplo, 420 px) para que no se achiquen de más.
- Activar `wordWrap` en las etiquetas de ayuda y mensajes largos.
- Ordenar el recorrido con “Edit Tab Order” para que Enter pase de un campo al siguiente.
- No cambiar el `objectName` de widgets que ya usa el código (`dniLineEdit`, `entrarBtn`, etc.).
- Los layouts no se ven en la ventana final, pero sí se usan desde Python cuando se agregan widgets en tiempo de ejecución.

---

## 7. Lógica del core

### 7.1 API actual que se debe reutilizar

| Método actual | Retorna | Dónde se usa |
| --- | --- | --- |
| `Biblioteca.resumen()` | Diccionario con títulos, ejemplares, disponibles, prestados, usuarios y fecha. | Inicio y reportes. |
| `Biblioteca.libro(isbn)` | Objeto `Libro`. | Ficha y préstamos. |
| `Biblioteca.usuario(dni)` | Objeto `Usuario` o `Administrador`. | Acceso y préstamos. |
| `Biblioteca.datos_del_catalogo()` | Lista de diccionarios. | Catálogo completo. |
| `Biblioteca.datos_de_un_libro(isbn)` | Diccionario. | Ficha del libro. |
| `Biblioteca.buscar(texto)` | Lista de diccionarios. | Búsqueda simple. |
| `Biblioteca.datos_de_los_usuarios()` | Lista de diccionarios. | Página de usuarios. |
| `Biblioteca.datos_de_membresia(dni)` | Diccionario. | Membresía. |
| `Libro.datos_para_pantalla()` | Diccionario extendido. | Tabla y ficha. |
| `Usuario.datos_de_membresia()` | Diccionario. | Página de membresía. |
| `Usuario.estado()` | Texto del estado. | Membresía y usuarios. |
| `Usuario.puede_administrar()` | `True` o `False`. | Visibilidad de opciones. |

No se debe volver a escribir esta lógica en las ventanas. Si una ventana necesita un dato, se agrega un método en `Biblioteca` y se llama desde la interfaz.

### 7.2 Ajustes a funciones existentes

| Archivo | Ajuste | Motivo |
| --- | --- | --- |
| `core/biblioteca.py` | Cambiar `from core import ...` por `from . import ...`. | Consistencia y ejecución como paquete. |
| `core/biblioteca.py` | Agregar `buscar_avanzado(...)`. | Filtros del catálogo. |
| `core/biblioteca.py` | Agregar `guardar_datos(...)`. | Persistencia. |
| `core/libros.py` | Poner valores por defecto en `crear_libro()`. | Evitar `TypeError` con JSON incompleto. |
| `core/libros.py` | Revisar `se_puede_prestar()` y documentar la regla del último ejemplar. | Evitar decisiones contradictorias. |
| `core/libros.py` | Agregar `prestar_ejemplar()` y `devolver_ejemplar()` para modificar el stock con validación. | Evitar que la interfaz cambie `disponibles` directamente. |
| `core/configuracion.py` | Agregar `escribir_archivo()`, constantes de préstamos y `MESES_DE_MEMBRESIA`. | Persistencia y reglas centralizadas. |
| `core/utilidades.py` | Agregar `formatear_fecha()`, `sumar_dias()` y `sumar_meses()`. | Calcular vencimientos y fechas límite. |
| `core/usuarios.py` | Agregar `a_diccionario()` para poder guardar usuarios. | Persistencia de altas y renovaciones. |
| `core/errores.py` | Agregar `ErrorDeArchivo`, `ErrorDePrestamo` y `ErrorDeMembresia`. | Mensajes claros por tipo de error. |
| `ui/acceso.py` | Agregar validator, Enter, mensaje inline y `abrir_registro()`. | Mejor experiencia de uso y autorregistro. |
| `ui/acceso.ui` | Agregar `registrarBtn`. | Abrir el formulario de registro. |
| `ui/principal.py` | Completar navegación, datos y cierre. | Es el panel central. |
| `ui/principal.ui` | Agregar un contenedor para el catálogo y quitar textos fijos. | Integración y configuración central. |

### 7.3 Nuevas clases y funciones

#### `core/prestamos.py`

| Elemento | Tipo | Responsabilidad |
| --- | --- | --- |
| `Prestamo` | Clase | Guardar ISBN, DNI, fecha de préstamo, fecha límite, fecha de devolución y estado. |
| `prestamo.a_diccionario()` | Método | Convertir el préstamo a un diccionario para JSON. |
| `prestamo.esta_activo()` | Método | Indicar si todavía no se devolvió. |
| `prestamo.esta_vencido(fecha_hoy)` | Método | Comparar la fecha límite con la fecha actual; solo sirve para mostrarlo en reportes. |
| `prestamo.marcar_devuelto(fecha)` | Método | Guardar la fecha de devolución y cambiar el estado a “devuelto”. |
| `crear_prestamo(datos)` | Función | Construir un `Prestamo` desde un diccionario del JSON. |

#### `core/biblioteca.py`

| Método nuevo | Qué hace |
| --- | --- |
| `buscar_avanzado(texto, campo, categoria, solo_disponibles, ordenar_por, limite)` | Filtra el catálogo para la interfaz. |
| `guardar_libros()` | Escribe `libros.json`. |
| `guardar_usuarios()` | Escribe `usuarios.json`. |
| `guardar_prestamos()` | Escribe `prestamos.json`. |
| `registrar_libro(datos)` | Crea un libro y guarda. |
| `actualizar_libro(isbn, datos)` | Modifica un libro y guarda. |
| `eliminar_libro(isbn)` | Elimina un libro sin préstamos activos. |
| `registrar_usuario(datos, permitir_administrador=False)` | Crea un usuario, calcula su vencimiento si no viene en `datos` y guarda. |
| `actualizar_usuario(dni, datos)` | Modifica un usuario y guarda. |
| `dar_de_baja(dni)` | Marca al usuario como inactivo. |
| `reactivar(dni)` | Vuelve a activar al usuario. |
| `renovar_membresia(dni, meses=None)` | Extiende el vencimiento desde hoy o desde el actual, el que sea mayor. |
| `prestar(isbn, dni)` | Valida que el usuario no tenga otro préstamo activo y registra uno nuevo. |
| `devolver(isbn, dni)` | Registra la devolución, repone el stock y libera al usuario. |
| `prestamo_activo_de_usuario(dni)` | Devuelve el préstamo activo del usuario o `None`. |
| `prestamos_activos()` | Lista los préstamos no devueltos. |
| `prestamos_de_usuario(dni)` | Historial de un usuario. |
| `reporte_general()` | Devuelve el resumen y las matrices para la interfaz. |

#### `core/usuarios.py`

| Elemento nuevo | Tipo | Responsabilidad |
| --- | --- | --- |
| `usuario.a_diccionario()` | Método | Convertir DNI, nombre, tipo, vencimiento y estado activo en un diccionario para JSON. |
| `usuario.renovar_hasta(nueva_fecha)` | Método | Cambiar la fecha de vencimiento y devolver la nueva fecha. |

`Administrador` hereda `a_diccionario()` y `renovar_hasta()`; no hace falta repetirlos.

#### `core/configuracion.py`

| Elemento nuevo | Valor sugerido | Uso |
| --- | --- | --- |
| `MAXIMO_PRESTAMOS_POR_USUARIO` | `1` | Un solo préstamo activo por usuario. |
| `DIAS_DE_PRESTAMO` | `15` | Plazo de devolución; si vence, solo se marca como vencido. |
| `MESES_DE_MEMBRESIA` | `3` | Duración de la membresía al registrarse o renovarse. |
| `ESTADOS_DE_PRESTAMO` | `["activo", "devuelto"]` | Valores válidos del campo `estado`. |
| `CARPETA_REPORTES` | `datos/reportes` | Exportaciones. |
| `ARCHIVO_BITACORA` | `bitacora.txt` | Registro de movimientos. |
| `escribir_archivo(nombre, datos)` | Función | Guardar JSON de forma segura. |
| `agregar_a_bitacora(texto)` | Función | Agregar una línea al archivo de texto. |

#### `core/reportes.py`

Ver la sección 8.

### 7.4 Modelo de datos

#### `datos/libros.json`

```json
{
  "isbn": "9788437604947",
  "titulo": "Cien años de soledad",
  "autor": "Gabriel García Márquez",
  "categoria": "Literatura",
  "seccion": "A",
  "estante": 1,
  "ejemplares": 3,
  "disponibles": 2
}
```

#### `datos/usuarios.json`

```json
{
  "dni": "11111111",
  "nombre": "P_ESTUDIANTE",
  "tipo": "Estudiante",
  "vencimiento_membresia": "2027-12-31",
  "activo": true
}
```

No hace falta guardar la fecha de registro: al crear el usuario se calcula el vencimiento con `sumar_meses(date.today(), MESES_DE_MEMBRESIA)` y se guarda directamente `vencimiento_membresia`. Si más adelante se quiere mostrar “miembro desde”, se agrega `fecha_registro` como campo opcional y se actualiza `crear_usuario()` para leerlo con valor por defecto `None`.

#### `datos/prestamos.json`

```json
[
  {
    "id": "P-0001",
    "isbn": "9788437604947",
    "dni": "11111111",
    "fecha_prestamo": "2026-11-10",
    "fecha_limite": "2026-11-25",
    "fecha_devolucion": null,
    "estado": "activo"
  }
]
```

El campo `id` es opcional, pero facilita identificar un préstamo cuando un usuario tiene varios del mismo libro a lo largo del tiempo. Si no se usa, la devolución se busca por `isbn` + `dni` + estado activo. La regla del sistema es que solo puede existir **un préstamo activo por usuario**.

#### `datos/bitacora.txt`

Una línea por movimiento:

```
2026-11-10 10:15 | PRESTAMO | 11111111 | 9788437604947
2026-11-20 16:40 | DEVOLUCION | 11111111 | 9788437604947
```

### 7.5 Reglas de negocio

| Regla | Valor o condición | Dónde se aplica |
| --- | --- | --- |
| Ingreso | Usuario existente, activo y con membresía vigente. | `VentanaAcceso` + `Biblioteca.usuario()`. |
| Registro | DNI único de 8 dígitos, nombre no vacío y tipo `Estudiante` o `Docente`. | `VentanaRegistro` + `Biblioteca.registrar_usuario()`. |
| Membresía nueva | `MESES_DE_MEMBRESIA = 3`; vence exactamente 3 meses después del alta. | `utilidades.sumar_meses()` + `Biblioteca.registrar_usuario()`. |
| Autorregistro | No se puede crear un `Administrador` desde la pantalla de acceso. | `Biblioteca.registrar_usuario()` con `permitir_administrador=False`. |
| Préstamo | Usuario activo, membresía vigente, stock disponible y **sin otro préstamo activo**. | `Biblioteca.prestar()`. |
| Un solo préstamo | `MAXIMO_PRESTAMOS_POR_USUARIO = 1`; si ya tiene uno, se bloquea el segundo. | `Biblioteca.prestamo_activo_de_usuario()`. |
| Stock | No se presta si `disponibles` es 0. | `Biblioteca.prestar()` + `Libro.prestar_ejemplar()`. |
| Último ejemplar | Regla actual: se reserva el último (`disponibles > 1`). | `Libro.se_puede_prestar()`. |
| Devolución | Debe existir un préstamo activo para ese libro y usuario. | `Biblioteca.devolver()`. |
| Nuevo préstamo | Solo se permite después de registrar la devolución. | `Biblioteca.prestar()`. |
| Plazo | `DIAS_DE_PRESTAMO = 15`; si vence, se marca “Vencido”, pero **no genera multa**. | `Prestamo.esta_vencido()`. |
| Multas | **No se usan.** No hay cálculo, cobro ni bloqueo por deuda. | Ninguna parte del sistema. |
| Beneficios | **No se implementan por ahora.** La membresía solo muestra datos y estado. | `membresiaPage`. |
| Baja | Un usuario de baja no puede ingresar ni recibir préstamos. | `Usuario.esta_activo()`. |
| Renovación | Actualiza el vencimiento; no borra el historial. | `Biblioteca.renovar_membresia()`. |
| Administración | Solo `Administrador` ve y usa usuarios, reportes y CRUD de libros. | `Usuario.puede_administrar()`. |
| Persistencia | Toda operación que cambia datos guarda el JSON correspondiente. | `Biblioteca.guardar_*()`. |

**Implementación del préstamo único:**

```python
def prestar(self, isbn, dni):
    usuario = self.usuario(dni)
    if not usuario.esta_activo() or not usuario.tiene_membresia_vigente():
        raise errores.ErrorDePrestamo("El usuario no puede recibir préstamos")
    if self.prestamo_activo_de_usuario(dni) is not None:
        raise errores.ErrorDePrestamo(
            "El usuario ya tiene un libro prestado; debe devolverlo primero"
        )
    libro = self.libro(isbn)
    if not libro.se_puede_prestar():
        raise errores.ErrorDePrestamo("No hay ejemplares disponibles para prestar")
    libro.prestar_ejemplar()
    prestamo = prestamos.crear_prestamo(...)
    self._prestamos.append(prestamo)
    self.guardar_libros()
    self.guardar_prestamos()
    return prestamo
```

La regla del último ejemplar es una decisión de negocio: si la biblioteca quiere reservar una copia para consulta interna, se mantiene `> 1`; si se permite prestar la última copia, se cambia a `> 0`. Debe quedar escrita en el código y en el README.

---

## 8. Matrices y recursividad

### 8.1 Matrices del reporte

Las matrices se construyen en el momento del reporte; no se guardan en JSON para que nunca queden desactualizadas.

| Matriz | Dimensiones | Qué representa |
| --- | --- | --- |
| `mapa_de_estantes` | 5 secciones × 3 estantes | Ejemplares disponibles por sección y estante. |
| `agenda_de_devoluciones` | Usuarios × 3 estados | Préstamos activos, vencidos y devueltos. |
| `historial_por_usuario` | Usuarios × 3 columnas | Préstamos activos, devueltos y total histórico. |
| `prestamos_por_seccion` | 5 secciones × 2 columnas | Préstamos activos y devueltos por sección. |

Las columnas de `agenda_de_devoluciones` pueden ser `["Activo", "Vencido", "Devuelto"]`. Las de `historial_por_usuario`, `["Activos", "Devueltos", "Total"]`. Las de `prestamos_por_seccion`, `["Activos", "Devueltos"]`.

No existe una matriz de penalizaciones porque el equipo decidió no trabajar con multas.

### 8.2 Funciones recursivas

| Función | Entrada | Caso base | Paso recursivo |
| --- | --- | --- | --- |
| `buscar_en_categoria(libros, categoria, indice=0)` | Lista de libros | `indice == len(libros)` devuelve `[]`. | Compara el libro actual y concatena con el resto. |
| `contar_disponibles_en_seccion(libros, seccion, indice=0)` | Lista de libros | `indice == len(libros)` devuelve `0`. | Suma el libro actual y llama al siguiente. |
| `sumar_existencias(libros, indice=0)` | Lista de libros | `indice == len(libros)` devuelve `0`. | Suma `ejemplares()` y sigue. |
| `sumar_matriz(matriz, fila=0, columna=0)` | Matriz | Fin de filas o columnas devuelve `0`. | Suma la celda y avanza a la siguiente columna o fila. |
| `sumar_fila(matriz, fila, columna=0)` | Matriz y fila | `columna == len(fila)` devuelve `0`. | Suma la celda y sigue. |
| `contar_en_matriz(matriz, valor, fila=0, columna=0)` | Matriz | Fin de la matriz devuelve `0`. | Cuenta si la celda coincide y sigue. |

### 8.3 Ejemplo de construcción

```python
def mapa_de_estantes(libros):
    secciones = list(configuracion.SECCIONES)
    mapa = [
        [0 for _ in range(configuracion.CANTIDAD_DE_ESTANTES)]
        for _ in secciones
    ]
    for libro in libros:
        fila = secciones.index(libro.seccion())
        columna = libro.estante() - 1
        mapa[fila][columna] += libro.disponibles()
    return mapa
```

### 8.4 Dónde se muestran

- `reportesPage` muestra las matrices como tablas HTML dentro de `reporteTextEdit`.
- El reporte exportado las incluye en texto o CSV.
- La página de inicio puede usar `resumen()` para las tarjetas; no necesita matrices.

---

## 9. Guía de implementación por funcionalidad

Esta sección explica cómo arrancar cada avance para que todo el equipo trabaje con la misma idea: **primero el núcleo, después la interfaz y al final la prueba manual**. No es código definitivo; es el orden y las conexiones que hay que respetar.

#### Qué falta y por dónde empezar

| Avance pendiente | Empezar por (núcleo) | Después conectar (interfaz) | Guía |
| --- | --- | --- | --- |
| Registro de usuarios | `configuracion.MESES_DE_MEMBRESIA`, `utilidades.sumar_meses()`, `Biblioteca.registrar_usuario()` | `acceso.ui`, `acceso.py`, `registro.ui`, `registro.py` | 9.3 |
| Panel principal | `Biblioteca.resumen()` y `usuario.datos_de_membresia()` | `principal.py`: navegación, tarjetas y membresía | 9.4 |
| Catálogo | `Biblioteca.buscar_avanzado()` | `ui/catalogo.py` incrustado en `catalogoPage` | 9.5 |
| CRUD de libros | `registrar_libro()`, `actualizar_libro()`, `eliminar_libro()` | `libro_form.ui`, `libro_form.py` y botones del catálogo | 9.6 |
| Préstamos | `core/prestamos.py` y `Biblioteca.prestar()` | `prestamo.ui`, `prestamo.py` | 9.7 |
| Devoluciones | `Biblioteca.devolver()` | `devolucion.ui`, `devolucion.py` | 9.8 |
| Gestión de usuarios | `renovar_membresia()`, `dar_de_baja()`, `reactivar()` | botones de `usuariosPage` | 9.9 |
| Reportes | `core/reportes.py` y `Biblioteca.reporte_general()` | `reporteTextEdit` y exportación | 9.10 |
| Persistencia | `configuracion.escribir_archivo()` y `guardar_*()` | se usa desde todas las operaciones | Fases 0 y 3 |
| Estilos e íconos | — | `ui/estilos.qss` y `recursos/` | Fase 7 |

### 9.1 El recorrido de un dato

Toda funcionalidad sigue el mismo camino:

```text
Widget del .ui
    │  (clic, Enter, cambio de fila)
    ▼
Método de la ventana en ui/*.py
    │  (valida el formulario y llama)
    ▼
Método de Biblioteca en core/biblioteca.py
    │  (aplica las reglas y usa las clases)
    ▼
Clase o función de core/libros.py, usuarios.py, prestamos.py, reportes.py
    │  (cambia el estado)
    ▼
configuracion.escribir_archivo()
    │
    ▼
datos/*.json
```

Reglas de oro:

1. La ventana **no** abre JSON, no recorre listas internas y no cambia `disponibles` a mano.
2. Si una ventana necesita un dato, se agrega un método en `Biblioteca` y se llama desde la ventana.
3. Primero se implementa y se prueba el método del núcleo; después se conecta el widget.
4. Toda operación que cambia datos termina guardando el JSON correspondiente.
5. Los errores del núcleo se capturan en la ventana y se muestran con `QMessageBox` o con una etiqueta de ayuda.

#### Mapa de conexiones del sistema

| Pantalla o archivo | Señal o evento | Método de la ventana | Método del núcleo | Archivo que cambia |
| --- | --- | --- | --- | --- |
| `main_interfaz.py` | arranque | `AplicacionBiblioteca.iniciar()` | `Biblioteca()` | — |
| `acceso.py` | `entrarBtn.clicked` | `validar_usuario()` | `usuario()`, `esta_activo()`, `tiene_membresia_vigente()` | — |
| `acceso.py` | `registrarBtn.clicked` | `abrir_registro()` | `registrar_usuario()` | `usuarios.json` |
| `registro.py` | `registrarButton.clicked` | `registrar()` | `registrar_usuario()` | `usuarios.json` |
| `principal.py` | `navegacionListWidget.currentRowChanged` | `_cambiar_pagina(fila)` | — | — |
| `principal.py` | `cerrarSesionButton.clicked` | `cerrar_sesion()` | — | — |
| `principal.py` | abrir Inicio | `_cargar_resumen()` | `resumen()` | — |
| `principal.py` | abrir Mi membresía | `_cargar_membresia()` | `usuario.datos_de_membresia()` | — |
| `catalogo.py` | `buscarButton.clicked` | `buscar()` | `buscar_avanzado()` | — |
| `catalogo.py` | `nuevoLibroButton.clicked` | `_nuevo_libro()` | `registrar_libro()` | `libros.json` |
| `catalogo.py` | `editarLibroButton.clicked` | `_editar_libro()` | `actualizar_libro()` | `libros.json` |
| `catalogo.py` | `eliminarLibroButton.clicked` | `_eliminar_libro()` | `eliminar_libro()` | `libros.json` |
| `prestamo.py` | `prestarButton.clicked` | `prestar()` | `prestar()` | `libros.json` y `prestamos.json` |
| `devolucion.py` | `devolverButton.clicked` | `devolver()` | `devolver()` | `libros.json` y `prestamos.json` |
| `principal.py` | `nuevoUsuarioButton.clicked` | `_nuevo_usuario()` | `registrar_usuario(..., permitir_administrador=True)` | `usuarios.json` |
| `principal.py` | `renovarMembresiaButton.clicked` | `_renovar_membresia()` | `renovar_membresia()` | `usuarios.json` |
| `principal.py` | `darDeBajaButton.clicked` | `_dar_de_baja()` | `dar_de_baja()` | `usuarios.json` |
| `principal.py` | `reactivarButton.clicked` | `_reactivar()` | `reactivar()` | `usuarios.json` |
| `principal.py` | `actualizarReporteButton.clicked` | `_cargar_reporte()` | `reporte_general()` | — |
| `principal.py` | `exportarReporteButton.clicked` | `_exportar_reporte()` | texto del reporte | `datos/reportes/` |

### 9.2 Checklist para arrancar cualquier avance

1. **Escribir el método del núcleo** con su docstring, sus validaciones y el error que lanza.
2. **Probarlo desde consola** antes de tocar la interfaz. Ejemplo:
   ```bash
   python3 -c "from core.biblioteca import Biblioteca; b = Biblioteca(); print(b.resumen())"
   ```
3. **Agregar la persistencia** con `guardar_*()` y verificar que el JSON cambie.
4. **Diseñar el `.ui`**: layout raíz, formulario, etiquetas de ayuda y botones con nombre.
5. **Crear el `.py`**: cargar el `.ui`, conectar señales y llamar al núcleo.
6. **Manejar los errores** esperados con un mensaje claro; no dejar que salga un traceback.
7. **Probar el caso feliz y los casos de error**, marcar la tarea en la fase y actualizar el plan si cambió una decisión.

### 9.3 Registro de usuario desde el acceso

Esta es la funcionalidad nueva que se agrega al primer diálogo. La persona que todavía no tiene cuenta abre `VentanaRegistro`, completa sus datos y el sistema le crea una membresía de **3 meses**.

#### Flujo

```text
VentanaAcceso
  └── registrarBtn.clicked
        └── abrir_registro()
              └── VentanaRegistro.exec_()
                    ├── registrarButton.clicked → registrar()
                    │     └── Biblioteca.registrar_usuario()
                    │           ├── valida DNI único y nombre
                    │           ├── calcula vencimiento con sumar_meses(hoy, 3)
                    │           ├── crea Usuario
                    │           └── guardar_usuarios()
                    └── cancelarButton.clicked → reject()
```

#### Archivos que se tocan

| Archivo | Acción | Qué se hace |
| --- | --- | --- |
| `core/configuracion.py` | Modificar | Agregar `MESES_DE_MEMBRESIA = 3`. |
| `core/utilidades.py` | Modificar | Agregar `sumar_meses(fecha, meses)`. |
| `core/usuarios.py` | Modificar | Agregar `a_diccionario()` y `renovar_hasta()`. |
| `core/biblioteca.py` | Modificar | Agregar `registrar_usuario()` y `guardar_usuarios()`. |
| `ui/acceso.ui` | Modificar | Agregar `registrarBtn`. |
| `ui/acceso.py` | Modificar | Agregar `abrir_registro()` y la conexión del botón. |
| `ui/registro.ui` | Crear | Formulario con DNI, nombre, tipo, aviso y botones. |
| `ui/registro.py` | Crear | `VentanaRegistro(QDialog)` y `registrar()`. |
| `datos/usuarios.json` | Se actualiza solo | Guarda el usuario nuevo. |

#### Por qué `sumar_meses()` y no `timedelta(days=90)`

`timedelta` suma días, no meses. Tres meses pueden tener 89, 90, 91 o 92 días según el mes de inicio. Si se usa `date.today() + timedelta(days=90)`, la fecha de vencimiento queda corrida y no coincide con “el mismo día dentro de tres meses”.

La solución sin dependencias externas es una función que sume meses y ajuste el día al último del mes:

```python
import calendar
from datetime import date


def sumar_meses(fecha, meses):
    """Suma una cantidad de meses a una fecha y ajusta el día al último del mes."""
    meses_totales = fecha.month - 1 + int(meses)
    año = fecha.year + meses_totales // 12
    mes = meses_totales % 12 + 1
    ultimo_dia = calendar.monthrange(año, mes)[1]
    dia = min(fecha.day, ultimo_dia)
    return date(año, mes, dia)
```

Ejemplos:

| Fecha de alta | Suma | Vencimiento |
| --- | --- | --- |
| `2026-11-10` | 3 meses | `2027-02-10` |
| `2026-01-31` | 3 meses | `2026-04-30` |
| `2026-12-15` | 3 meses | `2027-03-15` |

> `dateutil.relativedelta` también resuelve esto, pero agrega una dependencia que el proyecto no necesita. Si el equipo ya la tiene instalada, se puede usar; si no, `sumar_meses()` es suficiente.

#### Núcleo: guardar el usuario

Primero, `Usuario` necesita poder convertirse en diccionario:

```python
def a_diccionario(self):
    """Convierte los datos del usuario en un diccionario para guardarlo en JSON."""
    return {
        "dni": self._dni,
        "nombre": self._nombre,
        "tipo": self._tipo,
        "vencimiento_membresia": str(self._vencimiento_membresia),
        "activo": self._activo,
    }
```

Después, `Biblioteca` registra y guarda:

```python
def registrar_usuario(self, datos, permitir_administrador=False, fecha_de_alta=None):
    """Registra un usuario nuevo y calcula su vencimiento de membresía."""
    dni = utilidades.validar_dni(datos.get("dni"))
    if dni in self._usuarios:
        raise errores.ErrorDeDatos(f"Ya existe un usuario con el DNI {dni}")

    nombre = str(datos.get("nombre", "")).strip()
    tipo = str(datos.get("tipo", "Estudiante")).strip()
    if tipo == "Administrador" and not permitir_administrador:
        raise errores.ErrorDeDatos("No se puede crear un administrador desde el acceso")

    fecha_de_alta = fecha_de_alta or date.today()
    vencimiento = datos.get("vencimiento_membresia")
    if vencimiento is None:
        vencimiento = utilidades.sumar_meses(
            fecha_de_alta, configuracion.MESES_DE_MEMBRESIA
        )

    usuario = usuarios.crear_usuario(
        {
            "dni": dni,
            "nombre": nombre,
            "tipo": tipo,
            "vencimiento_membresia": str(vencimiento),
            "activo": True,
        }
    )
    self._usuarios[usuario.dni()] = usuario
    self.guardar_usuarios()
    return usuario
```

`guardar_usuarios()` se apoya en `a_diccionario()`:

```python
def guardar_usuarios(self):
    """Escribe todos los usuarios en usuarios.json."""
    configuracion.escribir_archivo(
        configuracion.ARCHIVO_USUARIOS,
        [usuario.a_diccionario() for usuario in self._usuarios.values()],
    )
```

#### Interfaz: `VentanaRegistro`

Antes de la clase se definen la ruta del `.ui` y los imports, igual que en `acceso.py`:

```python
from datetime import date
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog

from core import configuracion, errores, utilidades

ruta_ui = Path(__file__).resolve().parent / "registro.ui"
```

```python
class VentanaRegistro(QDialog):
    """Formulario de autorregistro para un usuario nuevo."""

    def __init__(self, biblioteca, parent=None, permitir_administrador=False):
        super().__init__(parent)
        uic.loadUi(str(ruta_ui), self)
        self.biblioteca = biblioteca
        self.permitir_administrador = permitir_administrador
        self.dni_registrado = None

        tipos = ["Estudiante", "Docente"]
        if permitir_administrador:
            tipos.append("Administrador")
        self.tipoComboBox.addItems(tipos)
        self.dniLineEdit.setValidator(QIntValidator(0, 99999999, self))
        self.dniLineEdit.setMaxLength(8)
        self.membresiaLabel.setText(
            "La membresía dura 3 meses desde hoy y vence el "
            f"{utilidades.sumar_meses(date.today(), configuracion.MESES_DE_MEMBRESIA)}."
        )
        self.registrarButton.setDefault(True)
        self.registrarButton.clicked.connect(self.registrar)
        self.cancelarButton.clicked.connect(self.reject)
        self.dniLineEdit.returnPressed.connect(self.registrar)

    def registrar(self):
        """Valida los datos y crea el usuario en la biblioteca."""
        try:
            usuario = self.biblioteca.registrar_usuario(
                {
                    "dni": self.dniLineEdit.text(),
                    "nombre": self.nombreLineEdit.text(),
                    "tipo": self.tipoComboBox.currentText(),
                },
                permitir_administrador=self.permitir_administrador,
            )
        except errores.ErrorBiblioteca as error:
            self.ayudaRegistroLabel.setText(str(error))
            return

        self.dni_registrado = usuario.dni()
        self.accept()
```

#### Interfaz: abrir el registro desde el acceso

```python
def abrir_registro(self):
    """Abre el formulario de registro y deja el DNI listo para ingresar."""
    dialogo = VentanaRegistro(self.biblioteca, self)
    if dialogo.exec_() == QDialog.Accepted:
        self.dniLineEdit.setText(dialogo.dni_registrado)
        self.dniLineEdit.setFocus()
        self._mostrar_mensaje("Registro completado. Ya puedes ingresar.")
```

En el constructor de `VentanaAcceso` se agrega el import y la conexión:

```python
from ui.registro import VentanaRegistro

self.registrarBtn.clicked.connect(self.abrir_registro)
```

#### Reglas y casos de prueba

| Caso | Resultado esperado |
| --- | --- |
| DNI nuevo, nombre válido, tipo Estudiante | Se guarda en `usuarios.json` con vencimiento a 3 meses. |
| DNI repetido | Mensaje “Ya existe un usuario con el DNI …”; no se guarda. |
| DNI con letras o menos de 8 dígitos | El campo no lo permite o muestra error. |
| Nombre vacío | Mensaje de error; no se guarda. |
| Tipo Administrador desde el acceso | Mensaje de error; no se crea. |
| Cancelar | No se guarda nada y se vuelve al acceso. |
| Después de registrar | El DNI queda escrito en el acceso y la persona puede entrar. |

### 9.4 Panel principal: navegación, resumen y membresía

**Archivos:** `ui/principal.py` (casi todo), `ui/principal.ui` (solo si faltan widgets) y `core/biblioteca.py` (si falta algún dato).

**Orden para empezar:**

1. Cargar los textos fijos de la barra lateral: `marca1Label`, `marca2Label`, `bienvenidaLabel`, `tipoLabel`.
2. Conectar `navegacionListWidget.currentRowChanged` con `_cambiar_pagina(fila)`.
3. Ocultar las filas 3 y 4 cuando `usuario.puede_administrar()` sea `False`.
4. Cargar las tarjetas de Inicio con `biblioteca.resumen()`.
5. Cargar `membresiaPage` con `usuario.datos_de_membresia()`.
6. Conectar `cerrarSesionButton` y `closeEvent`.
7. Recién al final incrustar el catálogo (sección 9.5).

**Conexiones:**

| Señal | Método | Qué hace |
| --- | --- | --- |
| `navegacionListWidget.currentRowChanged` | `_cambiar_pagina(fila)` | Cambia el índice de `paginasStackedWidget`. |
| `cerrarSesionButton.clicked` | `cerrar_sesion()` | Emite `sesion_cerrada`. |
| `closeEvent` | `closeEvent(evento)` | Pregunta si se quiere salir o volver al acceso. |

**Código base:**

```python
def _cargar_resumen(self):
    """Muestra los totales de la biblioteca en las tarjetas de inicio."""
    datos = self.biblioteca.resumen()
    self.titulosValorLabel.setText(str(datos["titulos"]))
    self.ejemplaresValorLabel.setText(str(datos["ejemplares"]))
    self.disponiblesValorLabel.setText(str(datos["disponibles"]))
    self.prestadosValorLabel.setText(str(datos["prestados"]))
    self.usuariosValorLabel.setText(str(datos["usuarios"]))

def _cargar_membresia(self):
    """Muestra los datos de la membresía del usuario conectado."""
    datos = self.usuario.datos_de_membresia()
    self.nombreValorLabel.setText(datos["nombre"])
    self.dniValorLabel.setText(datos["dni"])
    self.tipoValorLabel.setText(datos["tipo"])
    self.vencimientoValorLabel.setText(datos["vencimiento_membresia"])
    self.estadoValorLabel.setText(datos["estado"])
```

**Cuidado:** `currentRowChanged` puede dispararse antes de que exista `self.catalogo`. En `_cambiar_pagina()` hay que comprobar `if fila == 1 and hasattr(self, "catalogo")` antes de llamar a `self.catalogo.buscar()`.

### 9.5 Catálogo dentro del panel

**Archivos:** `core/biblioteca.py` (búsqueda avanzada), `core/libros.py` (filtros), `ui/catalogo.py` (nuevo), `ui/catalogo.ui` (ya existe) y `ui/principal.py` (incrustar).

**Orden para empezar:**

1. Implementar `Biblioteca.buscar_avanzado(...)` y probarla desde consola.
2. Crear `ui/catalogo.py` con `VentanaCatalogo(QWidget)`.
3. Cargar `catalogo.ui` y configurar las columnas de `tablaLibros`.
4. Llenar `campoComboBox`, `categoriaComboBox` y `ordenarComboBox`.
5. Conectar búsqueda, limpiar, filtros y selección.
6. Incrustar el widget en `layoutCatalogoContenedor` desde `principal.py`.

**Firma sugerida:**

```python
def buscar_avanzado(
    self,
    texto="",
    campo="Todo",
    categoria="Todas",
    solo_disponibles=False,
    ordenar_por="Título",
    limite=None,
):
    """Filtra el catálogo según el texto, el campo y los filtros de la interfaz."""
```

La función puede vivir en `core/libros.py` y recibir la lista de libros; `Biblioteca` solo la llama y devuelve `datos_del_catalogo(resultado)`.

**Conexiones:**

| Señal | Método | Qué hace |
| --- | --- | --- |
| `buscarButton.clicked` | `buscar()` | Reúne los filtros y llama al núcleo. |
| `buscarLineEdit.returnPressed` | `buscar()` | Busca con Enter. |
| `limpiarButton.clicked` | `limpiar_filtros()` | Restablece los controles. |
| `categoriaComboBox.currentIndexChanged` | `buscar()` | Filtra al cambiar la categoría. |
| `tablaLibros.itemSelectionChanged` | `mostrar_detalle()` | Llena `detalleTextEdit`. |

**Incrustar:**

```python
# ui/principal.py, dentro de __init__
self.catalogo = VentanaCatalogo(self.biblioteca, self)
self.layoutCatalogoContenedor.addWidget(self.catalogo)
```

**Cuidado:** no se debe reemplazar `catalogoPage` ni crear una ventana nueva; `catalogo.ui` es un `QWidget` que se agrega al layout que ya existe.

### 9.6 CRUD de libros

**Archivos:** `core/biblioteca.py`, `core/libros.py`, `ui/libro_form.ui`, `ui/libro_form.py` y `ui/catalogo.py` (botones).

**Orden para empezar:**

1. Implementar `guardar_libros()`, `registrar_libro()`, `actualizar_libro()` y `eliminar_libro()` en el núcleo.
2. Probar cada método desde consola y revisar `libros.json`.
3. Crear `libro_form.ui` y `VentanaLibro`.
4. Agregar los botones `nuevoLibroButton`, `editarLibroButton` y `eliminarLibroButton` al catálogo.
5. Mostrarlos solo si `self.usuario.puede_administrar()`.
6. Después de aceptar el diálogo, volver a llamar a `self.buscar()`.

**Diálogo reutilizable:**

```python
class VentanaLibro(QDialog):
    """Formulario para crear o editar un libro."""

    def __init__(self, biblioteca, libro=None, parent=None):
        super().__init__(parent)
        uic.loadUi(str(ruta_ui), self)
        self.biblioteca = biblioteca
        self.libro = libro
        self.guardarButton.clicked.connect(self.guardar)
        self.cancelarButton.clicked.connect(self.reject)
        if libro is not None:
            self._cargar_datos(libro)
            self.isbnLineEdit.setEnabled(False)
            self.setWindowTitle("Editar libro")
```

**Conexiones del catálogo:**

| Botón | Método | Núcleo |
| --- | --- | --- |
| `nuevoLibroButton` | `_nuevo_libro()` | `registrar_libro(datos)` |
| `editarLibroButton` | `_editar_libro()` | `actualizar_libro(isbn, datos)` |
| `eliminarLibroButton` | `_eliminar_libro()` | `eliminar_libro(isbn)` |

**Reglas:** no se elimina un libro con préstamos activos; no se acepta ISBN repetido al crear; `disponibles` no puede ser mayor que `ejemplares`.

### 9.7 Préstamos

**Archivos:** `core/prestamos.py` (nuevo), `core/biblioteca.py`, `core/libros.py`, `ui/prestamo.ui` y `ui/prestamo.py`.

**Orden para empezar:**

1. Crear `Prestamo` y `crear_prestamo()` en `core/prestamos.py`.
2. Cargar `prestamos.json` en `Biblioteca.cargar_datos()`.
3. Implementar `prestamo_activo_de_usuario()` y `prestamos_activos()`.
4. Implementar `Libro.prestar_ejemplar()`.
5. Implementar `Biblioteca.prestar(isbn, dni)`.
6. Probar desde consola: prestar, intentar prestar otro y revisar ambos JSON.
7. Crear el diálogo `VentanaPrestamo` y conectarlo desde el catálogo o desde un acceso rápido.

**Secuencia interna de `prestar()`:**

1. Buscar el usuario y validar que esté activo y con membresía vigente.
2. Verificar que no tenga otro préstamo activo.
3. Buscar el libro y verificar stock.
4. Descontar un ejemplar.
5. Crear el préstamo con fecha de hoy y fecha límite.
6. Guardar libros y préstamos.
7. Registrar el movimiento en la bitácora.

**Conexiones de la ventana:**

| Señal | Método | Núcleo |
| --- | --- | --- |
| `prestarButton.clicked` | `prestar()` | `Biblioteca.prestar(isbn, dni)` |
| `dniLineEdit.returnPressed` | `buscar_usuario()` | `Biblioteca.usuario(dni)` |
| `isbnLineEdit.returnPressed` | `buscar_libro()` | `Biblioteca.libro(isbn)` |

**Cuidado:** si el usuario ya tiene un préstamo, `prestamoActivoLabel` debe explicarlo y `prestarButton` debe quedar deshabilitado. El núcleo también debe rechazarlo, no solo la interfaz.

### 9.8 Devoluciones

**Archivos:** `core/prestamos.py`, `core/biblioteca.py`, `core/libros.py`, `ui/devolucion.ui` y `ui/devolucion.py`.

**Orden para empezar:**

1. Implementar `Libro.devolver_ejemplar()`.
2. Implementar `Biblioteca.devolver(isbn, dni)`.
3. Buscar el préstamo activo por ISBN + DNI.
4. Marcar el préstamo como devuelto y guardar la fecha.
5. Reponer el stock y guardar libros y préstamos.
6. Registrar la devolución en la bitácora.
7. Crear `VentanaDevolucion` y conectarla.

**Secuencia interna de `devolver()`:**

1. Verificar que exista un préstamo activo para ese libro y usuario.
2. Guardar `fecha_devolucion = date.today()`.
3. Cambiar el estado a `devuelto`.
4. Sumar un ejemplar al stock.
5. Guardar y registrar en la bitácora.

**Reglas:** no hay multa. Si la fecha límite ya pasó, solo se muestra “Vencido” antes de devolver. Después de devolver, el usuario queda libre para pedir otro libro.

### 9.9 Usuarios y membresías (administrador)

**Archivos:** `core/biblioteca.py`, `core/usuarios.py`, `ui/principal.py` y `ui/registro.py` (reutilizado).

**Orden para empezar:**

1. Llenar `tablaUsuarios` con `biblioteca.datos_de_los_usuarios()`.
2. Conectar `buscarUsuarioLineEdit` y `buscarUsuarioButton` a un filtro local.
3. Conectar `nuevoUsuarioButton` para abrir `VentanaRegistro(self.biblioteca, self, permitir_administrador=True)`.
4. Implementar `renovar_membresia()`, `dar_de_baja()` y `reactivar()`.
5. Después de cada operación, recargar la tabla.

**Renovación de membresía:**

```python
def renovar_membresia(self, dni, meses=None):
    """Extiende la membresía desde hoy o desde el vencimiento actual, lo que sea mayor."""
    usuario = self.usuario(dni)
    meses = meses or configuracion.MESES_DE_MEMBRESIA
    desde = max(date.today(), usuario.vencimiento_membresia())
    nueva_fecha = utilidades.sumar_meses(desde, meses)
    usuario.renovar_hasta(nueva_fecha)
    self.guardar_usuarios()
    return nueva_fecha
```

**Reglas:** el administrador no puede darse de baja a sí mismo; un usuario de baja no puede ingresar; renovar no borra el historial de préstamos.

### 9.10 Reportes, matrices y recursividad

**Archivos:** `core/reportes.py` (nuevo), `core/biblioteca.py` y `ui/principal.py`.

**Orden para empezar:**

1. Implementar las funciones de matrices y recursivas en `core/reportes.py`.
2. Probarlas con los datos actuales y comprobar que los totales coincidan con `resumen()`.
3. Implementar `Biblioteca.reporte_general()`.
4. Mostrar el resultado en `reporteTextEdit` como HTML.
5. Conectar `actualizarReporteButton` y `exportarReporteButton`.
6. Exportar con `QFileDialog` y `open(..., "w", encoding="utf-8")`.

**Conexiones:**

| Señal | Método | Núcleo |
| --- | --- | --- |
| `actualizarReporteButton.clicked` | `_cargar_reporte()` | `Biblioteca.reporte_general()` |
| `exportarReporteButton.clicked` | `_exportar_reporte()` | Texto ya generado |

**Cuidado:** el reporte se calcula al abrir la página; no se guarda en JSON para que no quede desactualizado.

---

## 10. Plan de trabajo por fases

### Fase 0 — Estabilizar la base

**Objetivo:** que las dos entradas arranquen y que el núcleo no falle con datos incompletos.

- [ ] Agregar `core/__init__.py` y `ui/__init__.py`.
- [ ] Unificar imports relativos en `core/`.
- [ ] Envolver la llamada de `main.py` en `if __name__ == "__main__":`.
- [ ] Agregar valores por defecto a `crear_libro()`.
- [ ] Capturar errores de JSON en `leer_archivo()`.
- [ ] Agregar `escribir_archivo()` en `configuracion.py`.
- [ ] Revisar que `python3 main.py` y `python3 main_interfaz.py` arranquen sin traceback.

**Hecho cuando:** las dos entradas funcionan y un JSON inválido muestra un error controlado.

### Fase 1 — Acceso, registro y panel principal

**Objetivo:** que el acceso permita entrar o registrarse y que `principal.ui` sea un panel real y navegable.

- [ ] Agregar `MESES_DE_MEMBRESIA = 3` en `configuracion.py`.
- [ ] Implementar `utilidades.sumar_meses()` y probarla con los ejemplos de la sección 9.3.
- [ ] Agregar `Usuario.a_diccionario()` y `Biblioteca.guardar_usuarios()`.
- [ ] Implementar `Biblioteca.registrar_usuario()` con DNI único y vencimiento automático.
- [ ] Crear `ui/registro.ui` y `ui/registro.py` con los nombres de la sección 6.5.
- [ ] Agregar `registrarBtn` en `acceso.ui` y `abrir_registro()` en `acceso.py`.
- [ ] Implementar `_configurar_marca()` con `configuracion.NOMBRE_BIBLIOTECA` y `configuracion.LEMA`.
- [ ] Implementar `_configurar_usuario()` con nombre, tipo y estado.
- [ ] Implementar `_configurar_navegacion()` y `_cambiar_pagina()`.
- [ ] Ocultar las filas 3 y 4 a los usuarios que no administran.
- [ ] Cargar las cinco tarjetas de resumen con `biblioteca.resumen()`.
- [ ] Cargar la página de membresía con `usuario.datos_de_membresia()`.
- [ ] Implementar `closeEvent` y el cierre de sesión con confirmación.
- [ ] Agregar botones de acceso rápido en `layoutAccesosRapidos` (catálogo, préstamo, devolución y membresía).
- [ ] Corregir el controlador para ocultar o cerrar el panel al volver al acceso.

**Hecho cuando:** una persona nueva se registra con membresía de 3 meses, puede ingresar, el estudiante y el administrador ven opciones distintas, las páginas cambian y el cierre de sesión vuelve al acceso sin dejar ventanas ocultas.

### Fase 2 — Integrar el catálogo

**Objetivo:** que `catalogo.ui` funcione dentro de `catalogoPage`.

- [ ] Crear `ui/catalogo.py` con `VentanaCatalogo(QWidget)`.
- [ ] Cargar `catalogo.ui` con `uic.loadUi()`.
- [ ] Configurar la tabla con las seis columnas actuales.
- [ ] Llenar los combos con categorías, campos y órdenes.
- [ ] Conectar búsqueda, limpiar, filtros y selección.
- [ ] Incrustar la ventana en `layoutCatalogoContenedor`.
- [ ] Implementar `buscar_avanzado()` en `Biblioteca` o reutilizar `buscar()` con filtros.
- [ ] Mostrar la ficha del libro en `detalleTextEdit`.

**Hecho cuando:** se ven los 22 libros, la búsqueda y los filtros funcionan y la ficha cambia al seleccionar una fila.

### Fase 3 — Persistencia y gestión de libros

**Objetivo:** que los cambios de libros se guarden y se puedan recuperar.

- [ ] Implementar `guardar_libros()` y `guardar_datos()`.
- [ ] Implementar `registrar_libro()`, `actualizar_libro()` y `eliminar_libro()`.
- [ ] Crear `ui/libro_form.ui` y `ui/libro_form.py`.
- [ ] Agregar botones de “Nuevo”, “Editar” y “Eliminar” en el catálogo, visibles solo para administradores.
- [ ] Validar ISBN duplicado, campos vacíos, sección, estante y ejemplares.
- [ ] Guardar después de cada operación.

**Hecho cuando:** un libro creado desde la interfaz sigue existiendo después de reiniciar y un libro con préstamos activos no se puede eliminar.

### Fase 4 — Préstamos y devoluciones

**Objetivo:** completar el ciclo de circulación de los libros.

- [ ] Crear `core/prestamos.py` con la clase `Prestamo` y sus funciones.
- [ ] Implementar `Biblioteca.prestar()` y `Biblioteca.devolver()`.
- [ ] Implementar `prestamo_activo_de_usuario()`, `prestamos_activos()` y `prestamos_de_usuario()`.
- [ ] Cargar y guardar `prestamos.json`.
- [ ] Crear `ui/prestamo.ui`, `ui/prestamo.py`, `ui/devolucion.ui` y `ui/devolucion.py`.
- [ ] Descontar y reponer `disponibles` correctamente.
- [ ] Bloquear un segundo préstamo mientras el usuario tenga uno activo.
- [ ] Registrar cada movimiento en `bitacora.txt`.
- [ ] Impedir préstamos a usuarios de baja o con membresía vencida.
- [ ] Marcar como “Vencido” si pasa la fecha límite, sin calcular multa.

**Hecho cuando:** prestar baja el stock, devolver lo sube, el usuario no puede pedir otro hasta devolver y el historial queda guardado.

### Fase 5 — Usuarios y membresías

**Objetivo:** que el administrador pueda gestionar cuentas y vencimientos.

- [ ] Reutilizar `registrar_usuario()` y `VentanaRegistro` con `permitir_administrador=True`.
- [ ] Implementar `actualizar_usuario()`, `dar_de_baja()`, `reactivar()` y `renovar_membresia()`.
- [ ] Agregar los botones `nuevoUsuarioButton`, `renovarMembresiaButton`, `darDeBajaButton` y `reactivarButton` en `usuariosPage`.
- [ ] Validar DNI, nombre, tipo y fecha.
- [ ] Renovar con `sumar_meses(max(date.today(), vencimiento_actual), MESES_DE_MEMBRESIA)`.
- [ ] Actualizar la tabla después de cada operación.
- [ ] Impedir el ingreso de usuarios de baja o vencidos.
- [ ] Impedir que el administrador se dé de baja a sí mismo.
- [ ] Guardar `usuarios.json` después de cada cambio.

**Hecho cuando:** el administrador crea, renueva, da de baja y reactiva usuarios, y los cambios se reflejan al reiniciar.

### Fase 6 — Reportes, matrices y recursividad

**Objetivo:** cumplir la parte de reportes y demostrar matrices y recursividad con nombres del dominio.

- [ ] Crear `core/reportes.py`.
- [ ] Implementar `mapa_de_estantes`, `agenda_de_devoluciones`, `historial_por_usuario` y `prestamos_por_seccion`.
- [ ] Implementar las funciones recursivas de la sección 8.
- [ ] Implementar `Biblioteca.reporte_general()`.
- [ ] Mostrar las matrices en `reporteTextEdit`.
- [ ] Implementar la exportación del reporte.
- [ ] Verificar que los totales coincidan con `resumen()`.

**Hecho cuando:** el reporte muestra las cuatro matrices, los totales son correctos y la exportación genera un archivo legible.

### Fase 7 — Presentación y limpieza

**Objetivo:** dejar el proyecto listo para demostrar y mantener.

- [ ] Crear `ui/estilos.qss` solo si se va a usar; mientras tanto, mantener la interfaz básica.
- [ ] Agregar `recursos/imagenes/` y `recursos/iconos/` si se usan imágenes.
- [ ] Actualizar `README.md` con la estructura, las entradas y las credenciales de prueba.
- [ ] Decidir si se conserva `main.py` o si la entrada única es `main_interfaz.py`.
- [ ] Si se retira la consola, eliminar `core/menu.py`, `main.py` y `utilidades.pausa()`.
- [ ] Revisar imports sin usar, nombres con tildes y textos duplicados.
- [ ] Hacer la prueba manual completa de la sección 11.

**Hecho cuando:** la interfaz se puede usar de principio a fin, el README coincide con el código y no quedan archivos ni funciones sin uso.

---

## 11. Pruebas manuales

### 11.1 Acceso y registro

| Caso | DNI | Resultado esperado |
| --- | --- | --- |
| Estudiante activo | `11111111` | Abre el panel sin opciones de administración. |
| Docente activo | `22222222` | Abre el panel sin opciones de administración. |
| Administrador | `33333333` | Abre el panel con Usuarios y Reportes. |
| Usuario de baja | `70778899` | Mensaje de cuenta de baja; no entra. |
| Membresía vencida | `76789012` | Mensaje de membresía vencida; no entra. |
| DNI inexistente | `99999999` | Mensaje de usuario no encontrado. |
| DNI vacío | — | Mensaje para escribir el DNI. |
| DNI con letras | `abc` | El campo no permite letras o muestra error. |
| Registro con DNI nuevo | `88888888` | Se crea el usuario con vencimiento a 3 meses y queda en `usuarios.json`. |
| Registro con DNI repetido | `11111111` | Mensaje de DNI ya registrado; no se duplica. |
| Registro con nombre vacío | `88888888` | Mensaje de error; no se guarda. |
| Registro como administrador | `88888888` | No se permite desde el acceso. |
| Después de registrarse | — | El DNI queda escrito en el acceso y la persona puede entrar. |

### 11.2 Panel principal

| Caso | Resultado esperado |
| --- | --- |
| Estudiante | No ve Usuarios ni Reportes. |
| Administrador | Ve Usuarios y Reportes. |
| Cambiar de página | El `StackedWidget` muestra la página correcta. |
| Inicio | Las cinco tarjetas muestran los datos reales. |
| Mi membresía | Muestra nombre, DNI, tipo, vencimiento y estado del usuario conectado. |
| Cerrar sesión | Vuelve al acceso y limpia el DNI. |
| Cerrar con la X | Pregunta si se desea salir o vuelve al acceso, pero no deja la app invisible. |

### 11.3 Catálogo

| Caso | Resultado esperado |
| --- | --- |
| Abrir catálogo | 22 libros. |
| Buscar “arte” | 4 resultados de la categoría Arte. |
| Buscar “tolkien” | 1 resultado. |
| Buscar texto inexistente | 0 resultados y mensaje claro. |
| Limpiar filtros | Vuelve a los 22 libros. |
| Seleccionar fila | La ficha muestra ISBN, autor, ubicación, ejemplares y estado. |
| Solo disponibles | Solo libros prestables según la regla del último ejemplar. |

### 11.4 Préstamos y devoluciones

| Caso | Resultado esperado |
| --- | --- |
| Prestar un libro disponible | `disponibles` baja en 1 y se crea el préstamo. |
| Prestar sin stock | Mensaje de error; no se modifica el stock. |
| Prestar con membresía vencida | Mensaje de error; no se presta. |
| Prestar a usuario de baja | Mensaje de error; no se presta. |
| Prestar con un libro ya activo | Mensaje de error; no se presta el segundo. |
| Devolver el libro activo | `disponibles` sube en 1, el préstamo queda devuelto y el usuario puede pedir otro. |
| Devolver después de la fecha límite | Se marca “Vencido”, no se calcula multa y el usuario queda libre al devolver. |
| Devolver un libro no prestado | Mensaje de error; no se modifica el stock. |

### 11.5 Usuarios y reportes

| Caso | Resultado esperado |
| --- | --- |
| Buscar usuario por DNI | Filtra la tabla. |
| Crear usuario desde administración | Aparece en la tabla y en `usuarios.json`. |
| Crear usuario con DNI repetido | Mensaje de error; no se duplica. |
| Renovar membresía | La fecha se extiende 3 meses desde hoy o desde el vencimiento actual. |
| Dar de baja | El usuario ya no puede ingresar. |
| Reactivar | El usuario vuelve a poder ingresar. |
| Administrador intenta darse de baja | El sistema lo impide. |
| Generar reporte | Se muestran las matrices y los totales. |
| Exportar reporte | Se crea un archivo con el contenido. |

### 11.6 Comandos de verificación

Desde `proyecto_parcial/`:

```bash
# Consola
python3 main.py

# Interfaz gráfica
python3 main_interfaz.py

# Verificar que los módulos se importan sin abrir ventanas
QT_QPA_PLATFORM=offscreen python3 -c "import main_interfaz; print('import ok')"

# Revisar errores de sintaxis
python3 -m compileall -q core ui main.py main_interfaz.py
```

---

## 12. Convenciones y definición de terminado

### 12.1 Código

- Nombres de clases en `PascalCase` y empiezan con `Ventana` si son ventanas.
- Nombres de archivos `.ui` y `.py` en `snake_case`.
- Atributos privados con `_` y métodos públicos con nombres claros.
- Docstrings en clases y métodos, con el mismo estilo del núcleo actual.
- Comentarios solo cuando explican una decisión, no para repetir lo que el código ya dice.
- Sin lógica de negocio en los `.py` de las ventanas: la ventana pide, el núcleo resuelve.
- Sin JSON abierto desde la interfaz.
- Sin textos de marca duplicados: usar `configuracion.py`.
- Sin imports sin usar.
- Sin nombres como `aux`, `dato`, `x`, `temporal` para conceptos del dominio.

### 12.2 Interfaz

- Todo widget que se use desde Python tiene un `objectName` estable.
- Los layouts están aplicados; no se usan posiciones absolutas.
- La ventana se prueba al menos en 1024×768 y 1366×768.
- Los errores se muestran con mensajes claros, no con tracebacks.
- Los botones de administración solo aparecen cuando el usuario puede administrar.
- Las tablas no se pueden editar directamente si los datos se cambian con formularios.

### 12.3 Definición de terminado por funcionalidad

Una funcionalidad está terminada cuando:

1. Se puede usar desde la interfaz.
2. Usa el núcleo y no duplica lógica.
3. Guarda los cambios en el archivo correspondiente.
4. Maneja los errores esperados.
5. Tiene una prueba manual documentada.
6. No rompe la consola ni las demás páginas.

---

## 13. Decisiones del equipo y pendientes

### 13.1 Decisiones ya tomadas

| Decisión | Regla acordada |
| --- | --- |
| Multas | No se usan. No hay cálculo, cobro ni bloqueo por deuda. |
| Préstamos por usuario | Solo uno activo. Hasta que no se devuelva, no se puede pedir otro. |
| Beneficios de membresía | No se implementan por ahora. La página de membresía solo muestra datos y estado. |
| Devolución | Repone el stock y libera al usuario para un nuevo préstamo. |
| Plazo | Se puede mantener una fecha límite de 15 días solo para marcar “Vencido”; no genera multa. |
| Registro desde el acceso | Cualquier persona puede crear su cuenta con DNI, nombre y tipo `Estudiante` o `Docente`. No puede crear administradores. |
| Duración de membresía | 3 meses exactos desde la fecha de alta, calculados con `sumar_meses()` y `MESES_DE_MEMBRESIA = 3`. |
| Renovación | Se suman 3 meses desde la fecha de hoy o desde el vencimiento actual, el que sea mayor. |
| Autoingreso después del registro | No. Se cierra el diálogo, se deja el DNI escrito y la persona ingresa manualmente. |

### 13.2 Decisiones pendientes

| Decisión | Opciones | Recomendación |
| --- | --- | --- |
| ¿Se conserva la consola? | Mantener `main.py` o dejar solo `main_interfaz.py`. | Mantenerla hasta que la GUI cubra todo; al final, si no se usa, retirarla. |
| ¿Se presta el último ejemplar? | `disponibles > 0` o `disponibles > 1`. | Decidirlo antes de implementar préstamos y escribirlo en el README. La regla actual reserva el último. |
| ¿Dónde se guardan los reportes? | `datos/reportes/` o la carpeta que elija el usuario. | `datos/reportes/` por defecto, con opción de elegir otra ruta. |
| ¿Se usa `QCalendarWidget`? | Solo `QLineEdit` con fecha o un calendario. | Usar calendario solo si se permite una fecha personalizada; si la renovación siempre suma 3 meses, no hace falta. |
| ¿Se agregan estilos ahora? | QSS desde el inicio o al final. | Al final, para no mezclar presentación con conexión. |
| ¿Se usa `id` en los préstamos? | Sí o buscar por ISBN + DNI. | Usar `id` si se quiere conservar un historial claro; con un solo préstamo activo, buscar por ISBN + DNI también es suficiente. |
| ¿Qué pasa con `datos/prestamos.json` vacío? | Dejarlo vacío o inicializarlo con `[]`. | `leer_archivo()` ya devuelve `[]` si está vacío; al guardar por primera vez quedará con contenido. |
| ¿Se retira `menu.py`? | Conservarlo o eliminarlo. | Conservarlo mientras `main.py` sea una entrada útil. |
| ¿Se guarda `fecha_registro`? | Guardar solo el vencimiento o guardar también la fecha de alta. | Guardar solo `vencimiento_membresia`; si se quiere mostrar “miembro desde”, agregar `fecha_registro` como campo opcional. |
| ¿Se valida que un `Docente` sea realmente docente? | Permitir el autorregistro o pedir una clave administrativa. | Para la demo, permitir `Estudiante` y `Docente`; dejar la validación formal fuera del alcance. |
| ¿Cuántos meses dura la membresía? | 1, 3 o 6 meses. | 3 meses, como se acordó. El valor queda en `MESES_DE_MEMBRESIA` para cambiarlo en un solo lugar. |

---

## 14. Orden recomendado para empezar

Si se retoma el trabajo en una sola sesión, el orden más corto para ver resultados es:

1. **Fase 0:** corregir imports, defaults y escritura de archivos.
2. **Fase 1:** registro desde el acceso, navegación, resumen y membresía del panel.
3. **Fase 2:** crear `ui/catalogo.py` e incrustarlo en `catalogoPage`.
4. **Fase 4:** implementar préstamos y devoluciones, porque son la funcionalidad que más impacto tiene en el sistema.
5. **Fase 3 y 5:** CRUD de libros y gestión de usuarios.
6. **Fase 6:** reportes, matrices y recursividad.
7. **Fase 7:** estilos, íconos y limpieza final.

Con las fases 0, 1 y 2 el sistema ya permite registrarse, entrar, navegar y consultar el catálogo. Con la fase 4 empieza a comportarse como una biblioteca real. Las fases 5 y 6 completan la parte administrativa y los reportes.
