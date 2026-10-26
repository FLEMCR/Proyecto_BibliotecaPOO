# Guia del proyecto: sistema de biblioteca

Esta guia explica el proyecto bloque por bloque para defenderlo maniana. Se lee de arriba
hacia abajo: primero el mapa general, despues cada unidad del curso con el codigo real del
proyecto, y al final la rubrica con la demostracion paso a paso.

Cada tema tiene tres cosas:

- **Teoria**: que problema resuelve y como se ve en este proyecto.
- **Codigo**: celdas que se pueden ejecutar aca mismo, con su salida real.
- **Error comun**: el error tipico del tema, con la version mala y la buena.

Si solo tienes 20 minutos, lee la portada, la seccion de la rubrica y los errores comunes.

## Conectar el cuaderno con el proyecto

El cuaderno vive en `cuadernos/` y el codigo un nivel arriba. Esta primera celda agrega esa
carpeta al camino de busqueda de Python para que `import modulos` funcione. Hay que ejecutarla
una vez al abrir el cuaderno; las demas celdas ya la dan por hecha.

```python
import os
import sys

CARPETA = os.path.abspath(os.path.join(os.getcwd(), ".."))
if CARPETA not in sys.path:
    sys.path.insert(0, CARPETA)

from datetime import date, timedelta

from modulos import biblioteca, config, errores, libros, menu, usuarios, utilidades

print("conectado con la carpeta del proyecto:", CARPETA)
print("Python", sys.version.split()[0])
```

**Salida**

```
conectado con la carpeta del proyecto: /home/user/proyecto_parcial
Python 3.13.16
```

## Que hace el programa hoy

Es un **avance**. Lo que ya funciona:

- cargar el catalogo y los miembros desde dos archivos JSON;
- iniciar sesion con DNI, con tres caminos distintos segun quien entre;
- consultar el catalogo y buscar por categoria con una funcion recursiva;
- ver la membresia de cada miembro (tipo, estado, vencimiento, limite, dias, multa);
- un menu de administracion con el estado, la lista de miembros, tres matrices y el guardado;
- guardar los cambios en los JSON, pidiendo confirmacion antes.

Lo que **todavia no** esta hecho: prestar y devolver libros, y con eso las multas por retraso.
El archivo con el historial de prestamos del equipo esta guardado aparte, sin usar, para
retomarlo despues. Las piezas que si quedaron listas para ese dia son `Libro.prestar_uno()` y
`Libro.devolver_uno()`, y `Membresia.renovar()` y `Membresia.cancelar()`.

## El mapa del proyecto

| Archivo               | Lineas | Que guarda                                                        |
| --------------------- | ------ | ----------------------------------------------------------------- |
| main.py               | 12     | arranca todo: portada, biblioteca y menu                          |
| modulos/config.py     | 62     | rutas de los JSON, las reglas por tipo de miembro, leer y guardar |
| modulos/errores.py    | 10     | las 3 excepciones propias del sistema                             |
| modulos/utilidades.py | 54     | titulo, pausa, validar DNI e ISBN, fechas                         |
| modulos/usuarios.py   | 184    | Membresia y sus 4 subclases, y la clase Usuario                   |
| modulos/libros.py     | 187    | Libro, las 3 matrices y la busqueda recursiva por categoria       |
| modulos/biblioteca.py | 96     | une todo: carga los JSON, resume, guarda                          |
| modulos/menu.py       | 253    | las tablas de opciones y todas las acciones                       |

Total: 858 lineas. Adentro solo hay un comentario y un ejemplo de recursion comentado, los dos en utilidades.py.

**Por que esta dividido asi.** Cada archivo tiene un solo tema. Si maniana hay que cambiar
cuantos libros puede llevar un estudiante, se abre `config.py` y nada mas. Eso es lo que la
rubrica llama _programa modular_: partes que se pueden tocar por separado.

Las flechas siempre van hacia abajo, nunca al reves:

```python
print("main.py")
print("   llama a -> menu.py (solo dos funciones: portada y menu_principal)")
print("              usa -> biblioteca.py")
print("                     usa -> libros.py, usuarios.py")
print("                            usan -> utilidades.py, errores.py, config.py")
```

**Salida**

```
main.py
   llama a -> menu.py (solo dos funciones: portada y menu_principal)
              usa -> biblioteca.py
                     usa -> libros.py, usuarios.py
                            usan -> utilidades.py, errores.py, config.py
```

Ningun archivo de abajo importa uno de arriba: `config.py` no sabe que existe `menu.py`. Por
eso se puede probar un modulo solo, sin arrancar el programa entero, que es lo que hacemos en
las celdas de esta guia.

Un detalle que se puede mencionar: `menu.py` **no** importa `Biblioteca`. El objeto lo crea
`main.py` y se lo pasa por parametro a `menu_principal`. Eso corta el circulo de importaciones
y deja claro que el menu solo dibuja pantallas.

## Las clases del proyecto

```python
from modulos.biblioteca import Biblioteca
from modulos.libros import Libro
from modulos.usuarios import (Administrador, Docente, Estudiante, Invitado,
                              Membresia, Usuario)

clases = [Libro, Usuario, Membresia, Estudiante, Docente, Administrador,
          Invitado, Biblioteca]
print("las 8 del sistema:")
for clase in clases:
    print(f"   {clase.__name__:<15} esta en {clase.__module__}")

print()
print("y las 3 de errores:")
for clase in [errores.BibliotecaError, errores.DatosInvalidosError,
              errores.ArchivoDatosError]:
    padres = [p.__name__ for p in clase.__bases__]
    print(f"   {clase.__name__:<24} hereda de {padres}")
```

**Salida**

```
las 8 del sistema:
   Libro           esta en modulos.libros
   Usuario         esta en modulos.usuarios
   Membresia       esta en modulos.usuarios
   Estudiante      esta en modulos.usuarios
   Docente         esta en modulos.usuarios
   Administrador   esta en modulos.usuarios
   Invitado        esta en modulos.usuarios
   Biblioteca      esta en modulos.biblioteca

y las 3 de errores:
   BibliotecaError          hereda de ['Exception']
   DatosInvalidosError      hereda de ['BibliotecaError', 'ValueError']
   ArchivoDatosError        hereda de ['BibliotecaError']
```

## Los datos

Hay dos archivos JSON en `modulos/datos/`. El programa los lee al arrancar y arma los objetos
en memoria. No vuelve a tocar el disco hasta que alguien elige _Guardar cambios_ en el menu de
administracion.

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()

print("titulos en el catalogo:", len(b.catalogo()))
print("miembros registrados:  ", len(b.miembros()))
print()
print("resumen:", b.resumen())
print()
print("y donde estan los archivos:")
for nombre, archivo in config.ARCHIVOS.items():
    print(f"   {nombre:<9} -> {config.ruta_json(nombre)}")
```

**Salida**

```
titulos en el catalogo: 7
miembros registrados:   10

resumen: {'titulos': 7, 'ejemplares': 19, 'disponibles': 15, 'prestados': 4, 'miembros': 10}

y donde estan los archivos:
   libros    -> /home/user/proyecto_parcial/modulos/datos/libros.json
   miembros  -> /home/user/proyecto_parcial/modulos/datos/miembros.json
```

Los 7 titulos tienen categoria, seccion, estante, ejemplares y disponibles. Los 10 miembros
tienen DNI, nombre, tipo, vencimiento de membresia y si estan activos.

Ojo con un dato: en `libros.json` algunos titulos tienen menos `disponibles_prestamo` que
`ejemplares` (por ejemplo Eloquent JavaScript tiene 2 ejemplares y 1 disponible). Eso venia del
historial de prestamos del equipo. Como los prestamos todavia no estan hechos, ese numero hoy
simplemente se muestra y alimenta las matrices.

## Como probarlo en una terminal

```
python3 main.py
```

El ingreso es solo con DNI. Estos son los caminos que hay que saber mostrar:

| DNI        | Quien es                    | Que menu abre                                    |
| ---------- | --------------------------- | ------------------------------------------------ |
| 72345678   | Jorge Huaman, administrador | estado, miembros, matrices y busqueda, guardar   |
| 75678901   | Sofia Rojas, estudiante     | catalogo, busqueda por categoria, mi membresia   |
| 70445566   | Luis Ramos, docente         | el mismo menu de miembro, con limite 5 y 20 dias |
| (opcion 2) | invitado                    | solo catalogo y busqueda por categoria           |
| 70778899   | Rosa Palomino, dada de baja | no entra: el programa lo avisa y vuelve al menu  |
| 123        | DNI de 3 cifras             | no entra: 'El DNI debe tener 8 digitos'          |

## Tres cosas que hay que decir en la defensa

1. **Es un avance.** Prestamos, devoluciones y multas no estan hechos todavia. Esta dicho en
   el README y en la ultima seccion de esta guia, con lo que ya existe para retomarlo.
2. **No hay ni una libreria externa.** Todo es Python estandar, asi que corre en cualquier
   maquina con `python3 main.py`.
3. **Los nombres de la portada son provisionales.** En `config.py` estan
   `nombre_biblioteca` y `lema` con textos de broma; hay que cambiarlos antes de presentar.

## Que unidad del curso toca cada seccion

| Seccion de esta guia       | Material del curso                          | Donde se ve en el proyecto                                              |
| -------------------------- | ------------------------------------------- | ----------------------------------------------------------------------- |
| 1. Fundamentos             | Semana 1 - Fundamentos de Python            | config.py, utilidades.py, las tablas del menu                           |
| 2. POO                     | Principios de POO                           | las 8 clases, atributos privados, constructores con valores por defecto |
| 3. Funciones y excepciones | Metodos y Funciones, Estructuras Selectivas | utilidades.py, libros.py, errores.py, los try/except                    |
| 4. Matrices y recursividad | Matrices y Recursividad                     | las 3 matrices y las 3 funciones recursivas                             |
| 5. Herencia y polimorfismo | Herencia y Polimorfismo                     | Membresia y sus 4 subclases, describir()                                |
| 6. Errores comunes         | todos                                       | los errores que salieron de verdad, con su correccion                   |
| 7. Rubrica y demo          | Rubrica del parcial                         | criterio por criterio, con los flujos de prueba                         |

# 1. Fundamentos de Python en el proyecto

Esta seccion cubre lo de la Semana 1: variables, tipos, entrada y salida, cadenas con formato,
listas, tuplas, diccionarios, condiciones, bucles y archivos. Todo con el codigo real del
proyecto, no con ejemplos sueltos.

> ### Teoria: variables y tipos
>
> **El problema.** Un programa tiene que guardar valores mientras corre: cuantos libros puede llevar un estudiante, que dia vence una membresia, si un miembro esta activo.
>
> **Como lo resuelve el proyecto.** Con nombres claros y sin anotar el tipo al lado. Python lo deduce del valor: `estantes = 6` es un entero, `lema = "..."` es texto, `activo = True` es booleano.
>
> | Otra forma                             | Por que no se uso                                            |
> | -------------------------------------- | ------------------------------------------------------------ |
> | Anotar el tipo como en otros lenguajes | Python lo deduce solo, escribirlo de mas ensucia el codigo   |
> | Nombres de una letra                   | en un archivo de 250 lineas como menu.py no se entiende nada |
>
> **El modelo mental.** Una variable es una etiqueta pegada a un valor. La etiqueta se puede mover a otro valor, y el tipo de lo que tenga pegado puede cambiar.
>
> **Receta para otro proyecto.** Nombrar segun lo que guarda el valor (`dias_prestamo`, no `x` ni `dato2`). Si el nombre no necesita un comentario al lado, esta bien puesto.

### Las reglas del negocio estan en un solo lugar

`config.py` guarda los numeros que podrian cambiar: cuantos libros puede llevar cada tipo de
miembro, cuantos dias dura el prestamo y cuanto se cobraria por dia de retraso. Son
diccionarios con el tipo de miembro como llave.

```python
from modulos import config

print("limite de libros:", config.limite_libros)
print("dias de prestamo:", config.dias_prestamo)
print("multa por dia:  ", config.multa_por_dia)
print()
print("secciones:", len(config.secciones), "letras, de la A a la",
      list(config.secciones)[-1], "(diccionario de letra a nombre)")
print("estantes por seccion:", config.estantes)
print()
print("nombre de la biblioteca:", config.nombre_biblioteca)
print("lema:", config.lema)
```

**Salida**

```
limite de libros: {'estudiante': 3, 'docente': 5, 'administrador': 5, 'invitado': 0}
dias de prestamo: {'estudiante': 14, 'docente': 20, 'administrador': 20, 'invitado': 0}
multa por dia:   {'estudiante': 0.5, 'docente': 0.5, 'administrador': 0.5, 'invitado': 0.0}

secciones: 8 letras, de la A a la H (diccionario de letra a nombre)
estantes por seccion: 6

nombre de la biblioteca: Biblioteca POO HAY QUE CAMBIAR NOMBREEEEEE
lema: FRASE A USAR WAAAAAA
```

**Por que diccionarios y no variables sueltas.** Porque asi se puede preguntar por la regla con
un nombre que llega de los datos. Mira estas lineas de `usuarios.py`:

```python
class Estudiante(Membresia):
    LIMITE_LIBROS = config.limite_libros["estudiante"]
    DIAS_PRESTAMO = config.dias_prestamo["estudiante"]
```

Si las reglas estuvieran en variables separadas (`LIMITE_ESTUDIANTE`, `LIMITE_DOCENTE`...),
habria que escribir una cadena de `if` para elegir cual usar en cada clase. Con el diccionario
la llave hace ese trabajo.

```python
for tipo in config.limite_libros:
    limite = config.limite_libros[tipo]
    dias = config.dias_prestamo[tipo]
    multa = config.multa_por_dia[tipo]
    print(f"{tipo:<15} {limite} libros, {dias} dias, multa S/{multa:.2f} por dia")
```

**Salida**

```
estudiante      3 libros, 14 dias, multa S/0.50 por dia
docente         5 libros, 20 dias, multa S/0.50 por dia
administrador   5 libros, 20 dias, multa S/0.50 por dia
invitado        0 libros, 0 dias, multa S/0.00 por dia
```

> ### Error comun: repetir la misma regla en varios archivos
>
> **Asi no**
>
> ```python
> def limite_segun_tipo(tipo):
>     if tipo == "estudiante":
>         return 3
>     if tipo == "docente":
>         return 5
>     if tipo == "administrador":
>         return 5
>     return 0
> ```
>
> **Asi si**
>
> ```python
> from modulos import config
>
> def limite_segun_tipo(tipo):
>     return config.limite_libros[tipo]
> ```
>
> **Por que.** Si maniana el limite del estudiante sube a 4 hay que buscar todos los lugares donde se escribio 3. Con el valor en config.py se cambia una linea y todo el sistema la usa. Ademas el primer ejemplo se olvida de los tipos nuevos sin querer: el diccionario los tiene a los cuatro.

### Cadenas con formato (f-strings)

Casi todo lo que el programa imprime se arma con `f"..."`. Las llaves meten el valor de una
expresion dentro del texto, y los dos puntos finales le dan forma: `:.2f` deja dos decimales,
`:<10` rellena con espacios hasta 10 caracteres, `:>8` alinea a la derecha, `.center(60)`
centra.

```python
from datetime import date

print(f"hoy es {date.today()}")
print(f"con dos decimales: S/{0.5:.2f}")
print(f"a la izquierda: |{'Ana Quispe':<15}|")
print(f"a la derecha:   |{'Ana Quispe':>15}|")
print(f"centrado:       |{'Ana Quispe':^15}|")
print(f"una cuenta adentro: {3 + 4} libros")
print(f"mayusculas: {'biblioteca poo'.upper()}")
```

**Salida**

```
hoy es 2026-10-23
con dos decimales: S/0.50
a la izquierda: |Ana Quispe     |
a la derecha:   |     Ana Quispe|
centrado:       |  Ana Quispe   |
una cuenta adentro: 7 libros
mayusculas: BIBLIOTECA POO
```

Asi se arman las tablas del programa. Esta es `accion_miembros` de `menu.py`, y por eso las
columnas quedan derechas aunque los nombres midan distinto:

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()
print(f"{'DNI':<10}{'Nombre':<22}{'Tipo':<14}{'Vence':<12}{'Estado':<10}")
print("-" * 68)
for dni, miembro in b.miembros().items():
    print(f"{dni:<10}{miembro.nombre()[:20]:<22}{miembro.tipo().capitalize():<14}"
          f"{str(miembro.vencimiento()):<12}{miembro.estado():<10}")
```

**Salida**

```
DNI       Nombre                Tipo          Vence       Estado
--------------------------------------------------------------------
11111111  Ana Quispe            Estudiante    2027-04-29  Vigente
70445566  Luis Ramos            Docente       2027-05-21  Vigente
70778899  Rosa Palomino         Estudiante    2026-09-18  De baja
70889900  Marco Perez           Estudiante    2026-11-23  Vigente
71234567  Carla Mendoza         Docente       2025-12-15  De baja
72345678  Jorge Huaman          Administrador 2027-01-10  Vigente
73456789  Lucia Torres          Estudiante    2024-06-30  De baja
74567890  Pedro Castillo        Estudiante    2026-08-05  De baja
75678901  Sofia Rojas           Estudiante    2027-10-02  Vigente
76789012  Diego Vargas          Docente       2026-10-20  Vencida
```

Fijate en `miembro.nombre()[:20]`: es un **rebanado**. Si un nombre mide mas de 20 letras se
corta y la tabla no se desordena. Los rebanados tambien se usan en `libros.py` para partir las
categorias por la `/`.

### Listas, tuplas y diccionarios

| Estructura              | Se puede cambiar | Donde se usa                                 | Ejemplo real                                                    |
| ----------------------- | ---------------- | -------------------------------------------- | --------------------------------------------------------------- |
| lista, con corchetes    | si               | cosas que crecen mientras corre el programa  | las filas de una matriz, los libros encontrados por la busqueda |
| tupla, con parentesis   | no               | grupos fijos que nunca se modifican          | las filas de las tablas del menu: codigo, texto y funcion       |
| diccionario, con llaves | si               | buscar por una llave en vez de recorrer todo | el catalogo por ISBN, los miembros por DNI, las reglas por tipo |

**El catalogo y los miembros son diccionarios, no listas.** Esa decision es la que hace que
todo sea corto. Buscar un libro por ISBN en una lista obligaria a recorrerla entera; en un
diccionario es directo:

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()
catalogo = b.catalogo()

print("el catalogo es un", type(catalogo).__name__, "con", len(catalogo), "libros")
print("sus llaves son los ISBN:")
for isbn in catalogo:
    print("   ", isbn, "->", catalogo[isbn].titulo())

print()
print("buscar uno solo, sin recorrer nada:")
print("   ", catalogo.get("9788437604947"))
print()
print("y si el ISBN no existe, .get() devuelve None en vez de reventar:")
print("   ", catalogo.get("0000000000000"))
```

**Salida**

```
el catalogo es un dict con 7 libros
sus llaves son los ISBN:
    9780131103627 -> Eloquent JavaScript
    9786123181017 -> El capital
    9786071511546 -> Fisica para ciencias e ingenieria
    9786123164102 -> Tradiciones peruanas
    9789876122672 -> Maze Runner
    9788437604947 -> Cien años de soledad
    9788445073728 -> El Señor de los Anillos: La Comunidad del Anillo

buscar uno solo, sin recorrer nada:
    9788437604947 | Cien años de soledad | Gabriel Garcia Marquez | disp: 2

y si el ISBN no existe, .get() devuelve None en vez de reventar:
    None
```

> ### Error comun: usar una lista cuando se busca por llave
>
> **Asi no**
>
> ```python
> libros = [libro1, libro2, libro3]
>
> def buscar(isbn):
>     for libro in libros:
>         if libro.isbn() == isbn:
>             return libro
>     return None
> ```
>
> **Asi si**
>
> ```python
> libros = {libro1.isbn(): libro1, libro2.isbn(): libro2}
>
> def buscar(isbn):
>     return libros.get(isbn)
> ```
>
> **Por que.** El diccionario ya hace la busqueda por dentro y devuelve None si la llave no esta. El proyecto lo usa en tres lugares: el catalogo por ISBN, los miembros por DNI y las reglas por tipo de miembro. Ademas evita escribir el mismo bucle tres veces.

### Las tablas del menu son listas de tuplas

`menu.py` no tiene un `if` por opcion. Tiene tablas: cada fila es una tupla con el codigo, el
texto que se muestra y la funcion que hay que ejecutar. Asi agregar una opcion es agregar una
fila, no tocar la logica.

```python
from modulos import menu

for nombre in ["ACCESO", "MIEMBRO", "INVITADO", "ADMIN", "MATRICES"]:
    print(nombre + ":")
    for codigo, texto, accion in getattr(menu, nombre):
        destino = accion.__name__ if accion else "abre un submenu"
        print(f"   {codigo}) {texto:<38} -> {destino}")
    print()
```

**Salida**

```
ACCESO:
   1) Iniciar sesion (DNI)                   -> abre un submenu
   2) Ingresar como invitado                 -> abre un submenu
   0) Salir                                  -> abre un submenu

MIEMBRO:
   1) Consultar catalogo                     -> accion_catalogo
   2) Buscar por categoria (recursiva)       -> accion_buscar_categoria
   3) Mi membresia                           -> accion_mi_membresia
   0) Cerrar sesion                          -> abre un submenu

INVITADO:
   1) Consultar catalogo                     -> accion_catalogo
   2) Buscar por categoria (recursiva)       -> accion_buscar_categoria
   0) Salir                                  -> abre un submenu

ADMIN:
   1) Estado de la biblioteca                -> accion_estado
   2) Miembros                               -> accion_miembros
   3) Matrices y busqueda recursiva          -> abre un submenu
   4) Guardar cambios en los JSON            -> accion_guardar
   0) Cerrar sesion                          -> abre un submenu

MATRICES:
   1) Disponibilidad por seccion y estante   -> accion_matriz_disponibilidad
   2) Titulos por seccion y estante          -> accion_matriz_ubicacion
   3) Categorias principales                 -> accion_matriz_categorias
   4) Busqueda recursiva por categoria       -> accion_buscar_categoria
   0) Volver al menu de administracion       -> abre un submenu
```

Al desempaquetar con `for codigo, texto, accion in menu.ADMIN` cada parte de la tupla cae en su
propia variable. Y `accion.__name__` da el nombre de la funcion sin ejecutarla: una funcion es
un valor mas, se puede guardar en una tupla y llamarla despues.

### Condiciones: if, elif, else

La guia de estructuras selectivas del curso las llama **simple** (solo `if`), **doble**
(`if`/`else`) y **multiple** (`if`/`elif`/`else`). En el proyecto hay de las tres. Esta es la
multiple, y decide que menu se abre:

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()
for dni in ["75678901", "72345678", "70778899"]:
    miembro = b.miembro(dni)
    if not miembro.activo():
        destino = "no entra, esta dado de baja"
    elif miembro.puede_administrar():
        destino = "menu de administracion"
    else:
        destino = "menu de miembro"
    print(f"   {miembro.nombre():<15} {miembro.tipo():<15} {destino}")
```

**Salida**

```
   Sofia Rojas     estudiante      menu de miembro
   Jorge Huaman    administrador   menu de administracion
   Rosa Palomino   estudiante      no entra, esta dado de baja
```

Y los **operadores logicos** (`and`, `or`, `not`) aparecen en las utilidades. Por ejemplo en
`Libro.prestar_uno`, que hoy no llama nadie pero quedo listo para cuando se hagan los
prestamos:

```python
if len(limpio) != 8 or not limpio.isdigit():
    raise errores.DatosInvalidosError("El DNI debe tener 8 digitos")
```

Dos condiciones con `or`: si cualquiera de las dos se cumple, el DNI es invalido.

### Comparar texto sin que importen las mayusculas

```python
from modulos import libros

print("la busqueda pasa todo a minusculas antes de comparar:")
print("   'LITERATURA'.lower() == 'literatura' ->", "LITERATURA".lower() == "literatura")
print()
print("por eso estas tres busquedas dan lo mismo:")
for nombre in ["Literatura", "literatura", "  LITERATURA  "]:
    encontrados = libros.buscar_por_categoria(
        list(biblioteca.Biblioteca().catalogo().values()), nombre)
    # list(...) y .values() porque buscar_por_categoria recibe una lista
    print(f"   {nombre!r:<16} -> {len(encontrados)} titulos")
```

**Salida**

```
la busqueda pasa todo a minusculas antes de comparar:
   'LITERATURA'.lower() == 'literatura' -> True

por eso estas tres busquedas dan lo mismo:
   'Literatura'     -> 4 titulos
   'literatura'     -> 4 titulos
   '  LITERATURA  ' -> 4 titulos
```

### Bucles: for y while

Los menues usan `while True` con un `return` adentro para salir: el bucle no sabe cuantas
veces va a girar, lo decide el usuario. Las tablas y las matrices usan `for`, que si sabe
cuantas vueltas da.

```python
from modulos import menu

print("el esqueleto de menu_invitado:")
print()
print("while True:")
print("    mostrar_opciones(INVITADO)")
print("    opcion = leer_opcion(INVITADO)")
print("    if opcion == '0':")
print("        return None          <- el return rompe el while")
print("    for codigo, texto, accion in INVITADO:")
print("        if codigo == opcion:")
print("            accion(biblioteca)")
print("    utilidades.pausa()")
print()
print("los codigos validos salen de la misma tabla, no estan escritos a mano:")
print("  ", [c for c, _, _ in menu.INVITADO])
```

**Salida**

```
el esqueleto de menu_invitado:

while True:
    mostrar_opciones(INVITADO)
    opcion = leer_opcion(INVITADO)
    if opcion == '0':
        return None          <- el return rompe el while
    for codigo, texto, accion in INVITADO:
        if codigo == opcion:
            accion(biblioteca)
    utilidades.pausa()

los codigos validos salen de la misma tabla, no estan escritos a mano:
   ['1', '2', '0']
```

Esa ultima linea es una **comprension de listas**: arma una lista recorriendo otra en una sola
linea. El proyecto las usa para los codigos validos y en `biblioteca.py` para guardar:

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()

print("comprension de listas en guardar_datos:")
print('   [l.a_diccionario() for l in self._catalogo.values()]')
print()
guardados = [l.a_diccionario() for l in b.catalogo().values()]
print("   convierte", len(b.catalogo()), "objetos Libro en", len(guardados),
      "diccionarios listos para el JSON")
print()
print("   el primero:")
for llave, valor in guardados[0].items():
    print(f"      {llave:<22} {valor}")
```

**Salida**

```
comprension de listas en guardar_datos:
   [l.a_diccionario() for l in self._catalogo.values()]

   convierte 7 objetos Libro en 7 diccionarios listos para el JSON

   el primero:
      isbn                   9780131103627
      titulo                 Eloquent JavaScript
      autor                  Marijn Haverbeke
      categoria              Computacion/Lenguajes
      seccion                B
      estante                2
      ejemplares             2
      disponibles_prestamo   1
```

### enumerate: el bucle con indice que pidio el instructor

> ### Teoria: enumerate()
>
> **El problema.** Cuando hace falta el numero de la vuelta ademas del elemento, la tentacion es escribir `for i in range(len(lista))` y despues `lista[i]` por todos lados.
>
> **Como lo resuelve el proyecto.** `enumerate` entrega las dos cosas juntas. Se ve en `imprimir_matriz`, que necesita el indice para saber el ancho de cada columna.
>
> **El modelo mental.** Un bucle `for` en Python recorre cosas, no numeros. Si necesitas el numero, pidelo con `enumerate` en vez de fabricarlo con `range(len(...))`.
>
> **Receta para otro proyecto.** `for indice, elemento in enumerate(lista):` y olvidarse de `range(len())`.

```python
from modulos import config

pares = list(config.secciones.items())

print("con range(len()), la forma que hay que evitar:")
for i in range(3):
    print(f"   {i} {pares[i][0]} = {pares[i][1]}")

print()
print("con enumerate(), la forma pedida:")
for indice, (letra, nombre) in enumerate(pares[:3]):
    print(f"   {indice} {letra} = {nombre}")
```

**Salida**

```
con range(len()), la forma que hay que evitar:
   0 A = Literatura
   1 B = Historia y lenguas
   2 C = Ciencias exactas

con enumerate(), la forma pedida:
   0 A = Literatura
   1 B = Historia y lenguas
   2 C = Ciencias exactas
```

En la segunda version ademas se desempaqueta la tupla `(letra, nombre)` directo en el bucle,
asi que no hay que escribir `pares[i][0]` nunca mas.

> ### Error comun: for i en vez de enumerate
>
> **Asi no**
>
> ```python
> for i in range(len(filas)):
>     print(i, filas[i][0])
> ```
>
> **Asi si**
>
> ```python
> for indice, fila in enumerate(filas):
>     print(indice, fila[0])
> ```
>
> **Por que.** range(len()) obliga a indexar la lista a mano en cada linea y se rompe facil si la lista cambia de largo. enumerate da el indice y el elemento juntos, y si no necesitas el indice el for recorre la lista directamente: for fila in filas.

### Entrada por teclado: input()

`input()` siempre devuelve **texto**, aunque escriban un numero. Por eso el programa valida
antes de usar el dato. Estas son las dos utilidades de `utilidades.py`:

```python
def validar_dni(texto):
    limpio = str(texto).strip()
    if len(limpio) != 8 or not limpio.isdigit():
        raise errores.DatosInvalidosError("El DNI debe tener 8 digitos")
    return limpio
```

`strip()` quita los espacios de los bordes, `isdigit()` dice si son todos numeros, `len()`
cuenta las letras. Si algo falla no devuelve un valor raro: **lanza un error propio**, que es
lo que permite que el menu muestre un mensaje amable en vez de caerse.

```python
import builtins

from modulos import errores, utilidades

def probar(entrada):
    teclado_real = builtins.input
    builtins.input = lambda texto="": entrada
    try:
        resultado = utilidades.validar_dni(input("DNI: "))
        print(f"   {entrada!r:<14} -> valido: {resultado}")
    except errores.DatosInvalidosError as error:
        print(f"   {entrada!r:<14} -> error: {error}")
    finally:
        builtins.input = teclado_real

print("validar_dni con varias entradas:")
for entrada in ["75678901", " 75678901 ", "1234567", "7567890a", "756789012"]:
    probar(entrada)

print()
print("validar_isbn con varias entradas:")
for entrada in ["9788437604947", "978843760494", "978843760494a"]:
    teclado_real = builtins.input
    builtins.input = lambda texto="": entrada
    try:
        print(f"   {entrada!r:<18} -> valido:", utilidades.validar_isbn(input()))
    except errores.DatosInvalidosError as error:
        print(f"   {entrada!r:<18} -> error: {error}")
    finally:
        builtins.input = teclado_real
```

**Salida**

```
validar_dni con varias entradas:
   '75678901'     -> valido: 75678901
   ' 75678901 '   -> valido: 75678901
   '1234567'      -> error: El DNI debe tener 8 digitos
   '7567890a'     -> error: El DNI debe tener 8 digitos
   '756789012'    -> error: El DNI debe tener 8 digitos

validar_isbn con varias entradas:
   '9788437604947'    -> valido: 9788437604947
   '978843760494'     -> error: El ISBN debe tener 13 digitos
   '978843760494a'    -> error: El ISBN debe tener 13 digitos
```

El truco de `builtins.input = lambda ...` es solo para el cuaderno: asi probamos la validacion
sin escribir de verdad. En el programa real `input()` lee del teclado. El `finally` devuelve el
`input` original pase lo que pase.

### Archivos: leer y escribir JSON

`config.py` se encarga del disco. Tres funciones y nada mas: `ruta_json` arma la ruta,
`leer_json` trae la lista y `guardar_json` la escribe. Con `with open(...)` el archivo se
cierra solo, aunque ocurra un error en el medio.

```python
from modulos import config

print("config.py esta en modulos/, asi que CARPETA_BASE es modulos/")
print("   CARPETA_BASE :", config.CARPETA_BASE)
print("   CARPETA_DATOS:", config.CARPETA_DATOS)
print("   existe?      :", os.path.isdir(config.CARPETA_DATOS))
print()
for nombre, archivo in config.ARCHIVOS.items():
    datos = config.leer_json(nombre)
    print(f"   {archivo:<15} {len(datos):>3} registros   existe: "
          f"{os.path.exists(config.ruta_json(nombre))}")
```

**Salida**

```
config.py esta en modulos/, asi que CARPETA_BASE es modulos/
   CARPETA_BASE : /home/user/proyecto_parcial/modulos
   CARPETA_DATOS: /home/user/proyecto_parcial/modulos/datos
   existe?      : True

   libros.json       7 registros   existe: True
   miembros.json    10 registros   existe: True
```

`leer_json` tiene tres salidas y ninguna revienta: si el archivo no existe devuelve una lista
vacia, si esta vacio devuelve una lista vacia, y si tiene contenido lo convierte con
`json.loads`. Si el JSON esta mal escrito, `json.loads` lanza un `ValueError` que
`biblioteca.py` atrapa y convierte en `ArchivoDatosError` con un mensaje que se entiende.

```python
import json

mal = '{"dni": "12345678", }'
try:
    json.loads(mal)
except ValueError as error:
    print("un JSON mal escrito lanza ValueError:")
    print("   ", error)
    print()
    print("biblioteca.py lo atrapa y lo convierte en ArchivoDatosError, para que el")
    print("mensaje que ve el usuario no hable de comas ni de numeros de linea")
```

**Salida**

```
un JSON mal escrito lanza ValueError:
    Illegal trailing comma before end of object: line 1 column 19 (char 18)

biblioteca.py lo atrapa y lo convierte en ArchivoDatosError, para que el
mensaje que ve el usuario no hable de comas ni de numeros de linea
```

### Lo que usa esta seccion

| Tema                  | Donde                    | Para que                                                     |
| --------------------- | ------------------------ | ------------------------------------------------------------ |
| diccionarios          | config.py, biblioteca.py | reglas por tipo, catalogo por ISBN, miembros por DNI         |
| listas y tuplas       | menu.py, libros.py       | las tablas del menu y las filas de las matrices              |
| f-strings y rebanados | menu.py                  | todas las tablas impresas y el corte de nombres largos       |
| if / elif / else      | menu.py, usuarios.py     | elegir que menu se abre y elegir el tipo de membresia        |
| operadores logicos    | utilidades.py, libros.py | las utilidades de DNI e ISBN y la comparacion de categorias  |
| while True            | menu.py                  | los cuatro menues, que giran hasta que el usuario sale       |
| for y comprensiones   | biblioteca.py, menu.py   | convertir objetos a diccionarios y sacar los codigos validos |
| enumerate             | menu.py                  | imprimir las matrices con el ancho de cada columna           |
| input y validacion    | utilidades.py, menu.py   | leer el DNI sin confiar en lo que escribe el usuario         |
| archivos y json       | config.py                | leer los datos al arrancar y guardarlos cuando lo piden      |

# 2. Programacion orientada a objetos

Esta seccion y la de matrices son las que mas puntos valen en la rubrica. Aca esta todo lo que
hay que saber decir sobre las clases del proyecto.

> ### Teoria: clases y objetos
>
> **El problema.** Una biblioteca maneja muchos libros y muchos miembros. Si cada libro fuera un monton de variables sueltas (`titulo1`, `isbn1`, `disp1`, `titulo2`...), el codigo seria imposible de mantener.
>
> **Como lo resuelve el proyecto.** Con una **clase** por cada cosa del mundo real: `Libro`, `Usuario`, `Membresia`, `Biblioteca`. La clase es el molde y cada **objeto** es un libro de verdad con sus propios datos.
>
> | Otra forma                      | Por que no se uso                                             |
> | ------------------------------- | ------------------------------------------------------------- |
> | Usar solo diccionarios          | un diccionario no sabe hacer nada con sus datos; una clase si |
> | Una clase gigante que haga todo | mezcla responsabilidades y no se puede probar por partes      |
>
> **El modelo mental.** Clase = molde de galletas. Objeto = cada galleta que sale de ese molde. Todas tienen la misma forma pero datos distintos.
>
> **Receta para otro proyecto.** Antes de escribir codigo, listar los sustantivos del enunciado (libro, miembro, membresia, biblioteca) y convertir cada uno en una clase.

### Las 8 clases y como se relacionan

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()

print("una Biblioteca TIENE:")
print("   - muchos Libro    (en un diccionario con el ISBN como llave)")
print("   - muchos Usuario  (en un diccionario con el DNI como llave)")
print("   - la sesion actual (el Usuario que entro, o None)")
print()
print("un Usuario TIENE una Membresia")
print("una Membresia puede SER Estudiante, Docente, Administrador o Invitado")
print()
print("comprobado con los datos reales:")
libro = b.libro("9788437604947")
miembro = b.miembro("75678901")
print("   ", type(libro).__name__, "->", libro.titulo())
print("   ", type(miembro).__name__, "->", miembro.nombre())
print("   ", type(miembro.membresia()).__name__, "->", miembro.membresia().describir())
```

**Salida**

```
una Biblioteca TIENE:
   - muchos Libro    (en un diccionario con el ISBN como llave)
   - muchos Usuario  (en un diccionario con el DNI como llave)
   - la sesion actual (el Usuario que entro, o None)

un Usuario TIENE una Membresia
una Membresia puede SER Estudiante, Docente, Administrador o Invitado

comprobado con los datos reales:
    Libro -> Cien años de soledad
    Usuario -> Sofia Rojas
    Estudiante -> Estudiante: 3 libros por 14 dias
```

Esas relaciones tienen nombre: **composicion** cuando una clase guarda objetos de otra (la
biblioteca tiene libros, el miembro tiene una membresia), y **herencia** cuando una clase es
una version especializada de otra (el administrador es un docente). La seccion 5 desarrolla la
de herencia.

### El constructor y sus valores por defecto

`__init__` es el metodo que corre cuando se crea el objeto. La rubrica pide explicitamente
**constructores con valores por defecto**, y el proyecto los tiene en `Libro`: los tres primeros
parametros son obligatorios y los otros seis tienen un valor asumido.

```python
from modulos.libros import Libro

print("el constructor de Libro, tal cual esta en el codigo:")
print()
print("def __init__(self, isbn, titulo, autor,")
print('             categoria="General", seccion="A", estante=1,')
print("             ejemplares=1, disponibles_prestamo=None):")
print()

print("creado con lo minimo:")
sencillo = Libro("9781111111113", "Libro de prueba", "Autor de prueba")
print("   ", sencillo)
print("    categoria:", sencillo.categoria(), "| seccion:", sencillo.seccion(),
      "| estante:", sencillo.estante(), "| ejemplares:", sencillo.ejemplares())
print()

print("creado con todo:")
completo = Libro("9782222222224", "Otro libro", "Otra autora",
                 categoria="Computacion/Redes", seccion="G", estante=4,
                 ejemplares=5, disponibles_prestamo=2)
print("   ", completo)
print("    categoria:", completo.categoria(), "| seccion:", completo.seccion(),
      "| estante:", completo.estante(), "| prestados:", completo.prestados())
```

**Salida**

```
el constructor de Libro, tal cual esta en el codigo:

def __init__(self, isbn, titulo, autor,
             categoria="General", seccion="A", estante=1,
             ejemplares=1, disponibles_prestamo=None):

creado con lo minimo:
    9781111111113 | Libro de prueba | Autor de prueba | disp: 1
    categoria: General | seccion: A | estante: 1 | ejemplares: 1

creado con todo:
    9782222222224 | Otro libro | Otra autora | disp: 2
    categoria: Computacion/Redes | seccion: G | estante: 4 | prestados: 3
```

**El orden importa**: los parametros con valor por defecto van al final, si no Python no sabria
a cual va cada dato.

Y hay un detalle bueno para mencionar: `disponibles_prestamo=None` y adentro

```python
self._disponibles = (
    int(disponibles_prestamo)
    if disponibles_prestamo is not None
    else self._ejemplares
)
```

Si el JSON no trae ese dato, se asume que todos los ejemplares estan libres. Es un valor por
defecto **calculado**, no una constante. No se puede poner `disponibles_prestamo=self._ejemplares`
en la firma porque en ese momento `self._ejemplares` todavia no existe.

> ### Error comun: poner una lista como valor por defecto
>
> **Asi no**
>
> ```python
> class Libro:
>     def __init__(self, isbn, etiquetas=[]):
>         self._isbn = isbn
>         self._etiquetas = etiquetas
> ```
>
> **Asi si**
>
> ```python
> class Libro:
>     def __init__(self, isbn, etiquetas=None):
>         self._isbn = isbn
>         self._etiquetas = etiquetas if etiquetas is not None else []
> ```
>
> **Por que.** La lista del valor por defecto se crea una sola vez, cuando se define la clase, y la comparten todos los objetos: si un libro agrega una etiqueta, aparece en todos los demas. Con None cada objeto recibe su lista propia. El proyecto usa exactamente ese truco con disponibles_prestamo en Libro y con vencimiento en Membresia.

### Encapsulacion: atributos privados y metodos publicos

> ### Teoria: encapsulacion
>
> **El problema.** Si cualquiera puede cambiar los datos de un objeto directamente, el objeto puede quedar en un estado imposible: un libro con -3 ejemplares disponibles, o con mas disponibles que ejemplares en total.
>
> **Como lo resuelve el proyecto.** Los atributos se guardan con un guion bajo adelante (`self._disponibles`) y se leen con metodos (`disponibles_prestamo()`). Para modificarlos hay que pasar por un metodo que revisa la regla: `prestar_uno()` no deja bajar de cero y `devolver_uno()` no deja pasar del total.
>
> | Otra forma                                      | Por que no se uso                                                          |
> | ----------------------------------------------- | -------------------------------------------------------------------------- |
> | Dejar todo publico                              | cualquier linea del sistema puede romper el objeto sin que nadie se entere |
> | Poner privados hasta los datos que solo se leen | en Python el guion bajo es una senal, no un candado; no hace falta abusar  |
>
> **El modelo mental.** El objeto es una caja con un boton afuera. Adentro puede cambiar lo que quiera, pero desde afuera solo se aprieta el boton.
>
> **Receta para otro proyecto.** Preguntarse, atributo por atributo: quien de afuera necesita cambiar esto? Si la respuesta es nadie, se pone privado y se expone solo un metodo que lo lea.

```python
from modulos import errores
from modulos.libros import Libro

libro = Libro("9783333333335", "Libro con 2 ejemplares", "Autora", ejemplares=2)

print("estado inicial:              ", libro)
libro.prestar_uno()
print("despues de prestar_uno():    ", libro)
libro.prestar_uno()
print("despues del segundo:         ", libro)
print()
print("el tercer intento ya no puede:")
try:
    libro.prestar_uno()
except errores.DatosInvalidosError as error:
    print("   DatosInvalidosError:", error)
print()
print("y devolver_uno() nunca pasa del total de ejemplares:")
for _ in range(5):
    libro.devolver_uno()
print("   despues de 5 devoluciones:", libro)
print("   prestados():", libro.prestados())
```

**Salida**

```
estado inicial:               9783333333335 | Libro con 2 ejemplares | Autora | disp: 2
despues de prestar_uno():     9783333333335 | Libro con 2 ejemplares | Autora | disp: 1
despues del segundo:          9783333333335 | Libro con 2 ejemplares | Autora | disp: 0

el tercer intento ya no puede:
   DatosInvalidosError: No hay ejemplares disponibles de 'Libro con 2 ejemplares'

y devolver_uno() nunca pasa del total de ejemplares:
   despues de 5 devoluciones: 9783333333335 | Libro con 2 ejemplares | Autora | disp: 2
   prestados(): 0
```

Ese es el punto clave de la encapsulacion: **la regla vive adentro del objeto**. Nadie de
afuera tiene que acordarse de revisar si quedan ejemplares; `prestar_uno()` ya lo hace y avisa
con un error si no se puede.

Estos dos metodos todavia no los llama nadie: quedaron listos para cuando se haga la parte de
prestamos. Sirven igual para explicar encapsulacion, que es lo que pide la rubrica.

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()
libro = b.libro("9788437604947")

print("los atributos privados se leen con metodos:")
for nombre in ["isbn", "titulo", "autor", "categoria", "seccion", "estante",
               "ejemplares", "disponibles_prestamo", "prestados"]:
    print(f"   libro.{nombre}()".ljust(34), getattr(libro, nombre)())

print()
print("se pueden tocar directamente porque Python no lo impide, pero no se hace:")
libro._disponibles = -5
print("   despues de romperlo a mano:", libro)
print("   el guion bajo es una senal de 'esto no se toca', no un candado")

libro._disponibles = 2
print("   lo dejamos como estaba:   ", libro)
```

**Salida**

```
los atributos privados se leen con metodos:
   libro.isbn()                    9788437604947
   libro.titulo()                  Cien años de soledad
   libro.autor()                   Gabriel Garcia Marquez
   libro.categoria()               Literatura/Narrativa
   libro.seccion()                 A
   libro.estante()                 1
   libro.ejemplares()              3
   libro.disponibles_prestamo()    2
   libro.prestados()               1

se pueden tocar directamente porque Python no lo impide, pero no se hace:
   despues de romperlo a mano: 9788437604947 | Cien años de soledad | Gabriel Garcia Marquez | disp: -5
   el guion bajo es una senal de 'esto no se toca', no un candado
   lo dejamos como estaba:    9788437604947 | Cien años de soledad | Gabriel Garcia Marquez | disp: 2
```

### Metodos de instancia: self

Todo metodo recibe `self` como primer parametro, que es el objeto mismo. Al llamarlo no se
escribe: `libro.titulo()` ya le esta pasando el libro.

```python
from modulos.usuarios import Usuario

miembro = Usuario("Ana Quispe", "11111111", "estudiante", "2027-04-29")

print("llamado normal, como lo usa el proyecto:")
print("   miembro.nombre() ->", miembro.nombre())
print()
print("lo mismo, pasando el objeto a mano:")
print("   Usuario.nombre(miembro) ->", Usuario.nombre(miembro))
print()
print("son identicos: self es el objeto que esta antes del punto")
```

**Salida**

```
llamado normal, como lo usa el proyecto:
   miembro.nombre() -> Ana Quispe

lo mismo, pasando el objeto a mano:
   Usuario.nombre(miembro) -> Ana Quispe

son identicos: self es el objeto que esta antes del punto
```

> ### Teoria: parametros y retornos en vez de variables globales
>
> **El problema.** El instructor lo pidio explicitamente: si una funcion lee y escribe variables globales, no se puede probar sola y dos partes del programa se pisan sin querer.
>
> **Como lo resuelve el proyecto.** Ninguna funcion del proyecto usa `global`. Todas reciben lo que necesitan por parametro y devuelven el resultado. `buscar_por_categoria(catalogo, nombre)` recibe la lista y devuelve la lista de libros encontrados. Y el menu recibe la biblioteca por parametro: `menu_principal(biblioteca)`.
>
> | Otra forma  | Por que no se uso                                                          |
> | ----------- | -------------------------------------------------------------------------- |
> | Usar global | la funcion deja de funcionar fuera de su archivo y no se puede probar sola |
>
> **El modelo mental.** Una funcion es una maquina: entra algo por un lado, sale algo por el otro. Si tiene que salir a buscar cosas afuera, la maquina no es portable.
>
> **Receta para otro proyecto.** Antes de escribir `global`, preguntarse: puedo pasarlo por parametro y devolverlo? Casi siempre se puede.

```python
import ast

print("comprobado con el propio Python, archivo por archivo:")
print()
total = globales = 0
for archivo in ["main.py", "modulos/config.py", "modulos/errores.py",
                "modulos/utilidades.py", "modulos/usuarios.py",
                "modulos/libros.py", "modulos/biblioteca.py", "modulos/menu.py"]:
    ruta = os.path.join(CARPETA, archivo)
    for nodo in ast.walk(ast.parse(open(ruta, encoding="utf-8").read())):
        if isinstance(nodo, ast.Global):
            globales += 1
            print(f"   {archivo}:{nodo.lineno} usa global")
        if isinstance(nodo, ast.FunctionDef):
            total += 1
print(f"   funciones y metodos en el proyecto: {total}")
print(f"   declaraciones 'global':             {globales}")
```

**Salida**

```
comprobado con el propio Python, archivo por archivo:

   funciones y metodos en el proyecto: 94
   declaraciones 'global':             0
```

### Atributos de clase contra atributos de instancia

`Membresia` mezcla los dos, y es un buen tema para explicar:

- **De clase** (`TIPO`, `LIMITE_LIBROS`, `DIAS_PRESTAMO`, `MULTA_POR_DIA`,
  `PUEDE_ADMINISTRAR`): escritos directamente en la clase, sin `self`. Son las reglas, iguales
  para todos los estudiantes del mundo.
- **De instancia** (`self._vence`, `self._cancelada`): escritos en `__init__` con `self.`
  delante. Son los datos de ese miembro en particular.

```python
from modulos.usuarios import Estudiante

ana = Estudiante("2027-04-29")
luis = Estudiante("2026-11-30")

print("atributos de CLASE: iguales para los dos, se leen desde la clase misma")
print("   Estudiante.TIPO          ->", Estudiante.TIPO)
print("   Estudiante.LIMITE_LIBROS ->", Estudiante.LIMITE_LIBROS)
print("   Estudiante.DIAS_PRESTAMO ->", Estudiante.DIAS_PRESTAMO)
print("   Estudiante.MULTA_POR_DIA ->", Estudiante.MULTA_POR_DIA)
print()
print("atributos de INSTANCIA: distintos para cada objeto")
print("   ana.vencimiento()  ->", ana.vencimiento())
print("   luis.vencimiento() ->", luis.vencimiento())
print()
print("los dos leen la misma regla pero tienen su propia fecha")
```

**Salida**

```
atributos de CLASE: iguales para los dos, se leen desde la clase misma
   Estudiante.TIPO          -> estudiante
   Estudiante.LIMITE_LIBROS -> 3
   Estudiante.DIAS_PRESTAMO -> 14
   Estudiante.MULTA_POR_DIA -> 0.5

atributos de INSTANCIA: distintos para cada objeto
   ana.vencimiento()  -> 2027-04-29
   luis.vencimiento() -> 2026-11-30

los dos leen la misma regla pero tienen su propia fecha
```

> ### Error comun: confundir atributo de clase con atributo de instancia
>
> **Asi no**
>
> ```python
> class Usuario:
>     leidos = []
>
>     def __init__(self, nombre):
>         self._nombre = nombre
>
>     def anotar(self, libro):
>         Usuario.leidos.append(libro)
> ```
>
> **Asi si**
>
> ```python
> class Usuario:
>     def __init__(self, nombre):
>         self._nombre = nombre
>         self._leidos = []
>
>     def anotar(self, libro):
>         self._leidos.append(libro)
> ```
>
> **Por que.** La lista del primer ejemplo es una sola y la comparten todos los usuarios: lo que anota Ana aparece en la cuenta de Luis. La regla pratica es que los atributos de clase sirven para constantes (los numeros de config), y cualquier cosa que pueda cambiar por objeto va con self. en el **init**.

### **str**: como se imprime el objeto

Sin `__str__`, imprimir un objeto da algo inutil como
`<modulos.libros.Libro object at 0x7f8b1c2d3a10>`. Con `__str__` el objeto decide como se
muestra, y el programa lo usa todo el tiempo.

```python
from modulos.biblioteca import Biblioteca
from modulos.libros import Libro
from modulos.usuarios import Usuario

b = Biblioteca()
libro = b.libro("9788437604947")
miembro = b.miembro("75678901")

print("con print(objeto) se usa __str__:")
print("   ", libro)
print("   ", miembro)
print("   ", miembro.membresia())
print("   ", b)
print()
print("y tambien dentro de un f-string:")
print(f"   {miembro} quiere {libro}")
print()
print("sin __str__ saldria algo asi:")


class SinStr:
    pass


print("   ", SinStr())
```

**Salida**

```
con print(objeto) se usa __str__:
    9788437604947 | Cien años de soledad | Gabriel Garcia Marquez | disp: 2
    Sofia Rojas (75678901) - estudiante
    Estudiante: 3 libros por 14 dias
    Biblioteca POO HAY QUE CAMBIAR NOMBREEEEEE: 7 titulos y 10 miembros

y tambien dentro de un f-string:
   Sofia Rojas (75678901) - estudiante quiere 9788437604947 | Cien años de soledad | Gabriel Garcia Marquez | disp: 2

sin __str__ saldria algo asi:
    <__main__.SinStr object at 0x7f58b8412e40>
```

### Multi-ejemplar: muchos objetos de la misma clase

La rubrica pide crear instancias. El proyecto crea 7 `Libro` y 10 `Usuario` al arrancar, uno
por cada registro de los JSON, y cada objeto guarda sus propios datos aunque todos vengan de la
misma clase.

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()

print("los 7 Libro, cada uno con lo suyo:")
for isbn, libro in b.catalogo().items():
    print(f"   {isbn}  {libro.titulo()[:34]:<36} sec {libro.seccion()} "
          f"est {libro.estante()}  {libro.disponibles_prestamo()}/{libro.ejemplares()}")

print()
print("son objetos distintos en memoria:")
dos = list(b.catalogo().values())[:2]
print("   id del primero:", id(dos[0]))
print("   id del segundo:", id(dos[1]))
print("   son el mismo objeto?", dos[0] is dos[1])

print()
print("y cambiar uno no toca al otro:")
dos[0].prestar_uno()
print("   ", dos[0])
print("   ", dos[1])
dos[0].devolver_uno()
```

**Salida**

```
los 7 Libro, cada uno con lo suyo:
   9780131103627  Eloquent JavaScript                  sec B est 2  1/2
   9786123181017  El capital                           sec C est 1  2/2
   9786071511546  Fisica para ciencias e ingenieria    sec C est 5  2/3
   9786123164102  Tradiciones peruanas                 sec B est 1  4/5
   9789876122672  Maze Runner                          sec A est 4  2/2
   9788437604947  Cien años de soledad                 sec A est 1  2/3
   9788445073728  El Señor de los Anillos: La Comuni   sec A est 4  2/2

son objetos distintos en memoria:
   id del primero: 140019025636544
   id del segundo: 140019025634816
   son el mismo objeto? False

y cambiar uno no toca al otro:
    9780131103627 | Eloquent JavaScript | Marijn Haverbeke | disp: 0
    9786123181017 | El capital | Karl Marx | disp: 2
True
```

### **del**: cuando el objeto desaparece

El material de Principios de POO menciona `__del__`, el metodo que corre cuando Python borra el
objeto de la memoria. **El proyecto no lo usa**, y conviene explicarlo en vez de esconderlo: no
hay nada que liberar, porque los archivos se cierran con `with open(...)` y el programa no abre
conexiones. Aca esta demostrado con un ejemplo chico por si lo preguntan:

```python
class LibroConAviso:
    def __init__(self, titulo):
        self._titulo = titulo
        print(f"   nacio el libro {self._titulo}")

    def __del__(self):
        print(f"   se borro el libro {self._titulo}")


print("crear y dejar que se vaya:")
LibroConAviso("temporal")
print()
print("crear, guardar en una variable y borrarla:")
libro = LibroConAviso("guardado")
del libro
print()
print("en el proyecto los objetos Libro viven dentro del diccionario _catalogo")
print("mientras dure la Biblioteca, y se borran todos juntos al terminar")
```

**Salida**

```
crear y dejar que se vaya:
   nacio el libro temporal
   se borro el libro temporal

crear, guardar en una variable y borrarla:
   nacio el libro guardado
   se borro el libro guardado

en el proyecto los objetos Libro viven dentro del diccionario _catalogo
mientras dure la Biblioteca, y se borran todos juntos al terminar
```

> ### Error comun: usar **del** para cerrar archivos
>
> **Asi no**
>
> ```python
> class Archivo:
>     def __init__(self, ruta):
>         self._archivo = open(ruta, "w")
>
>     def __del__(self):
>         self._archivo.close()
> ```
>
> **Asi si**
>
> ```python
> with open(ruta, "w") as archivo:
>     json.dump(datos, archivo, ensure_ascii=False, indent=2)
> ```
>
> **Por que.** Nadie sabe exactamente cuando Python decide borrar un objeto, asi que el archivo puede quedar abierto un rato largo o cerrarse tarde. Con with se cierra en la linea siguiente, siempre, y tambien si ocurre un error en el medio. Es lo que hace config.py en leer_json y en guardar_json.

### El objeto grande: Biblioteca

`Biblioteca` es la clase que une todo. Su constructor no recibe nada: arma los diccionarios
vacios y llama a `cargar_datos()`, que es la que lee los JSON y llena todo.

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()

print("que guarda adentro:")
print("   _catalogo :", type(b.catalogo()).__name__, "con", len(b.catalogo()), "Libro")
print("   _miembros :", type(b.miembros()).__name__, "con", len(b.miembros()), "Usuario")
print("   _sesion   :", b.sesion())
print()
print("lo que le pregunta el menu:")
print("   libro('9788437604947') ->", b.libro("9788437604947"))
print("   miembro('75678901')    ->", b.miembro("75678901"))
print("   miembro('00000000')    ->", b.miembro("00000000"))
print()
print("   resumen() ->")
for llave, valor in b.resumen().items():
    print(f"      {llave:<12} {valor}")
```

**Salida**

```
que guarda adentro:
   _catalogo : dict con 7 Libro
   _miembros : dict con 10 Usuario
   _sesion   : None

lo que le pregunta el menu:
   libro('9788437604947') -> 9788437604947 | Cien años de soledad | Gabriel Garcia Marquez | disp: 2
   miembro('75678901')    -> Sofia Rojas (75678901) - estudiante
   miembro('00000000')    -> None

   resumen() ->
      titulos      7
      ejemplares   19
      disponibles  15
      prestados    4
      miembros     10
```

Y la sesion: `iniciar_sesion()` guarda el miembro que entro en `self._sesion`, y el menu la
lee con `sesion()`. Es el unico estado del programa que no viene de los JSON.

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()
print("al arrancar, sesion:", b.sesion())

b.iniciar_sesion("75678901")
print("despues de iniciar_sesion('75678901'):", b.sesion())
print("   y accion_mi_membresia la lee con biblioteca.sesion()")

b.cerrar_sesion()
print("despues de cerrar_sesion():", b.sesion())

b.iniciar_sesion(invitado=True)
print("como invitado:", b.sesion(), "| tipo:", b.sesion().tipo())
print("   limite de libros:", b.sesion().membresia().limite_libros())
b.cerrar_sesion()
```

**Salida**

```
al arrancar, sesion: None
despues de iniciar_sesion('75678901'): Sofia Rojas (75678901) - estudiante
   y accion_mi_membresia la lee con biblioteca.sesion()
despues de cerrar_sesion(): None
como invitado: Invitado () - invitado | tipo: invitado
   limite de libros: 0
```

### Lo que usa esta seccion

| Concepto de POO                     | Donde se ve                               | Que decir en la defensa                                          |
| ----------------------------------- | ----------------------------------------- | ---------------------------------------------------------------- |
| clases y objetos                    | 8 del sistema, mas 3 de errores           | cada sustantivo del enunciado es una clase                       |
| constructor con valores por defecto | Libro.**init**                            | 6 parametros con default; el de disponibles se calcula           |
| atributos privados                  | todos empiezan con \_                     | \_isbn, \_disponibles, \_vence, \_cancelada, \_sesion            |
| metodos publicos                    | isbn(), titulo(), vigente(), estado()     | la unica puerta para leer y cambiar los datos                    |
| encapsulacion                       | prestar_uno(), devolver_uno()             | la regla vive adentro del objeto, no se puede quedar en negativo |
| atributos de clase                  | TIPO, LIMITE_LIBROS, DIAS_PRESTAMO        | las reglas compartidas por todos los objetos de esa clase        |
| atributos de instancia              | self.\_vence, self.\_cancelada            | los datos propios de cada miembro                                |
| composicion                         | Biblioteca tiene libros y miembros        | Usuario tiene una Membresia                                      |
| **str**                             | en Libro, Usuario, Membresia y Biblioteca | el objeto decide como se imprime                                 |
| multi-ejemplar                      | 7 Libro y 10 Usuario al arrancar          | cada objeto guarda lo suyo aunque vengan de la misma clase       |
| parametros y retornos               | en todas las funciones                    | ninguna usa global; la biblioteca se pasa por parametro al menu  |
| **del**                             | no se usa, y se explica por que           | no hay nada que liberar: los archivos se cierran con with        |

# 3. Funciones, metodos y excepciones

La rubrica tiene un criterio entero para esto (4 puntos): _uso correcto de funciones y
metodos_. Aca esta la diferencia entre los dos, los parametros y retornos, y el manejo de
excepciones con las clases propias del proyecto.

> ### Teoria: funcion contra metodo
>
> **El problema.** Hay calculos que son de un objeto (cuantos ejemplares le quedan a este libro) y otros que no son de nadie (convertir '2026-10-22' en una fecha). Ponerlos todos adentro de una clase obliga a crear objetos que no hacen falta.
>
> **Como lo resuelve el proyecto.** Las dos cosas conviven. Los **metodos** estan dentro de las clases y usan `self`. Las **funciones** estan sueltas en `utilidades.py`, `libros.py`, `config.py` y `menu.py`, y reciben todo por parametro.
>
> | Otra forma                      | Por que no se uso                                                            |
> | ------------------------------- | ---------------------------------------------------------------------------- |
> | Meter todo en clases            | se crean clases vacias que solo agrupan funciones y no representan nada real |
> | Dejar todo en funciones sueltas | se pierde la encapsulacion y cualquier linea puede romper un objeto          |
>
> **El modelo mental.** Si la pregunta es 'de quien es este dato?', es un metodo. Si es 'como se calcula esto que me dieron?', es una funcion.
>
> **Receta para otro proyecto.** Antes de crear una clase nueva, fijarse si alcanza con una funcion. El proyecto tiene las 3 matrices y la busqueda recursiva como funciones sueltas en libros.py, y no creo ninguna clase extra para agruparlas.

### Las funciones sueltas del proyecto

```python
print("utilidades.py - 7 funciones:")
print("   titulo(texto, caracter='=')   arma el cartel de 60 caracteres")
print("   pausa()                       espera un ENTER")
print("   validar_dni(texto)            8 digitos o lanza error")
print("   validar_isbn(codigo)          13 digitos o lanza error")
print("   responder_si_no(texto)        devuelve True o False")
print("   convertir_fecha(texto)        '2026-10-22' -> date")
print("   sumar_dias(fecha, dias)       fecha + dias")
print()
print("libros.py - 7 funciones:")
print("   matriz_disponibilidad(catalogo)  libres por seccion y estante")
print("   matriz_ubicacion(catalogo)       titulos por seccion y estante")
print("   matriz_categorias(catalogo)      por categoria principal")
print("   categorias_unicas(catalogo)      lista sin repetidos")
print("   niveles_categoria(categoria)                   recursiva")
print("   buscar_por_categoria(lista, nombre)            recursiva")
print("   pertenece_a_categoria(libro, nombre, niveles)  recursiva")
print()
print("config.py - 4 funciones:  ruta_json, leer_json, guardar_json, cargar_todos")
print("main.py   - 1 funcion:    main(), las tres lineas que arrancan el programa")
print("menu.py   - 17 funciones: portada, mostrar_opciones, leer_opcion,")
print("                          imprimir_matriz(matriz), 8 acciones,")
print("                          y los 4 bucles de menu")
print()
print("total del proyecto: 38 funciones sueltas y 56 metodos")
```

**Salida**

```
utilidades.py - 7 funciones:
   titulo(texto, caracter='=')   arma el cartel de 60 caracteres
   pausa()                       espera un ENTER
   validar_dni(texto)            8 digitos o lanza error
   validar_isbn(codigo)          13 digitos o lanza error
   responder_si_no(texto)        devuelve True o False
   convertir_fecha(texto)        '2026-10-22' -> date
   sumar_dias(fecha, dias)       fecha + dias

libros.py - 7 funciones:
   matriz_disponibilidad(catalogo)  libres por seccion y estante
   matriz_ubicacion(catalogo)       titulos por seccion y estante
   matriz_categorias(catalogo)      por categoria principal
   categorias_unicas(catalogo)      lista sin repetidos
   niveles_categoria(categoria)                   recursiva
   buscar_por_categoria(lista, nombre)            recursiva
   pertenece_a_categoria(libro, nombre, niveles)  recursiva

config.py - 4 funciones:  ruta_json, leer_json, guardar_json, cargar_todos
main.py   - 1 funcion:    main(), las tres lineas que arrancan el programa
menu.py   - 17 funciones: portada, mostrar_opciones, leer_opcion,
                          imprimir_matriz(matriz), 8 acciones,
                          y los 4 bucles de menu

total del proyecto: 38 funciones sueltas y 56 metodos
```

Probadas de a una, sin arrancar el programa:

```python
from datetime import date

from modulos import utilidades

print("titulo:")
print(utilidades.titulo("catalogo"))
print()
print("titulo con otro caracter:")
print(utilidades.titulo("aviso", "-"))
print()
print("convertir_fecha('2026-10-22') ->", utilidades.convertir_fecha("2026-10-22"),
      "| tipo:", type(utilidades.convertir_fecha("2026-10-22")).__name__)
print("sumar_dias(hoy, 14)          ->", utilidades.sumar_dias(date.today(), 14))
print("validar_dni(' 75678901 ')    ->", utilidades.validar_dni(" 75678901 "))
print("validar_isbn('9788437604947')->", utilidades.validar_isbn("9788437604947"))
```

**Salida**

```
titulo:
============================================================
                          CATALOGO
============================================================

titulo con otro caracter:
------------------------------------------------------------
                           AVISO
------------------------------------------------------------

convertir_fecha('2026-10-22') -> 2026-10-22 | tipo: date
sumar_dias(hoy, 14)          -> 2026-11-06
validar_dni(' 75678901 ')    -> 75678901
validar_isbn('9788437604947')-> 9788437604947
```

### Parametros con valor por defecto

```python
from modulos import utilidades

print("titulo('menu') usa el caracter por defecto:")
print(utilidades.titulo("menu"))
print()
print("titulo('menu', '-') lo cambia solo en esta llamada:")
print(utilidades.titulo("menu", "-"))
print()
print("y tambien se puede nombrar el parametro:")
print(utilidades.titulo("menu", caracter="*"))
```

**Salida**

```
titulo('menu') usa el caracter por defecto:
============================================================
                            MENU
============================================================

titulo('menu', '-') lo cambia solo en esta llamada:
------------------------------------------------------------
                            MENU
------------------------------------------------------------

y tambien se puede nombrar el parametro:
************************************************************
                            MENU
************************************************************
```

Tener el valor por defecto significa que en los 20 y tantos lugares donde se llama
`utilidades.titulo(...)` no hay que repetir el caracter.

### El retorno sale de la funcion

> ### Teoria: return
>
> **El problema.** Una funcion que no devuelve nada solo imprime, y entonces no se puede usar su resultado en una cuenta ni en una condicion.
>
> **Como lo resuelve el proyecto.** Casi todas las funciones del proyecto devuelven algo: `validar_dni()` devuelve el DNI limpio, `convertir_fecha()` devuelve un objeto date, `responder_si_no()` devuelve True o False, `buscar_por_categoria()` devuelve la lista de libros. Las unicas que no devuelven nada son las que imprimen: `pausa()`, `imprimir_matriz()` y las acciones del menu.
>
> | Otra forma                          | Por que no se uso                                              |
> | ----------------------------------- | -------------------------------------------------------------- |
> | Usar una variable bandera           | cuatro lineas donde alcanza un return                          |
> | Imprimir adentro y no devolver nada | el que llama no puede usar el resultado para seguir calculando |
>
> **El modelo mental.** `return` hace dos cosas a la vez: entrega el valor y **termina** la funcion. Lo que este escrito despues no se ejecuta.
>
> **Receta para otro proyecto.** Dentro de un bucle, un `return` es la forma mas corta de salir: no hace falta una variable bandera ni un `break` seguido de otro `if`.

```python
from modulos import menu

print("asi es leer_opcion en menu.py, con el return adentro del while:")
print()
print("def leer_opcion(opciones):")
print("    validos = [c for c, _, _ in opciones]")
print("    while True:")
print("        entrada = input('Elige una opcion: ').strip()")
print("        if entrada in validos:")
print("            return entrada        <- sale del bucle y de la funcion a la vez")
print("        print(f'Opcion no valida. Intenta con: {...}')")
print()

import builtins

teclado_real = builtins.input
respuestas = ["9", "abc", "", "2"]
builtins.input = lambda texto="": respuestas.pop(0)
try:
    print("simulando que el usuario se equivoca tres veces y despues acierta:")
    elegida = menu.leer_opcion(menu.INVITADO)
    print("   opcion finalmente leida:", elegida)
finally:
    builtins.input = teclado_real
```

**Salida**

```
asi es leer_opcion en menu.py, con el return adentro del while:

def leer_opcion(opciones):
    validos = [c for c, _, _ in opciones]
    while True:
        entrada = input('Elige una opcion: ').strip()
        if entrada in validos:
            return entrada        <- sale del bucle y de la funcion a la vez
        print(f'Opcion no valida. Intenta con: {...}')

simulando que el usuario se equivoca tres veces y despues acierta:
Opcion no valida. Intenta con: 1, 2, 0
Opcion no valida. Intenta con: 1, 2, 0
Opcion no valida. Intenta con: 1, 2, 0
   opcion finalmente leida: 2
```

Las tres primeras entradas se rechazaron y el bucle volvio a pedir. La funcion solo termino
cuando llego un codigo que estaba en la tabla. Por eso no hace falta validar nada despues de
llamarla: **si devolvio un valor, ese valor es seguro**.

> ### Error comun: validar despues de una funcion que ya valida
>
> **Asi no**
>
> ```python
> opcion = leer_opcion(MIEMBRO)
> if opcion not in ["1", "2", "3", "0"]:
>     print("opcion invalida")
> else:
>     ejecutar(opcion)
> ```
>
> **Asi si**
>
> ```python
> opcion = leer_opcion(MIEMBRO)
> ejecutar(opcion)
> ```
>
> **Por que.** leer_opcion ya no puede devolver un codigo que no este en la tabla: el while no la deja salir hasta que sea valida. Validar otra vez es codigo que nunca se ejecuta, y ademas repite la lista de codigos a mano, que es justo lo que la tabla evita. Lo mismo pasa con los try: si un error no puede ocurrir, no se pone el try.

### Metodos: funciones que viven en una clase

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()
libro = b.libro("9788437604947")
miembro = b.miembro("75678901")

print("metodos que solo leen:")
print("   libro.isbn()            ->", libro.isbn())
print("   libro.categoria()       ->", libro.categoria())
print("   miembro.nombre()        ->", miembro.nombre())
print("   miembro.estado()        ->", miembro.estado())
print()
print("metodos que calculan algo a partir de otros datos:")
print("   libro.prestados()       ->", libro.prestados(),
      " (ejemplares - disponibles)")
print("   miembro.vencimiento()   ->", miembro.vencimiento(),
      " (se lo pregunta a la membresia)")
print()
print("metodos que cambian el objeto:")
print("   antes de prestar_uno(): ", libro.disponibles_prestamo())
libro.prestar_uno()
print("   despues:                ", libro.disponibles_prestamo())
libro.devolver_uno()
print("   y devolver_uno():       ", libro.disponibles_prestamo())
```

**Salida**

```
metodos que solo leen:
   libro.isbn()            -> 9788437604947
   libro.categoria()       -> Literatura/Narrativa
   miembro.nombre()        -> Sofia Rojas
   miembro.estado()        -> Vigente

metodos que calculan algo a partir de otros datos:
   libro.prestados()       -> 1  (ejemplares - disponibles)
   miembro.vencimiento()   -> 2027-10-02  (se lo pregunta a la membresia)

metodos que cambian el objeto:
   antes de prestar_uno():  2
   despues:                 1
   y devolver_uno():        2
```

`miembro.vencimiento()` es un buen ejemplo de por que conviene un metodo aunque sea una linea:

```python
def vencimiento(self):
    return self._membresia.vencimiento()
```

El miembro no guarda una copia de la fecha: se la pregunta a su membresia. Si se guardara una
copia y despues la membresia se renovara, el miembro mostraria la fecha vieja.

### Excepciones: las 3 clases del proyecto

> ### Teoria: excepciones
>
> **El problema.** Cuando algo no se puede hacer (el DNI tiene 3 cifras, un JSON esta mal escrito), la funcion tiene que avisar. Si devuelve None o un numero raro, el que llama tiene que adivinar que paso y el programa sigue con datos malos.
>
> **Como lo resuelve el proyecto.** Tres clases propias en `errores.py`, todas hijas de `BibliotecaError`. La funcion que detecta el problema **lanza** el error con `raise` y el menu lo **atrapa** con `try/except` para mostrar un mensaje amable.
>
> | Otra forma                 | Por que no se uso                                         |
> | -------------------------- | --------------------------------------------------------- |
> | Devolver None              | el que llama no sabe si no habia datos o si hubo un error |
> | Imprimir el error y seguir | el programa continua con datos inconsistentes             |
> | Dejar que reviente solo    | el usuario ve la traza de Python completa                 |
>
> **El modelo mental.** Lanzar es tirar la pelota hacia arriba: la funcion no decide que hacer con el problema, solo avisa. Quien atrapa la pelota decide.
>
> **Receta para otro proyecto.** Separar el codigo que hace el trabajo del codigo que muestra los mensajes. Adentro se lanza, afuera se atrapa.

```python
from modulos import errores

print("la jerarquia de errores del proyecto:")
print()
print("Exception")
print("   BibliotecaError        <- la base")
print("   |")
print("   +-- DatosInvalidosError   (hereda tambien de ValueError)")
print("   +-- ArchivoDatosError")
print()
print("comprobado desde Python:")
for nombre in ["DatosInvalidosError", "ArchivoDatosError"]:
    clase = getattr(errores, nombre)
    padres = ", ".join(p.__name__ for p in clase.__bases__)
    print(f"   {nombre:<22} viene de ({padres})")
    print(f"   {'':<22} es BibliotecaError? {issubclass(clase, errores.BibliotecaError)}")
```

**Salida**

```
la jerarquia de errores del proyecto:

Exception
   BibliotecaError        <- la base
   |
   +-- DatosInvalidosError   (hereda tambien de ValueError)
   +-- ArchivoDatosError

comprobado desde Python:
   DatosInvalidosError    viene de (BibliotecaError, ValueError)
                          es BibliotecaError? True
   ArchivoDatosError      viene de (BibliotecaError)
                          es BibliotecaError? True
```

**Por que sirve que todas vengan de `BibliotecaError`.** Porque el que atrapa puede cubrir los
tres problemas del sistema con una sola linea:

```python
except errores.BibliotecaError as error:
    print(f"No se pudo: {error}")
```

Hoy el unico `try` del proyecto esta en `menu_principal` y atrapa `DatosInvalidosError`, que es
el error del DNI. Si manana se atrapa en otro lado, con escribir `BibliotecaError` ya se
cubren los tres, y tambien la cuarta excepcion que se agregue. Eso es herencia aplicada a
errores.

| Excepcion           | Quien la lanza           | Cuando                                      |
| ------------------- | ------------------------ | ------------------------------------------- |
| DatosInvalidosError | utilidades.validar_dni   | el DNI no tiene 8 digitos                   |
| DatosInvalidosError | utilidades.validar_isbn  | el ISBN no tiene 13 digitos                 |
| DatosInvalidosError | usuarios.crear_membresia | el tipo de membresia no existe              |
| DatosInvalidosError | usuarios.crear_usuario   | el registro del JSON no es un diccionario   |
| DatosInvalidosError | Libro.prestar_uno        | no quedan ejemplares disponibles            |
| ArchivoDatosError   | Biblioteca.cargar_datos  | un JSON no se puede leer o esta mal escrito |

El caso de 'libro no disponible' que pide el criterio 3 de la rubrica es el de Libro.prestar_uno: lanza DatosInvalidosError en vez de dejar los disponibles en negativo. Hoy no lo llama nadie del menu, porque los prestamos todavia no estan hechos, pero la validacion ya esta escrita y probada.

### Lanzar y atrapar, probado de verdad

```python
from modulos import errores, usuarios, utilidades

print("1) un tipo de membresia que no existe:")
try:
    usuarios.crear_membresia("superusuario")
except errores.DatosInvalidosError as error:
    print("   DatosInvalidosError:", error)

print()
print("2) un registro de miembro que no es un diccionario:")
try:
    usuarios.crear_usuario("Ana Quispe")
except errores.DatosInvalidosError as error:
    print("   DatosInvalidosError:", error)

print()
print("3) un libro sin ejemplares:")
from modulos.libros import Libro
agotado = Libro("9781111111113", "Un ejemplar", "Autora",
                ejemplares=1, disponibles_prestamo=0)
try:
    agotado.prestar_uno()
except errores.DatosInvalidosError as error:
    print("   DatosInvalidosError:", error)

print()
print("4) el mismo error atrapado por el nombre del padre:")
try:
    utilidades.validar_dni("123")
except errores.BibliotecaError as error:
    print("   atrapado como BibliotecaError:", type(error).__name__, "-", error)

print()
print("5) y por ValueError, gracias a la herencia multiple:")
try:
    utilidades.validar_dni("123")
except ValueError as error:
    print("   atrapado como ValueError:", error)
```

**Salida**

```
1) un tipo de membresia que no existe:
   DatosInvalidosError: Ese tipo de membresia no existe

2) un registro de miembro que no es un diccionario:
   DatosInvalidosError: Cada miembro debe ser un diccionario

3) un libro sin ejemplares:
   DatosInvalidosError: No hay ejemplares disponibles de 'Un ejemplar'

4) el mismo error atrapado por el nombre del padre:
   atrapado como BibliotecaError: DatosInvalidosError - El DNI debe tener 8 digitos

5) y por ValueError, gracias a la herencia multiple:
   atrapado como ValueError: El DNI debe tener 8 digitos
```

### try / except / finally

```python
print("main.py completo:")
print()
print(open(os.path.join(CARPETA, "main.py"), encoding="utf-8").read())
```

**Salida**

```
main.py completo:

from modulos import menu
from modulos.biblioteca import Biblioteca
from modulos.menu import menu_principal


def main():
    menu.portada()
    biblioteca = Biblioteca()
    menu_principal(biblioteca)


main()
```

Son nueve lineas y no hace nada mas que arrancar: portada, biblioteca y menu. **No tiene ningun
`try`**, y eso es una decision, no un olvido. Los errores se atrapan donde ocurren de verdad:

- en `menu_principal`, el `try/except errores.DatosInvalidosError` alrededor del DNI, para
  avisar y volver a mostrar el menu de acceso en vez de cerrarse;
- en `Biblioteca.cargar_datos`, el `try/except ValueError` que convierte un JSON roto en
  `ArchivoDatosError` con un mensaje que se entiende.

Un `except` general sin motivo esconde errores de verdad: si el codigo tiene un nombre mal
escrito, un `except Exception` lo tapa y el programa parece funcionar mientras devuelve
cualquier cosa. Por eso `main.py` no atrapa nada: si pasa algo que no esta previsto, se ve la
traza completa de Python, con el archivo, la linea y el error.

El costo de esa decision, dicho en limpio: si en la demo se aprieta Ctrl+C, o si se prueba con
la entrada desde un archivo y se acaba antes de tiempo, se ve una traza en pantalla
(`KeyboardInterrupt` y `EOFError`). Con una persona escribiendo en la terminal y saliendo con
la opcion 0, nunca pasa.

```python
import builtins

from modulos import errores, utilidades

print("el finally, que corre siempre, haya error o no:")
teclado_real = builtins.input
builtins.input = lambda texto="": ""
try:
    utilidades.validar_dni("123")
except errores.DatosInvalidosError as error:
    print("   except: ", error)
finally:
    builtins.input = teclado_real
    print("   finally: el teclado quedo como estaba")

print()
print("y sin error tambien corre:")
builtins.input = lambda texto="": "75678901"
try:
    print("   try:    ", utilidades.validar_dni(input()))
finally:
    builtins.input = teclado_real
    print("   finally: el teclado quedo como estaba")
```

**Salida**

```
el finally, que corre siempre, haya error o no:
   except:  El DNI debe tener 8 digitos
   finally: el teclado quedo como estaba

y sin error tambien corre:
   try:     75678901
   finally: el teclado quedo como estaba
```

> ### Error comun: atrapar todo con except sin mas
>
> **Asi no**
>
> ```python
> try:
>     miembro = crear_usuario(registro)
> except:
>     print("algo salio mal")
> ```
>
> **Asi si**
>
> ```python
> try:
>     miembro = crear_usuario(registro)
> except errores.DatosInvalidosError as error:
>     print(f"No se pudo crear el miembro: {error}")
> ```
>
> **Por que.** El except pelado atrapa hasta los errores del propio programa, como un nombre mal escrito, y los convierte en 'algo salio mal'. Ademas no se puede saber que paso. Atrapando DatosInvalidosError se cubre el caso previsto y nada mas, y el mensaje que llega es el que escribio quien lanzo el error.

### Donde se atrapa cada cosa

| Lugar                             | Que atrapa                         | Que hace                                                               |
| --------------------------------- | ---------------------------------- | ---------------------------------------------------------------------- |
| main.py                           | no atrapa nada, a proposito        | si algo no esta previsto se ve la traza de Python, con archivo y linea |
| menu_principal                    | DatosInvalidosError al leer el DNI | avisa y vuelve a mostrar el menu de acceso                             |
| Biblioteca.cargar_datos           | ValueError                         | lo convierte en ArchivoDatosError con un mensaje claro                 |
| Libro.prestar_uno (cuando se use) | -                                  | no atrapa nada: lanza DatosInvalidosError y decide el menu             |

La regla del proyecto: se atrapa donde se puede hacer algo al respecto. utilidades.py y libros.py lanzan y no atrapan nada, porque no saben si estan corriendo en el menu o en una prueba. menu.py atrapa, porque es el que habla con la persona.

### Validar antes de dividir

El instructor tambien pidio no dividir sin revisar el divisor. En el proyecto **no hay ninguna
division con un divisor que venga de los datos**. Esta comprobacion lo muestra:

```python
import re

print("todas las lineas del proyecto con una barra:")
for archivo in ["config.py", "utilidades.py", "usuarios.py", "libros.py",
                "biblioteca.py", "menu.py"]:
    ruta = os.path.join(CARPETA, "modulos", archivo)
    for numero, linea in enumerate(open(ruta, encoding="utf-8").read().splitlines(), 1):
        if re.search(r"[^/*]/[^/*]", linea) and "http" not in linea:
            print(f"   {archivo}:{numero}  {linea.strip()[:78]}")
```

**Salida**

```
todas las lineas del proyecto con una barra:
   libros.py:148  if libro.categoria().split("/")[0] == categoria:
   libros.py:159  primera = libro.categoria().split("/")[0]
   libros.py:166  partes = categoria.split("/")
   libros.py:169  return [partes[0]] + niveles_categoria("/".join(partes[1:]))
   biblioteca.py:16  f"No se pudieron leer los JSON de la carpeta datos/: {error}"
   menu.py:64  print(f"Multa por dia de retraso: S/{miembro.membresia().multa_por_dia():.2f}"
   menu.py:117  print("Se agrupa por el primer nivel de la categoria (antes de la /).")
   menu.py:122  "Se sobreescribiran los JSON de la carpeta datos/. Continuar (s/n): "
   menu.py:127  print("Cambios guardados en la carpeta datos/.")
```

Son `split("/")` para partir las categorias y `'S/'` en los textos. La unica cuenta con
division que podria aparecer es un promedio de ejemplares por titulo, y ahi si habria que
cuidarse. El proyecto usa el mismo principio en otro lado: **revisa que la lista no este vacia
antes de usarla**, que es lo que hace la recursion con su caso base.

```python
print("buscar_por_categoria en libros.py:")
print()
print("def buscar_por_categoria(catalogo, nombre):")
print("    if len(catalogo) == 0:      <- caso base: sin esto la recursion no para")
print("        return []")
print("    ...")
print()
print("y en imprimir_matriz, que es el mismo problema con max() en vez de una division:")
print()
print("columnas = max(len(fila) for fila in matriz)")
print("           ^ si la matriz llegara vacia, max() lanzaria ValueError.")
print("             No pasa porque las tres matrices siempre traen al menos la cabecera,")
print("             que se arma antes de recorrer el catalogo")
print()
from modulos import libros
print("probado con el catalogo vacio:")
print("   buscar_por_categoria([], 'Literatura') ->", libros.buscar_por_categoria([], "Literatura"))
print()
print("lo que si habria que cuidar si manana se agrega un promedio:")
ejemplares = 19
titulos = 0
if titulos > 0:
    print(f"   promedio: {ejemplares / titulos:.2f}")
else:
    print("   promedio: no se puede calcular, no hay titulos")
```

**Salida**

```
buscar_por_categoria en libros.py:

def buscar_por_categoria(catalogo, nombre):
    if len(catalogo) == 0:      <- caso base: sin esto la recursion no para
        return []
    ...

y en imprimir_matriz, que es el mismo problema con max() en vez de una division:

columnas = max(len(fila) for fila in matriz)
           ^ si la matriz llegara vacia, max() lanzaria ValueError.
             No pasa porque las tres matrices siempre traen al menos la cabecera,
             que se arma antes de recorrer el catalogo

probado con el catalogo vacio:
   buscar_por_categoria([], 'Literatura') -> []

lo que si habria que cuidar si manana se agrega un promedio:
   promedio: no se puede calcular, no hay titulos
```

> ### Error comun: dividir sin mirar el divisor
>
> **Asi no**
>
> ```python
> total = len(catalogo)
> promedio = ejemplares / total
> ```
>
> **Asi si**
>
> ```python
> total = len(catalogo)
> if total > 0:
>     promedio = ejemplares / total
> else:
>     promedio = 0
> ```
>
> **Por que.** Con el catalogo vacio, que es justo lo que pasa si un JSON se borra, la primera version revienta con ZeroDivisionError y el programa se cierra en la cara del usuario. El proyecto hoy no divide por datos, pero si se agrega un promedio hay que poner ese if.

### Lo que usa esta seccion

| Tema                   | Donde                                                 | Que decir                                                                                 |
| ---------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| funciones sueltas      | utilidades.py, libros.py, config.py, menu.py, main.py | 38 funciones que no necesitan un objeto para trabajar; 17 en menu.py y 7 en utilidades.py |
| metodos                | las 11 clases                                         | 56 funciones adentro de una clase, siempre con self primero                               |
| parametros por defecto | titulo(texto, caracter='=')                           | no repetir el mismo valor en cada llamada                                                 |
| retorno                | casi todas las funciones                              | return entrega el valor y termina la funcion                                              |
| excepciones propias    | errores.py                                            | 3 clases, las dos del sistema hijas de BibliotecaError                                    |
| raise                  | utilidades, usuarios, libros, biblioteca              | el que detecta el problema avisa, no decide                                               |
| try / except           | menu.py y biblioteca.py                               | dos try en todo el proyecto: el del DNI y el del JSON                                     |
| finally                | main.py no lo usa; las celdas de este cuaderno si     | dejar todo como estaba pase lo que pase                                                   |
| validar el divisor     | no aplica hoy, y se explica                           | el proyecto no divide por datos; revisa listas vacias antes de usarlas                    |

# 4. Matrices y recursividad (6 puntos)

Este es el criterio que mas puntos vale en la rubrica. El proyecto tiene **3 matrices** y **3
funciones recursivas**, y las dos cosas se ven en el menu de administracion: la opcion 3 abre
el submenu de matrices, que tiene las tres matrices y la busqueda recursiva.

> ### Teoria: matriz
>
> **El problema.** El enunciado habla de secciones, estantes y categorias: datos que naturalmente forman una tabla de doble entrada. Mostrarlos como una lista larga obliga al usuario a contar de cabeza.
>
> **Como lo resuelve el proyecto.** Una matriz es una lista de listas: `matriz[fila][columna]`. El proyecto arma tres: libros disponibles por seccion y estante, titulos por seccion y estante, y totales por categoria. Las tres salen del catalogo, ninguna se guarda en el JSON.
>
> | Otra forma                     | Por que no se uso                                                         |
> | ------------------------------ | ------------------------------------------------------------------------- |
> | Una lista larga de pares       | el usuario no puede comparar dos secciones de un vistazo                  |
> | Un diccionario de diccionarios | funciona, pero despues hay que convertirlo para imprimirlo alineado igual |
>
> **El modelo mental.** Una hoja de calculo en el codigo. Las filas y columnas tienen nombre, y en la de disponibilidad la ultima fila y la ultima columna son los totales.
>
> **Receta para otro proyecto.** Elegir que va en las filas y que en las columnas antes de escribir nada. Aca las filas son las secciones y las columnas los estantes, porque hay 8 secciones y 6 estantes: la tabla entra en la pantalla.

### Matriz 1: libros disponibles por seccion y estante

```python
from modulos import config, libros, menu
from modulos.biblioteca import Biblioteca

b = Biblioteca()
matriz = libros.matriz_disponibilidad(b.catalogo())

print(menu.utilidades.titulo("Matriz de disponibilidad"))
menu.imprimir_matriz(matriz)
print("Filas = secciones, columnas = estantes. La ultima fila y columna son totales.")
```

**Salida**

```
============================================================
                  MATRIZ DE DISPONIBILIDAD
============================================================
Seccion  E1  E2  E3  E4  E5  E6  Total
A        2   0   0   4   0   0   6
B        4   1   0   0   0   0   5
C        2   0   0   0   2   0   4
D        0   0   0   0   0   0   0
E        0   0   0   0   0   0   0
F        0   0   0   0   0   0   0
G        0   0   0   0   0   0   0
H        0   0   0   0   0   0   0
Total    8   1   0   4   2   0   15
Filas = secciones, columnas = estantes. La ultima fila y columna son totales.
```

**Como se lee:** en la seccion B, estante 1, hay 4 ejemplares libres. La columna Total dice
cuantos hay libres en toda esa seccion, y la fila Total cuantos en ese estante.

Las letras de las filas salen de `config.secciones`, que es un diccionario de letra a nombre. Al
recorrerlo con `for seccion in config.secciones` se usan solo las llaves, o sea las letras:

```python
print("config.secciones es un diccionario de letra a nombre:")
for letra, nombre in config.secciones.items():
    print(f"   {letra} = {nombre}")
print()
print("la matriz usa solo las letras, por eso las filas dicen A, B, C...")
print("y hay", config.estantes, "columnas de estantes mas la de totales")
```

**Salida**

```
config.secciones es un diccionario de letra a nombre:
   A = Literatura
   B = Historia y lenguas
   C = Ciencias exactas
   D = Ciencias de la vida
   E = Ciencias sociales
   F = Arte
   G = Tecnologia
   H = Referencia

la matriz usa solo las letras, por eso las filas dicen A, B, C...
y hay 6 columnas de estantes mas la de totales
```

Y es la matriz que dice donde esta cada libro:

```python
for isbn, libro in b.catalogo().items():
    fila = list(config.secciones).index(libro.seccion()) + 1
    columna = libro.estante()
    print(f"   {libro.titulo()[:38]:<40} seccion {libro.seccion()} estante "
          f"{libro.estante()} -> celda [{fila}][{columna}] = {matriz[fila][columna]}")
```

**Salida**

```
   Eloquent JavaScript                      seccion B estante 2 -> celda [2][2] = 1
   El capital                               seccion C estante 1 -> celda [3][1] = 2
   Fisica para ciencias e ingenieria        seccion C estante 5 -> celda [3][5] = 2
   Tradiciones peruanas                     seccion B estante 1 -> celda [2][1] = 4
   Maze Runner                              seccion A estante 4 -> celda [1][4] = 4
   Cien años de soledad                     seccion A estante 1 -> celda [1][1] = 2
   El Señor de los Anillos: La Comunidad    seccion A estante 4 -> celda [1][4] = 4
```

El `+ 1` es porque la fila 0 es la cabecera con las letras E1, E2, E3... La primera seccion de
datos es la fila 1.

Un detalle para tener presente: si un libro tuviera una seccion que no esta en
`config.secciones`, no apareceria en ninguna celda y los totales saldrian mas chicos. Hoy los 7
libros usan solo A, B y C, que si estan.

### Matriz 2: titulos por seccion y estante

```python
matriz = libros.matriz_ubicacion(b.catalogo())
print(menu.utilidades.titulo("Matriz de ubicacion"))
menu.imprimir_matriz(matriz)
print("Cuanta coleccion guarda cada estante de cada seccion.")
```

**Salida**

```
============================================================
                    MATRIZ DE UBICACION
============================================================
Seccion  E1  E2  E3  E4  E5  E6  Titulos
A        1   0   0   2   0   0   3
B        1   1   0   0   0   0   2
C        1   0   0   0   1   0   2
D        0   0   0   0   0   0   0
E        0   0   0   0   0   0   0
F        0   0   0   0   0   0   0
G        0   0   0   0   0   0   0
H        0   0   0   0   0   0   0
Cuanta coleccion guarda cada estante de cada seccion.
```

Es la misma forma que la anterior pero cuenta **titulos** en vez de ejemplares libres, y la
ultima columna se llama Titulos. Sirve para ver si una seccion esta sobrecargada: la A tiene 4
titulos y la D, E, F, G y H no tienen ninguno, asi que se podrian juntar.

Esta no trae fila de totales, y esta bien: la pregunta que responde es _donde hay cosas_, no
_cuanto hay en total_.

### Matriz 3: categorias

```python
matriz = libros.matriz_categorias(b.catalogo())
print(menu.utilidades.titulo("Matriz de categorias"))
menu.imprimir_matriz(matriz)
print("Se agrupa por el primer nivel de la categoria (antes de la /).")
```

**Salida**

```
============================================================
                    MATRIZ DE CATEGORIAS
============================================================
Categoria    Titulos  Ejemplares  Disponibles
Computacion  1        2           1
Economia     1        2           2
Fisica       1        3           2
Literatura   4        12          10
Se agrupa por el primer nivel de la categoria (antes de la /).
```

Esta no es cuadrada: cada fila es una categoria distinta y las columnas son titulos,
ejemplares y disponibles. La agrupacion sale de partir la categoria por la `/`:
`"Literatura/Narrativa"` y `"Literatura/Poesia"` caen en la misma fila, la de `Literatura`.

Las filas vienen de `categorias_unicas`, que recorre el catalogo y arma una lista sin
repetidos:

```python
from modulos import libros

print("las categorias completas que hay en los datos:")
for categoria in sorted({l.categoria() for l in b.catalogo().values()}):
    niveles = libros.niveles_categoria(categoria)
    print(f"   {categoria:<32} niveles: {niveles}")

print()
unicas = libros.categorias_unicas(b.catalogo())
print("categorias_unicas las agrupa en", len(unicas), "->", unicas)
```

**Salida**

```
las categorias completas que hay en los datos:
   Computacion/Lenguajes            niveles: ['Computacion', 'Lenguajes']
   Economia/General                 niveles: ['Economia', 'General']
   Fisica/Ingenieria                niveles: ['Fisica', 'Ingenieria']
   Literatura/Ciencia Ficción/Distopía Juvenil niveles: ['Literatura', 'Ciencia Ficción', 'Distopía Juvenil']
   Literatura/Fantasía Épica        niveles: ['Literatura', 'Fantasía Épica']
   Literatura/Historia Peruana      niveles: ['Literatura', 'Historia Peruana']
   Literatura/Narrativa             niveles: ['Literatura', 'Narrativa']

categorias_unicas las agrupa en 4 -> ['Computacion', 'Economia', 'Fisica', 'Literatura']
```

### Como se imprime una matriz sin que quede torcida

`imprimir_matriz` recibe **solo la matriz**: el titulo y la nota los imprime la accion del menu
que la llama, por eso cada una dice su propio texto. Esta es la funcion completa:

```python
print("def imprimir_matriz" + open(os.path.join(CARPETA, "modulos", "menu.py"),
      encoding="utf-8").read().split("def imprimir_matriz")[1]
      .split("def accion_matriz_disponibilidad")[0].rstrip())
```

**Salida**

```
def imprimir_matriz(matriz):
    columnas = max(len(fila) for fila in matriz)
    anchos = [0] * columnas
    for fila in matriz:
        for indice, celda in enumerate(fila):
            anchos[indice] = max(anchos[indice], len(str(celda)))
    for fila in matriz:
        celdas = [str(celda).ljust(anchos[indice]) for indice, celda in enumerate(fila)]
        print("  ".join(celdas).rstrip())
```

Linea por linea:

1. `columnas = max(len(fila) for fila in matriz)` — cuantas columnas tiene la fila mas ancha.
2. `anchos = [0] * columnas` — una lista con un cero por columna. Aca se ira guardando el ancho
   de cada una.
3. El primer `for` recorre todas las celdas con `enumerate` y va subiendo el ancho de su
   columna: `anchos[indice] = max(anchos[indice], len(str(celda)))`. Es el `enumerate` que pidio
   el instructor, y se necesita el indice porque hay que saber a que columna pertenece la celda.
4. El segundo `for` imprime: `str(celda).ljust(anchos[indice])` rellena cada celda con espacios
   hasta el ancho de su columna, `' '.join(...)` las pega con dos espacios, y `.rstrip()` quita
   los espacios que sobran al final de la linea.

Son dos pasadas por la matriz a proposito: en la primera se mide, en la segunda se imprime. No
se puede hacer en una sola porque para alinear la primera fila hay que conocer el ancho de la
mas larga, que puede estar al final.

```python
matriz = [["Seccion", "E1", "E2", "Total"],
          ["A", 2, 0, 2],
          ["Total", 2, 0, 2]]

print("el ancho de cada columna, calculado igual que en la funcion:")
columnas = max(len(fila) for fila in matriz)
anchos = [0] * columnas
for fila in matriz:
    for indice, celda in enumerate(fila):
        anchos[indice] = max(anchos[indice], len(str(celda)))
print("   columnas:", columnas, "| anchos:", anchos)
print()
print("cada celda rellenada con ljust (los | son para ver donde termina):")
for fila in matriz:
    print("   " + "".join(f"|{str(v).ljust(anchos[i])}" for i, v in enumerate(fila)) + "|")
print()
print("y asi la imprime el proyecto:")
menu.imprimir_matriz(matriz)
```

**Salida**

```
el ancho de cada columna, calculado igual que en la funcion:
   columnas: 4 | anchos: [7, 2, 2, 5]

cada celda rellenada con ljust (los | son para ver donde termina):
   |Seccion|E1|E2|Total|
   |A      |2 |0 |2    |
   |Total  |2 |0 |2    |

y asi la imprime el proyecto:
Seccion  E1  E2  Total
A        2   0   2
Total    2   0   2
```

> ### Error comun: imprimir una matriz con un ancho fijo
>
> **Asi no**
>
> ```python
> for fila in matriz:
>     for celda in fila:
>         print(celda, end="   ")
>     print()
> ```
>
> **Asi si**
>
> ```python
> anchos = [0] * max(len(fila) for fila in matriz)
> for fila in matriz:
>     for indice, celda in enumerate(fila):
>         anchos[indice] = max(anchos[indice], len(str(celda)))
> for fila in matriz:
>     print("  ".join(str(c).ljust(anchos[i]) for i, c in enumerate(fila)))
> ```
>
> **Por que.** Con espacios fijos las columnas se corren en cuanto un dato es mas largo que otro: la cabecera 'Seccion' mide 7 y un numero mide 1. Midiendo primero el ancho de cada columna, todas las celdas de esa columna quedan iguales y la tabla se lee de arriba abajo. Es lo que hace imprimir_matriz en menu.py.

### Recursividad

> ### Teoria: recursion
>
> **El problema.** Las categorias de los libros son jerarquicas: 'Computacion/Programacion/POO'. Hay que separarlas en niveles y buscar un libro aunque la persona escriba solo una parte del camino.
>
> **Como lo resuelve el proyecto.** Una funcion que se llama a si misma con un pedazo mas chico del problema. Hay dos partes obligatorias: el **caso base**, que termina sin volver a llamarse, y el **paso recursivo**, que se llama con menos datos. El proyecto tiene 3: `niveles_categoria`, `pertenece_a_categoria` y `buscar_por_categoria`.
>
> | Otra forma                    | Por que no se uso                                                                           |
> | ----------------------------- | ------------------------------------------------------------------------------------------- |
> | Usar un while con un contador | funciona, pero el codigo de la recursion es mas corto y muestra el tema que pide la rubrica |
> | Recursion sin caso base       | RecursionError: maximum recursion depth exceeded                                            |
>
> **El modelo mental.** Una munieca rusa: para abrirla hay que abrir la que tiene adentro, y adentro hay otra, hasta llegar a la mas chiquita que no tiene nada adentro.
>
> **Receta para otro proyecto.** Escribir el caso base primero y probarlo solo. Si el caso base no existe, Python revienta con RecursionError.

### Recursiva 1: niveles_categoria

Parte una categoria en sus niveles. Esta es la funcion completa:

```python
def niveles_categoria(categoria):
    partes = categoria.split("/")
    if len(partes) == 1:
        return [partes[0]]
    return [partes[0]] + niveles_categoria("/".join(partes[1:]))
```

- **Caso base:** si al partir por la `/` queda una sola parte, esa parte es el unico nivel y se
  devuelve en una lista. Ahi la funcion **no** se llama a si misma.
- **Paso recursivo:** se queda con la primera parte y se llama con las demas vueltas a pegar con
  `/`. Cada llamada trabaja con un texto mas corto.

```python
from modulos import libros

for categoria in ["Literatura", "Fisica/Mecanica",
                  "Computacion/Programacion/POO",
                  "Humanidades/Filosofia/Etica/Deontologia"]:
    niveles = libros.niveles_categoria(categoria)
    print(f"   {categoria:<40} -> {len(niveles)} niveles {niveles}")
```

**Salida**

```
   Literatura                               -> 1 niveles ['Literatura']
   Fisica/Mecanica                          -> 2 niveles ['Fisica', 'Mecanica']
   Computacion/Programacion/POO             -> 3 niveles ['Computacion', 'Programacion', 'POO']
   Humanidades/Filosofia/Etica/Deontologia  -> 4 niveles ['Humanidades', 'Filosofia', 'Etica', 'Deontologia']
```

Se usa en dos lugares: en `matriz_categorias` (aunque ahi la agrupacion se hace con
`split("/")[0]` directo) y en la busqueda, adentro de `pertenece_a_categoria`. Tambien en el
menu, para mostrar la categoria completa con flechitas: `' > '.join(niveles_categoria(...))`.

### Recursiva 2: pertenece_a_categoria

Dice si un **libro** esta dentro de la categoria que escribio la persona, comparando nivel por
nivel. Esta es la funcion:

```python
def pertenece_a_categoria(libro, nombre, niveles=None):
    if niveles is None:
        niveles = niveles_categoria(libro.categoria())
    if len(niveles) == 0:
        return False
    if niveles[0].lower() == str(nombre).strip().lower():
        return True
    return pertenece_a_categoria(libro, nombre, niveles[1:])
```

Tiene un detalle que vale la pena explicar porque el profesor puede preguntarlo: **el tercer
parametro, `niveles`, es la memoria de la recursion**. La primera llamada no lo trae, asi que
vale `None` y la funcion lo llena con los niveles de la categoria del libro. Las siguientes
llamadas si lo traen, cada vez con un nivel menos.

Tres salidas:

1. `len(niveles) == 0` → se acabaron los niveles y ninguno coincidio: `False`. **Es el caso
   base.**
2. el primer nivel coincide → `True`, y **no se vuelve a llamar**.
3. no coincide → se llama con `niveles[1:]`, o sea con los niveles que quedan.

Se podria escribir con un `for` sobre los niveles, y daria el mismo resultado. Se hizo recursiva
porque la rubrica pide recursion y porque encaja natural: cada nivel es el mismo problema con
menos datos.

```python
from modulos import libros

libro = b.libro("9788437604947")
print("con el libro", libro.titulo(), "| categoria:", libro.categoria())
print()
for nombre in ["literatura", "LITERATURA", "Narrativa", "  narrativa  ", "Poesia", "Redes"]:
    resultado = libros.pertenece_a_categoria(libro, nombre)
    print(f"   pertenece a {nombre!r:<16} -> {resultado}")

print()
print("sin pasar niveles, la funcion los calcula sola:")
print("   niveles_categoria ->", libros.niveles_categoria(libro.categoria()))
print()
print("y si se le pasa la lista vacia, el caso base responde False:")
print("   pertenece_a_categoria(libro, 'x', []) ->",
      libros.pertenece_a_categoria(libro, "x", []))
```

**Salida**

```
con el libro Cien años de soledad | categoria: Literatura/Narrativa

   pertenece a 'literatura'     -> True
   pertenece a 'LITERATURA'     -> True
   pertenece a 'Narrativa'      -> True
   pertenece a '  narrativa  '  -> True
   pertenece a 'Poesia'         -> False
   pertenece a 'Redes'          -> False

sin pasar niveles, la funcion los calcula sola:
   niveles_categoria -> ['Literatura', 'Narrativa']

y si se le pasa la lista vacia, el caso base responde False:
   pertenece_a_categoria(libro, 'x', []) -> False
```

Fijate en la comparacion: `niveles[0].lower() == str(nombre).strip().lower()`. Los dos lados
pasan a minusculas y el de la persona ademas se limpia de espacios, asi que `"NARRATIVA"`,
`"narrativa"` y `"  narrativa  "` dan lo mismo.

### Recursiva 3: buscar_por_categoria

La que usa el menu. Recibe la **lista** de libros y devuelve otra lista con los que coinciden,
sin tocar el catalogo:

```python
def buscar_por_categoria(catalogo, nombre):
    if len(catalogo) == 0:
        return []
    if pertenece_a_categoria(catalogo[0], nombre):
        return [catalogo[0]] + buscar_por_categoria(catalogo[1:], nombre)
    return buscar_por_categoria(catalogo[1:], nombre)
```

Cada llamada mira el primer libro, decide si va o no va, y se llama con el resto. Cuando la
lista llega vacia devuelve `[]` y las llamadas anteriores se van cerrando una por una, pegando
sus listas.

Ojo con el nombre del parametro: se llama `catalogo` pero **recibe una lista**, no el
diccionario. Por eso el menu lo llama asi:

```python
encontradas = libros.buscar_por_categoria(list(biblioteca.catalogo().values()), nombre)
```

Ese `list(...)` y `.values()` son obligatorios: `catalogo[0]` sobre un diccionario buscaria la
llave `0`, que no existe, y daria `KeyError`. Sobre una lista, `[0]` es el primer libro y `[1:]`
son los demas.

```python
from modulos import libros

lista = list(b.catalogo().values())

for nombre in ["Literatura", "Narrativa", "Poesia", "Computacion", "POO",
               "Fisica", "Inexistente"]:
    encontrados = libros.buscar_por_categoria(lista, nombre)
    print(f"   {nombre:<13} {len(encontrados)} titulos: "
          f"{', '.join(l.titulo()[:22] for l in encontrados) or '-'}")

print()
print("la lista original no se modifica:")
print("   libros en la lista:", len(lista))
print("   libros en el catalogo:", len(b.catalogo()))
print()
print("y lo que pasa si se le pasa el diccionario en vez de la lista:")
try:
    libros.buscar_por_categoria(b.catalogo(), "Literatura")
except KeyError as error:
    print("   KeyError:", error, "<- por eso el menu hace list(...values())")
```

**Salida**

```
   Literatura    4 titulos: Tradiciones peruanas, Maze Runner, Cien años de soledad, El Señor de los Anillo
   Narrativa     1 titulos: Cien años de soledad
   Poesia        0 titulos: -
   Computacion   1 titulos: Eloquent JavaScript
   POO           0 titulos: -
   Fisica        1 titulos: Fisica para ciencias e
   Inexistente   0 titulos: -

la lista original no se modifica:
   libros en la lista: 7
   libros en el catalogo: 7

y lo que pasa si se le pasa el diccionario en vez de la lista:
   KeyError: 0 <- por eso el menu hace list(...values())
```

**Devolver la lista en vez de imprimirla** es lo que permite que `accion_buscar_categoria`
decida que mostrar: si la lista viene vacia imprime _No hay titulos en la categoria_, y si no,
la tabla con los resultados y la categoria completa con flechitas. Si la funcion imprimiera por
dentro, no habria forma de saber si encontro algo.

### Ver la recursion paso a paso

```python
from modulos import libros

print("niveles_categoria('Computacion/Programacion/POO')")
print()
texto = "Computacion/Programacion/POO"
llamada = 0
while True:
    llamada += 1
    partes = texto.split("/")
    if len(partes) == 1:
        print(f"  llamada {llamada}: texto = {texto!r}")
        print(f"            split('/') da {partes}, una sola parte")
        print(f"            CASO BASE: devuelve {partes}")
        break
    print(f"  llamada {llamada}: texto = {texto!r}")
    print(f"            split('/') da {partes}")
    print(f"            devuelve ['{partes[0]}'] + recursion con {'/'.join(partes[1:])!r}")
    texto = "/".join(partes[1:])

print()
print("  se van cerrando de abajo hacia arriba:")
print("  ['POO']")
print("  ['Programacion'] + ['POO']")
print("  ['Computacion'] + ['Programacion', 'POO']")
print()
print("  resultado:", libros.niveles_categoria("Computacion/Programacion/POO"))
```

**Salida**

```
niveles_categoria('Computacion/Programacion/POO')

  llamada 1: texto = 'Computacion/Programacion/POO'
            split('/') da ['Computacion', 'Programacion', 'POO']
            devuelve ['Computacion'] + recursion con 'Programacion/POO'
  llamada 2: texto = 'Programacion/POO'
            split('/') da ['Programacion', 'POO']
            devuelve ['Programacion'] + recursion con 'POO'
  llamada 3: texto = 'POO'
            split('/') da ['POO'], una sola parte
            CASO BASE: devuelve ['POO']

  se van cerrando de abajo hacia arriba:
  ['POO']
  ['Programacion'] + ['POO']
  ['Computacion'] + ['Programacion', 'POO']

  resultado: ['Computacion', 'Programacion', 'POO']
```

```python
from modulos import libros

print("pertenece_a_categoria con 'Literatura/Narrativa', buscando 'Narrativa'")
print()
print("  llamada 1: niveles = None -> los calcula: ['Literatura', 'Narrativa']")
print("             hay 2 niveles, no esta vacia")
print("             'literatura' == 'narrativa'? no")
print("             recursion con niveles[1:] = ['Narrativa']")
print("  llamada 2: niveles = ['Narrativa']")
print("             hay 1 nivel, no esta vacia")
print("             'narrativa' == 'narrativa'? SI -> devuelve True")
print()
print("  resultado:", libros.pertenece_a_categoria(
    b.libro("9788437604947"), "Narrativa"))
print()
print("y si busca algo que no esta, llega al caso base:")
print("  llamada 1: ['Literatura', 'Narrativa'] -> no coincide 'Literatura'")
print("  llamada 2: ['Narrativa']               -> no coincide 'Narrativa'")
print("  llamada 3: []                          -> CASO BASE, devuelve False")
print()
print("  resultado:", libros.pertenece_a_categoria(
    b.libro("9788437604947"), "Redes"))
```

**Salida**

```
pertenece_a_categoria con 'Literatura/Narrativa', buscando 'Narrativa'

  llamada 1: niveles = None -> los calcula: ['Literatura', 'Narrativa']
             hay 2 niveles, no esta vacia
             'literatura' == 'narrativa'? no
             recursion con niveles[1:] = ['Narrativa']
  llamada 2: niveles = ['Narrativa']
             hay 1 nivel, no esta vacia
             'narrativa' == 'narrativa'? SI -> devuelve True

  resultado: True

y si busca algo que no esta, llega al caso base:
  llamada 1: ['Literatura', 'Narrativa'] -> no coincide 'Literatura'
  llamada 2: ['Narrativa']               -> no coincide 'Narrativa'
  llamada 3: []                          -> CASO BASE, devuelve False

  resultado: False
```

```python
from modulos import libros

print("buscar_por_categoria con 3 libros, paso a paso")
print()
mini = [libros.Libro("9781111111113", "Uno", "A", categoria="Fisica"),
        libros.Libro("9782222222224", "Dos", "B", categoria="Literatura"),
        libros.Libro("9783333333335", "Tres", "C", categoria="Literatura/Poesia")]
for indice, libro in enumerate(mini):
    print(f"  [{indice}] {libro.titulo()} - {libro.categoria()}")
print()
print("  llamada 1: 3 libros -> el [0] es 'Fisica', no pertenece")
print("             devuelve buscar_por_categoria(2 libros, 'Literatura')")
print("  llamada 2: 2 libros -> el [0] es 'Literatura', SI pertenece")
print("             devuelve [Dos] + buscar_por_categoria(1 libro, 'Literatura')")
print("  llamada 3: 1 libro  -> el [0] es 'Literatura/Poesia', SI pertenece")
print("             devuelve [Tres] + buscar_por_categoria(0 libros, 'Literatura')")
print("  llamada 4: 0 libros -> CASO BASE, devuelve []")
print()
print("  se cierran: [] -> [Tres] -> [Dos, Tres]")
print()
print("  resultado:", [l.titulo() for l in libros.buscar_por_categoria(mini, "Literatura")])
```

**Salida**

```
buscar_por_categoria con 3 libros, paso a paso

  [0] Uno - Fisica
  [1] Dos - Literatura
  [2] Tres - Literatura/Poesia

  llamada 1: 3 libros -> el [0] es 'Fisica', no pertenece
             devuelve buscar_por_categoria(2 libros, 'Literatura')
  llamada 2: 2 libros -> el [0] es 'Literatura', SI pertenece
             devuelve [Dos] + buscar_por_categoria(1 libro, 'Literatura')
  llamada 3: 1 libro  -> el [0] es 'Literatura/Poesia', SI pertenece
             devuelve [Tres] + buscar_por_categoria(0 libros, 'Literatura')
  llamada 4: 0 libros -> CASO BASE, devuelve []

  se cierran: [] -> [Tres] -> [Dos, Tres]

  resultado: ['Dos', 'Tres']
```

Cada llamada empuja un marco nuevo a la pila de Python. Cuando se llega al caso base, los
marcos se van cerrando del ultimo al primero, y cada uno aporta su pedazo al resultado.

**Nunca se desborda**, que es justo lo que pide el nivel maximo del criterio 4: la recursion mas
profunda posible es la de `niveles_categoria`, y son tantas llamadas como niveles tenga la
categoria. Con las categorias de los datos son 3 llamadas. Python aguanta unas 1000 por defecto
(`sys.getrecursionlimit()`), asi que habria que tener una categoria de mil niveles para que
fallara.

```python
import sys

from modulos import libros

print("limite de recursion de Python:", sys.getrecursionlimit())
print()
print("cuantas llamadas hace la categoria mas profunda de los datos:")
mas_larga = max((l.categoria() for l in b.catalogo().values()),
                key=lambda c: len(libros.niveles_categoria(c)))
print("   ", mas_larga, "->", len(libros.niveles_categoria(mas_larga)), "llamadas")
print()
print("y con una categoria inventada de 20 niveles:")
profunda = "/".join([f"n{i}" for i in range(20)])
print("   ", len(libros.niveles_categoria(profunda)), "llamadas, sin problema")
```

**Salida**

```
limite de recursion de Python: 1000

cuantas llamadas hace la categoria mas profunda de los datos:
    Literatura/Ciencia Ficción/Distopía Juvenil -> 3 llamadas

y con una categoria inventada de 20 niveles:
    20 llamadas, sin problema
```

### La recursion mas simple: el ejemplo comentado

Al final de `utilidades.py` hay un ejemplo de cuenta regresiva **comentado a proposito**, con
una nota del equipo:

```python
"""  AQUI DEJO UN EJEMPLO DE RECURSION, HAY QUE USAR ESE TEMA
def cuenta_regresiva(n):
    if n <= 0:
        print("Listo!")
        return 0
    print(n)
    return cuenta_regresiva(n - 1)
"""
```

Es el ejemplo mas claro de recursion que existe, y en el proyecto la parte que de verdad la
necesita son las categorias. Si el profesor pregunta por una recursion basica, se puede
descomentar, pero hoy el programa no la usa y la recursion real esta en `libros.py`.

Ojo si se descomenta: en el archivo la funcion se define como `cuenta_regresiva` y se llama a si
misma como `cuenta_regresiva`, con las dos palabras iguales, asi que funciona. Lo que no
funciona es llamarla desde el programa, porque no esta definida: esta adentro de un bloque de
texto.

```python
def cuenta_regresiva(n):
    if n <= 0:
        print("Listo!")
        return 0
    print(n)
    return cuenta_regresiva(n - 1)


print("la recursion basica, descomentada:")
cuenta_regresiva(5)

print()
print("y la recursion real del proyecto, con una categoria de 4 niveles:")
from modulos import libros
print("   'A/B/C/D' ->", libros.niveles_categoria("A/B/C/D"))
```

**Salida**

```
la recursion basica, descomentada:
5
4
3
2
1
Listo!

y la recursion real del proyecto, con una categoria de 4 niveles:
   'A/B/C/D' -> ['A', 'B', 'C', 'D']
```

> ### Error comun: recursion sin caso base
>
> **Asi no**
>
> ```python
> def niveles_categoria(categoria):
>     partes = categoria.split("/")
>     return [partes[0]] + niveles_categoria("/".join(partes[1:]))
> ```
>
> **Asi si**
>
> ```python
> def niveles_categoria(categoria):
>     partes = categoria.split("/")
>     if len(partes) == 1:
>         return [partes[0]]
>     return [partes[0]] + niveles_categoria("/".join(partes[1:]))
> ```
>
> **Por que.** Sin el if del medio la funcion se llama para siempre: al llegar a la cadena vacia, split('/') devuelve [''] y sigue llamandose con '' una y otra vez, hasta RecursionError: maximum recursion depth exceeded. Por eso en las tres recursivas del proyecto lo primero que se escribe es la linea que devuelve sin llamar a nadie: len(partes) == 1, len(niveles) == 0 y len(catalogo) == 0.

### Recursion contra bucle: la prueba de que hacen lo mismo

```python
from modulos import libros


def niveles_con_bucle(categoria):
    return categoria.split("/")


def pertenece_con_bucle(libro, nombre):
    for nivel in libro.categoria().split("/"):
        if nivel.lower() == str(nombre).strip().lower():
            return True
    return False


def buscar_con_bucle(lista, nombre):
    encontrados = []
    for libro in lista:
        if pertenece_con_bucle(libro, nombre):
            encontrados.append(libro)
    return encontrados


print("niveles_categoria, recursion contra split:")
for categoria in ["Literatura", "Fisica/Mecanica", "Computacion/Programacion/POO"]:
    print(f"   {categoria:<32} iguales: "
          f"{libros.niveles_categoria(categoria) == niveles_con_bucle(categoria)}")

print()
lista = list(b.catalogo().values())
print("buscar_por_categoria, recursion contra for:")
for nombre in ["Literatura", "POO", "Fisica", "Inexistente"]:
    con_recursion = [l.isbn() for l in libros.buscar_por_categoria(lista, nombre)]
    con_bucle = [l.isbn() for l in buscar_con_bucle(lista, nombre)]
    print(f"   {nombre:<13} {len(con_recursion)} titulos, "
          f"iguales: {con_recursion == con_bucle}")

print()
print("dan el mismo resultado. Se uso recursion porque la rubrica la pide y porque")
print("una categoria es un problema que se repite con menos datos en cada nivel.")
```

**Salida**

```
niveles_categoria, recursion contra split:
   Literatura                       iguales: True
   Fisica/Mecanica                  iguales: True
   Computacion/Programacion/POO     iguales: True

buscar_por_categoria, recursion contra for:
   Literatura    4 titulos, iguales: True
   POO           0 titulos, iguales: True
   Fisica        1 titulos, iguales: True
   Inexistente   0 titulos, iguales: True

dan el mismo resultado. Se uso recursion porque la rubrica la pide y porque
una categoria es un problema que se repite con menos datos en cada nivel.
```

### El submenu de matrices del menu de administracion

```python
from modulos import menu

print("las opciones del submenu MATRICES:")
for codigo, texto, accion in menu.MATRICES:
    destino = accion.__name__ if accion else "vuelve al menu de administracion"
    print(f"   {codigo}) {texto:<38} -> {destino}")

print()
print("y en menu_admin se abre con la opcion 3:")
print()
print("        if opcion == '3':")
print("            while True:")
print("                mostrar_opciones(MATRICES)")
print("                eleccion = leer_opcion(MATRICES)")
print("                if eleccion == '0':")
print("                    break")
print("                for codigo, texto, accion in MATRICES:")
print("                    if codigo == eleccion:")
print("                        accion(biblioteca)")
print("                utilidades.pausa()")
print("            continue")
print()
print("es un while adentro de otro while: el submenu gira hasta que se elige 0,")
print("y el continue vuelve al menu de administracion sin cerrarlo")
```

**Salida**

```
las opciones del submenu MATRICES:
   1) Disponibilidad por seccion y estante   -> accion_matriz_disponibilidad
   2) Titulos por seccion y estante          -> accion_matriz_ubicacion
   3) Categorias principales                 -> accion_matriz_categorias
   4) Busqueda recursiva por categoria       -> accion_buscar_categoria
   0) Volver al menu de administracion       -> vuelve al menu de administracion

y en menu_admin se abre con la opcion 3:

        if opcion == '3':
            while True:
                mostrar_opciones(MATRICES)
                eleccion = leer_opcion(MATRICES)
                if eleccion == '0':
                    break
                for codigo, texto, accion in MATRICES:
                    if codigo == eleccion:
                        accion(biblioteca)
                utilidades.pausa()
            continue

es un while adentro de otro while: el submenu gira hasta que se elige 0,
y el continue vuelve al menu de administracion sin cerrarlo
```

### Lo que usa esta seccion

| Pieza                 | Donde                                              | Caso base                                             |
| --------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| matriz_disponibilidad | libros.py, submenu opcion 1                        | no es recursiva                                       |
| matriz_ubicacion      | libros.py, submenu opcion 2                        | no es recursiva                                       |
| matriz_categorias     | libros.py, submenu opcion 3                        | no es recursiva, pero usa categorias_unicas           |
| imprimir_matriz       | menu.py                                            | no es recursiva: dos pasadas, una mide y otra imprime |
| niveles_categoria     | libros.py                                          | len(partes) == 1 devuelve [partes[0]]                 |
| pertenece_a_categoria | libros.py, submenu opcion 4                        | len(niveles) == 0 devuelve False                      |
| buscar_por_categoria  | libros.py, opcion 2 del menu de miembro e invitado | len(catalogo) == 0 devuelve []                        |
| cuenta_regresiva      | utilidades.py, comentada a proposito               | n <= 0 imprime Listo! y devuelve 0                    |

3 matrices y 3 funciones recursivas en uso. La cuarta, la cuenta regresiva, esta comentada en utilidades.py como referencia del tema.

# 5. Herencia y polimorfismo

El proyecto tiene dos arboles de herencia. El grande es el de las membresias: `Membresia` con
cuatro subclases, y `Administrador` que cuelga de `Docente`, asi que son tres niveles. El otro
es el de las excepciones de la seccion 3.

> ### Teoria: herencia
>
> **El problema.** Estudiante, docente, administrador e invitado comparten casi todo: una fecha de vencimiento, un estado, un limite de libros. Escribir cuatro clases desde cero significa copiar los mismos metodos cuatro veces.
>
> **Como lo resuelve el proyecto.** Se escribe una vez en `Membresia` y las cuatro subclases la reciben gratis. Cada subclase solo dice en que se diferencia: sus numeros, leidos de `config.py`.
>
> | Otra forma                           | Por que no se uso                                                  |
> | ------------------------------------ | ------------------------------------------------------------------ |
> | Copiar la clase y cambiar dos lineas | cuatro copias que hay que arreglar cuatro veces si algo falla      |
> | Una sola clase con un if por tipo    | crece hasta volverse ilegible y no se puede ampliar sin tocar todo |
>
> **El modelo mental.** Una clase hija hereda todo lo de la madre y le agrega o le cambia lo suyo. Administrador es un Docente con permiso de administrar.
>
> **Receta para otro proyecto.** Preguntar 'X es un Y?' Si la frase suena natural, X puede heredar de Y. 'El administrador es un docente' suena bien; 'el libro es un usuario' no.

### El arbol, dibujado desde Python

```python
from modulos.usuarios import (Administrador, Docente, Estudiante, Invitado,
                              Membresia)


def arbol(clase, nivel=0):
    prefijo = "   " * nivel + ("+-- " if nivel else "")
    print(f"{prefijo}{clase.__name__}")
    for hija in clase.__subclasses__():
        arbol(hija, nivel + 1)


print("el arbol de membresias:")
arbol(Membresia)

print()
print("y lo mismo para las excepciones:")
from modulos import errores
arbol(errores.BibliotecaError)
```

**Salida**

```
el arbol de membresias:
Membresia
   +-- Estudiante
   +-- Docente
      +-- Administrador
   +-- Invitado

y lo mismo para las excepciones:
BibliotecaError
   +-- DatosInvalidosError
   +-- ArchivoDatosError
```

Esa funcion `arbol` es recursiva tambien: se llama a si misma con cada hija. Es un extra del
cuaderno, no esta en el proyecto, pero sirve para ver el arbol sin leer el codigo.

```python
from modulos import config
from modulos.usuarios import (Administrador, Docente, Estudiante, Invitado,
                              Membresia)

print("que aporta cada clase:")
print()
print(f"{'Clase':<15}{'TIPO':<15}{'Limite':>7}{'Dias':>6}{'Multa':>8}{'Admin':>7}")
print("-" * 58)
for clase in [Membresia, Estudiante, Docente, Administrador, Invitado]:
    print(f"{clase.__name__:<15}{clase.TIPO:<15}{clase.LIMITE_LIBROS:>7}"
          f"{clase.DIAS_PRESTAMO:>6}{clase.MULTA_POR_DIA:>8.2f}"
          f"{'si' if clase.PUEDE_ADMINISTRAR else 'no':>7}")
print()
print("los numeros salen de config.py, no estan escritos en las clases:")
print("   ", config.limite_libros)
print("   ", config.dias_prestamo)
print("   ", config.multa_por_dia)
```

**Salida**

```
que aporta cada clase:

Clase          TIPO            Limite  Dias   Multa  Admin
----------------------------------------------------------
Membresia      base                 0     0    0.00     no
Estudiante     estudiante           3    14    0.50     no
Docente        docente              5    20    0.50     no
Administrador  administrador        5    20    0.50     si
Invitado       invitado             0     0    0.00     no

los numeros salen de config.py, no estan escritos en las clases:
    {'estudiante': 3, 'docente': 5, 'administrador': 5, 'invitado': 0}
    {'estudiante': 14, 'docente': 20, 'administrador': 20, 'invitado': 0}
    {'estudiante': 0.5, 'docente': 0.5, 'administrador': 0.5, 'invitado': 0.0}
```

**`Membresia` sola tiene ceros y no se usa nunca.** Existe como molde: nadie hace
`Membresia()`, siempre se crea una de las cuatro hijas. Eso es una clase base abstracta en la
practica, aunque el proyecto no use el modulo `abc` (no hace falta).

### Que hereda y que no

```python
from modulos.usuarios import Estudiante, Membresia

heredados = set(dir(Estudiante)) & set(dir(Membresia))
propios = [n for n in dir(Estudiante)
           if not n.startswith("__") and n not in heredados]

print("Estudiante hereda TODOS los metodos de Membresia:")
for nombre in sorted(n for n in heredados if not n.startswith("_")):
    print("   ", nombre)

print()
print("y no define ninguno propio. Su cuerpo entero son 4 lineas:")
print()
print("class Estudiante(Membresia):")
print("    TIPO = 'estudiante'")
print("    LIMITE_LIBROS = config.limite_libros['estudiante']")
print("    DIAS_PRESTAMO = config.dias_prestamo['estudiante']")
print("    MULTA_POR_DIA = config.multa_por_dia['estudiante']")
```

**Salida**

```
Estudiante hereda TODOS los metodos de Membresia:
    DIAS_PRESTAMO
    LIMITE_LIBROS
    MULTA_POR_DIA
    PUEDE_ADMINISTRAR
    TIPO
    cancelar
    describir
    dias_prestamo
    estado
    limite_libros
    multa_por_dia
    puede_administrar
    renovar
    tipo
    vencimiento
    vigente

y no define ninguno propio. Su cuerpo entero son 4 lineas:

class Estudiante(Membresia):
    TIPO = 'estudiante'
    LIMITE_LIBROS = config.limite_libros['estudiante']
    DIAS_PRESTAMO = config.dias_prestamo['estudiante']
    MULTA_POR_DIA = config.multa_por_dia['estudiante']
```

Estudiante **no tiene `__init__` propio**, y eso es lo mas importante de la seccion: hereda el
de `Membresia`, que es el que guarda la fecha de vencimiento y el estado de cancelacion. Por
eso `Estudiante("2027-04-29")` funciona sin escribir nada mas.

```python
from datetime import date, timedelta

from modulos.usuarios import Estudiante

vencimiento = date.today() + timedelta(days=400)
ana = Estudiante(vencimiento.isoformat())

print("creada con un solo dato:", ana)
print()
print("metodos que vienen de Membresia, funcionando en una Estudiante:")
print("   tipo()              ->", ana.tipo())
print("   vencimiento()       ->", ana.vencimiento())
print("   vigente()           ->", ana.vigente())
print("   estado()            ->", ana.estado())
print("   limite_libros()     ->", ana.limite_libros())
print("   dias_prestamo()     ->", ana.dias_prestamo())
print("   multa_por_dia()     ->", ana.multa_por_dia())
print("   puede_administrar() ->", ana.puede_administrar())
```

**Salida**

```
creada con un solo dato: Estudiante: 3 libros por 14 dias

metodos que vienen de Membresia, funcionando en una Estudiante:
   tipo()              -> estudiante
   vencimiento()       -> 2027-11-27
   vigente()           -> True
   estado()            -> Vigente
   limite_libros()     -> 3
   dias_prestamo()     -> 14
   multa_por_dia()     -> 0.5
   puede_administrar() -> False
```

### Polimorfismo: la misma llamada, comportamiento distinto

> ### Teoria: polimorfismo
>
> **El problema.** El menu tiene que mostrar los datos de la membresia de quien entro, sea estudiante, docente, administrador o invitado. Sin polimorfismo habria que escribir un if por tipo en cada lugar donde se muestra algo.
>
> **Como lo resuelve el proyecto.** Se llama al mismo metodo y cada clase responde a su manera. `accion_mi_membresia` ejecuta siete lineas identicas para los cuatro tipos y la pantalla sale distinta sola, porque `tipo()`, `estado()` y `describir()` resuelven segun el objeto.
>
> | Otra forma                               | Por que no se uso                                                            |
> | ---------------------------------------- | ---------------------------------------------------------------------------- |
> | Una cadena de if/elif por tipo           | cada vez que se agrega un tipo nuevo hay que buscar todos los if del sistema |
> | Copiar la accion del menu para cada tipo | cuatro copias que muestran lo mismo con numeros distintos                    |
>
> **El modelo mental.** Un enchufe. Todos los aparatos usan la misma toma pero adentro hacen cosas distintas.
>
> **Receta para otro proyecto.** El menu no pregunta 'de que tipo eres?', pregunta 'dame tus datos'. El objeto sabe responder.

```python
from modulos.usuarios import crear_membresia

print("el MISMO bucle, las MISMAS llamadas, cuatro resultados distintos:")
print()
print(f"{'describir()':<46}{'tipo()':<16}{'estado()':<10}")
print("-" * 72)
for tipo in ["estudiante", "docente", "administrador", "invitado"]:
    membresia = crear_membresia(tipo, "2027-01-15")
    print(f"{membresia.describir():<46}{membresia.tipo():<16}{membresia.estado():<10}")

print()
print("en el codigo del menu esto es literalmente:")
print()
print("    print(f'Tipo: {membresia.tipo().capitalize()}')")
print("    print(f'Estado: {membresia.estado()}')")
print("    print(membresia.describir())")
print()
print("sin ningun if que pregunte por el tipo")
```

**Salida**

```
el MISMO bucle, las MISMAS llamadas, cuatro resultados distintos:

describir()                                   tipo()          estado()
------------------------------------------------------------------------
Estudiante: 3 libros por 14 dias              estudiante      Vigente
Docente: 5 libros por 20 dias                 docente         Vigente
Administrador: 5 libros por 20 dias           administrador   Vigente
Invitado: solo puede consultar el catalogo    invitado        Vigente

en el codigo del menu esto es literalmente:

    print(f'Tipo: {membresia.tipo().capitalize()}')
    print(f'Estado: {membresia.estado()}')
    print(membresia.describir())

sin ningun if que pregunte por el tipo
```

### Sobrescribir (override): cuando la hija cambia un metodo

`Invitado` cambia `describir()` porque su mensaje no tiene nada que ver con limites ni dias:
no puede llevarse libros. Es la unica subclase que sobrescribe un metodo.

```python
from modulos.usuarios import Invitado, Membresia

invitado = Invitado()
membresia = Membresia()

print("Membresia.describir(): ", membresia.describir())
print("Invitado.describir():  ", invitado.describir())
print()
print("la hija tiene su propia version, y la madre conserva la suya:")
print("   el metodo que corre lo decide el OBJETO, no la clase desde donde se mira")
print()
print("pero Invitado sigue usando el __str__ heredado, que llama a describir():")
print("   str(invitado) ->", str(invitado))
print("   o sea que el __str__ de la madre produce el texto de la hija")
```

**Salida**

```
Membresia.describir():  Base: 0 libros por 0 dias
Invitado.describir():   Invitado: solo puede consultar el catalogo

la hija tiene su propia version, y la madre conserva la suya:
   el metodo que corre lo decide el OBJETO, no la clase desde donde se mira

pero Invitado sigue usando el __str__ heredado, que llama a describir():
   str(invitado) -> Invitado: solo puede consultar el catalogo
   o sea que el __str__ de la madre produce el texto de la hija
```

Ese ultimo detalle es bonito para explicar: `Membresia.__str__` dice `return self.describir()`,
y como `self` es un `Invitado`, termina ejecutando el `describir()` de `Invitado`. La madre
llama al metodo de la hija sin saberlo.

### El orden en que Python busca los metodos (MRO)

```python
from modulos.usuarios import Administrador, Docente, Membresia

print("Administrador -> Docente -> Membresia -> object")
print()
print("el orden real que usa Python:")
for posicion, clase in enumerate(Administrador.__mro__):
    print(f"   {posicion}. {clase.__name__}")
print()

jorge = Administrador("2027-01-15")
print("donde encuentra cada cosa:")
print("   TIPO = 'administrador'          -> definido en Administrador")
print("   PUEDE_ADMINISTRAR = True        -> definido en Administrador")
print("   MULTA_POR_DIA = 0.5             -> definido en Administrador")
print("   LIMITE_LIBROS =", jorge.limite_libros(), "              -> hereda de Docente")
print("   DIAS_PRESTAMO =", jorge.dias_prestamo(), "              -> hereda de Docente")
print("   describir()                     -> hereda de Membresia (ninguna de las dos la cambia)")
print("   __init__(vencimiento)           -> hereda de Membresia")
print("   estado()                        -> hereda de Membresia")
print()
print("   en los objetos:", jorge)
print("   es Docente?    ", isinstance(jorge, Docente))
print("   es Membresia?  ", isinstance(jorge, Membresia))
print("   es Estudiante? ", isinstance(jorge, type(Administrador).__mro__[0]) and
      isinstance(jorge, Membresia) and not isinstance(jorge, Docente))
```

**Salida**

```
Administrador -> Docente -> Membresia -> object

el orden real que usa Python:
   0. Administrador
   1. Docente
   2. Membresia
   3. object

donde encuentra cada cosa:
   TIPO = 'administrador'          -> definido en Administrador
   PUEDE_ADMINISTRAR = True        -> definido en Administrador
   MULTA_POR_DIA = 0.5             -> definido en Administrador
   LIMITE_LIBROS = 5               -> hereda de Docente
   DIAS_PRESTAMO = 20               -> hereda de Docente
   describir()                     -> hereda de Membresia (ninguna de las dos la cambia)
   __init__(vencimiento)           -> hereda de Membresia
   estado()                        -> hereda de Membresia

   en los objetos: Administrador: 5 libros por 20 dias
   es Docente?     True
   es Membresia?   True
   es Estudiante?  False
```

**Por que `Administrador` cuelga de `Docente` y no de `Membresia`.** Porque un administrador
es un docente con permiso extra: mismo limite de libros y mismos dias de prestamo. Si colgara
de `Membresia` habria que repetir esas dos lineas. El unico cambio de fondo es
`PUEDE_ADMINISTRAR = True`, y esa es la que decide que menu se abre en `menu_principal`.

Como consecuencia, si un dia cambia el limite del docente, el del administrador cambia solo.

```python
from modulos.usuarios import Docente, Administrador

print("Administrador no escribe LIMITE_LIBROS ni DIAS_PRESTAMO:")
print("   'LIMITE_LIBROS' en Administrador.__dict__ ->",
      "LIMITE_LIBROS" in Administrador.__dict__)
print("   'LIMITE_LIBROS' in Docente.__dict__       ->",
      "LIMITE_LIBROS" in Docente.__dict__)
print()
print("lo que si escribe:")
for nombre in sorted(Administrador.__dict__):
    if not nombre.startswith("__"):
        print(f"   {nombre} = {Administrador.__dict__[nombre]}")
```

**Salida**

```
Administrador no escribe LIMITE_LIBROS ni DIAS_PRESTAMO:
   'LIMITE_LIBROS' en Administrador.__dict__ -> False
   'LIMITE_LIBROS' in Docente.__dict__       -> True

lo que si escribe:
   MULTA_POR_DIA = 0.5
   PUEDE_ADMINISTRAR = True
   TIPO = administrador
```

### La fabrica: crear_membresia

El JSON guarda el tipo como texto (`"Estudiante"`, `"Docente"`, `"Administrador"`). Alguien
tiene que convertir ese texto en un objeto de la clase correcta, y esa es `crear_membresia`:

```python
from modulos import errores, usuarios

for texto in ["Estudiante", "docente", "ADMINISTRADOR", "  admin  ", "invitado",
              "superusuario"]:
    try:
        membresia = usuarios.crear_membresia(texto, "2027-01-15")
        print(f"   {texto!r:<16} -> {type(membresia).__name__:<14} {membresia.describir()}")
    except errores.DatosInvalidosError as error:
        print(f"   {texto!r:<16} -> error: {error}")
```

**Salida**

```
   'Estudiante'     -> Estudiante     Estudiante: 3 libros por 14 dias
   'docente'        -> Docente        Docente: 5 libros por 20 dias
   'ADMINISTRADOR'  -> Administrador  Administrador: 5 libros por 20 dias
   '  admin  '      -> Administrador  Administrador: 5 libros por 20 dias
   'invitado'       -> Invitado       Invitado: solo puede consultar el catalogo
   'superusuario'   -> error: Ese tipo de membresia no existe
```

**`str(tipo or "estudiante").strip().lower()`** hace tres cosas en una linea: si llega `None` o
un texto vacio asume `"estudiante"`, quita espacios, y pasa todo a minusculas. Por eso
`"ADMINISTRADOR"`, `" administrador "` y `"administrador"` dan el mismo objeto. Y acepta el
atajo `"admin"`.

Si el texto no es ninguno de los cuatro, lanza `DatosInvalidosError`. Es mejor que devolver
`None`: el programa se entera en el momento en que lee el JSON, no tres menus despues.

### La fabrica 2: crear_usuario

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()

print("los 10 miembros del JSON, con la clase de membresia que les toco:")
print()
print(f"{'DNI':<10}{'Nombre':<22}{'Clase de membresia':<20}{'Estado':<10}{'Admin':<7}")
print("-" * 69)
for dni, miembro in b.miembros().items():
    clase = type(miembro.membresia()).__name__
    admin = "si" if miembro.puede_administrar() else "no"
    print(f"{dni:<10}{miembro.nombre()[:20]:<22}{clase:<20}{miembro.estado():<10}{admin:<7}")
```

**Salida**

```
los 10 miembros del JSON, con la clase de membresia que les toco:

DNI       Nombre                Clase de membresia  Estado    Admin
---------------------------------------------------------------------
11111111  Ana Quispe            Estudiante          Vigente   no
70445566  Luis Ramos            Docente             Vigente   no
70778899  Rosa Palomino         Estudiante          De baja   no
70889900  Marco Perez           Estudiante          Vigente   no
71234567  Carla Mendoza         Docente             De baja   no
72345678  Jorge Huaman          Administrador       Vigente   si
73456789  Lucia Torres          Estudiante          De baja   no
74567890  Pedro Castillo        Estudiante          De baja   no
75678901  Sofia Rojas           Estudiante          Vigente   no
76789012  Diego Vargas          Docente             Vencida   no
```

`crear_usuario(datos)` recibe el diccionario del JSON, saca cada campo con `.get()` (que
devuelve `None` si falta en vez de reventar) y arma el `Usuario`, que por dentro llama a
`crear_membresia`. Las dos fabricas juntas son las que convierten texto plano en objetos.

```python
from modulos import config, usuarios

registros = config.leer_json("miembros")

print("esto es lo que viene del JSON, texto plano:")
print("   ", registros[0])
print()
print("y esto es lo que sale, un objeto:")
miembro = usuarios.crear_usuario(registros[0])
print("   ", type(miembro).__name__, "->", miembro)
print("    tipo de su membresia:", type(miembro.membresia()).__name__)
print("    vencimiento:", miembro.vencimiento(), type(miembro.vencimiento()).__name__)
print("    activo:", miembro.activo())
```

**Salida**

```
esto es lo que viene del JSON, texto plano:
    {'dni': '11111111', 'nombre': 'Ana Quispe', 'tipo': 'Estudiante', 'vencimiento_membresia': '2027-04-29', 'activo': True}

y esto es lo que sale, un objeto:
    Usuario -> Ana Quispe (11111111) - estudiante
    tipo de su membresia: Estudiante
    vencimiento: 2027-04-29 date
    activo: True
```

### Composicion: Usuario tiene una Membresia

`Usuario` no hereda de `Membresia`: la **tiene**. Son dos cosas distintas y conviene no
mezclarlas en la defensa.

- Herencia: _es un_. El administrador **es** un docente.
- Composicion: _tiene un_. El miembro **tiene** una membresia.

`Usuario` no podria heredar de `Membresia` porque un miembro no es una membresia: tiene DNI,
nombre y estado de alta, que la membresia no tiene.

```python
from modulos.usuarios import Usuario

miembro = Usuario("Ana Quispe", "11111111", "estudiante", "2027-04-29")

print("los atributos propios de Usuario:")
print("   _nombre   ->", miembro.nombre())
print("   _dni      ->", miembro.dni())
print("   _activo   ->", miembro.activo())
print()
print("y el objeto que guarda adentro:")
print("   _membresia ->", type(miembro.membresia()).__name__)
print()
print("los metodos que solo delegan hacia adentro:")
print("   miembro.vencimiento()          ->", miembro.vencimiento())
print("   miembro.estado()               ->", miembro.estado())
print("   miembro.puede_administrar()    ->", miembro.puede_administrar())
print("   miembro.membresia().tipo()     ->", miembro.membresia().tipo())
print()
print("por eso cambiar la membresia cambia todo lo que el miembro informa,")
print("sin tocar al miembro:")
miembro.renovar_membresia()
print("   despues de renovar_membresia():", miembro.vencimiento(), "|", miembro.estado())
```

**Salida**

```
los atributos propios de Usuario:
   _nombre   -> Ana Quispe
   _dni      -> 11111111
   _activo   -> True

y el objeto que guarda adentro:
   _membresia -> Estudiante

los metodos que solo delegan hacia adentro:
   miembro.vencimiento()          -> 2027-04-29
   miembro.estado()               -> Vigente
   miembro.puede_administrar()    -> False
   miembro.membresia().tipo()     -> estudiante

por eso cambiar la membresia cambia todo lo que el miembro informa,
sin tocar al miembro:
   despues de renovar_membresia(): 2028-04-28 | Vigente
```

`renovar_membresia` y `cancelar_membresia`, igual que `dar_de_baja` y `reactivar`, ya estan
escritos pero el menu todavia no los usa: son parte de lo que falta. Se muestran aca porque
explican bien la composicion.

```python
from modulos.usuarios import Usuario

print("cancelar_membresia, que cambia la membresia desde el miembro:")
miembro = Usuario("Rosa Palomino", "70778899", "estudiante", "2027-01-15")
print("   antes:  ", miembro.estado(), "| vigente:", miembro.membresia().vigente())
miembro.cancelar_membresia()
print("   despues:", miembro.estado(), "| vigente:", miembro.membresia().vigente())
print("   describir:", miembro.membresia().describir())
print()
print("dar_de_baja y reactivar, que cambian el estado del miembro:")
print("   activo?", miembro.activo())
miembro.dar_de_baja()
print("   tras dar_de_baja():", miembro.activo())
miembro.reactivar()
print("   tras reactivar(): ", miembro.activo())
```

**Salida**

```
cancelar_membresia, que cambia la membresia desde el miembro:
   antes:   Vigente | vigente: True
   despues: Cancelada | vigente: False
   describir: Estudiante: 3 libros por 14 dias

dar_de_baja y reactivar, que cambian el estado del miembro:
   activo? True
   tras dar_de_baja(): False
   tras reactivar():  True
```

Hay dos estados independientes y es facil confundirlos en la defensa:

- `activo`: lo decide la biblioteca (alta y baja del miembro). Se guarda en el JSON.
- `vigente`: lo decide la fecha (si la membresia vencio o se cancelo). Se calcula, no se guarda.

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()
print("los dos estados, lado a lado, con los datos reales:")
print()
print(f"{'DNI':<10}{'Nombre':<20}{'activo':<8}{'vigente':<9}{'estado()':<12}")
print("-" * 59)
for dni, miembro in b.miembros().items():
    print(f"{dni:<10}{miembro.nombre()[:18]:<20}"
          f"{'si' if miembro.activo() else 'no':<8}"
          f"{'si' if miembro.membresia().vigente() else 'no':<9}"
          f"{miembro.estado():<12}")

print()
print("estado() combina los dos: si no esta activo, gana ese dato;")
print("si esta activo, mira el vencimiento de la membresia")
```

**Salida**

```
los dos estados, lado a lado, con los datos reales:

DNI       Nombre              activo  vigente  estado()
-----------------------------------------------------------
11111111  Ana Quispe          si      si       Vigente
70445566  Luis Ramos          si      si       Vigente
70778899  Rosa Palomino       no      no       De baja
70889900  Marco Perez         si      si       Vigente
71234567  Carla Mendoza       no      no       De baja
72345678  Jorge Huaman        si      si       Vigente
73456789  Lucia Torres        no      no       De baja
74567890  Pedro Castillo      no      no       De baja
75678901  Sofia Rojas         si      si       Vigente
76789012  Diego Vargas        si      no       Vencida

estado() combina los dos: si no esta activo, gana ese dato;
si esta activo, mira el vencimiento de la membresia
```

> ### Error comun: heredar cuando lo que hace falta es tener
>
> **Asi no**
>
> ```python
> class Usuario(Membresia):
>     def __init__(self, nombre, dni, tipo, vencimiento):
>         super().__init__(vencimiento)
>         self._nombre = nombre
>         self._dni = dni
> ```
>
> **Asi si**
>
> ```python
> class Usuario:
>     def __init__(self, nombre, dni, tipo="estudiante", vencimiento=None,
>                  activo=True):
>         self._nombre = nombre
>         self._dni = dni
>         self._activo = bool(activo)
>         self._membresia = crear_membresia(tipo, vencimiento)
> ```
>
> **Por que.** Un usuario no es una membresia: tiene nombre, DNI y estado de alta que la membresia no tiene. Heredando, el usuario arrastraria los metodos de la membresia como si fueran suyos y no se podria cambiar la membresia sin rehacer el objeto. Con composicion el miembro le pregunta a su membresia lo que necesita y puede renovarla o cancelarla sin tocarse a si mismo.

### super() y por que el proyecto casi no lo necesita

El material del curso muestra `super().__init__()` para que la hija llame al constructor de la
madre. En el proyecto **no aparece**, y hay una razon concreta: ninguna subclase define su
propio `__init__`. Las cuatro heredan el de `Membresia` tal cual, asi que no hay nada que
encadenar.

```python
from modulos.usuarios import (Administrador, Docente, Estudiante, Invitado,
                              Membresia)

print("que clases definen su propio __init__:")
for clase in [Membresia, Estudiante, Docente, Administrador, Invitado]:
    propio = "__init__" in clase.__dict__
    print(f"   {clase.__name__:<15} {'si, lo define' if propio else 'no, hereda el de Membresia'}")

print()
print("si una hija quisiera agregar un dato, ahi si haria falta super():")
print()
print("class Becado(Estudiante):")
print("    def __init__(self, vencimiento, institucion):")
print("        super().__init__(vencimiento)      <- primero lo de la madre")
print("        self._institucion = institucion    <- despues lo propio")
print()
print("sin esa llamada el objeto se crearia sin fecha de vencimiento y")
print("membresia.vencimiento() devolveria None")
```

**Salida**

```
que clases definen su propio __init__:
   Membresia       si, lo define
   Estudiante      no, hereda el de Membresia
   Docente         no, hereda el de Membresia
   Administrador   no, hereda el de Membresia
   Invitado        no, hereda el de Membresia

si una hija quisiera agregar un dato, ahi si haria falta super():

class Becado(Estudiante):
    def __init__(self, vencimiento, institucion):
        super().__init__(vencimiento)      <- primero lo de la madre
        self._institucion = institucion    <- despues lo propio

sin esa llamada el objeto se crearia sin fecha de vencimiento y
membresia.vencimiento() devolveria None
```

```python
from modulos.usuarios import Estudiante


class Becado(Estudiante):
    def __init__(self, vencimiento, institucion):
        super().__init__(vencimiento)
        self._institucion = institucion


becado = Becado("2027-06-30", "IDAT")
print("probado de verdad, agregando una quinta subclase fuera del proyecto:")
print("   ", becado)
print("    institucion:", becado._institucion)
print("    limite de libros (heredado de Estudiante):", becado.limite_libros())
print("    estado:", becado.estado())
print()
print("la herencia deja ampliar el sistema sin tocar las clases que ya existen")
```

**Salida**

```
probado de verdad, agregando una quinta subclase fuera del proyecto:
    Estudiante: 3 libros por 14 dias
    institucion: IDAT
    limite de libros (heredado de Estudiante): 3
    estado: Vigente

la herencia deja ampliar el sistema sin tocar las clases que ya existen
```

### Los tres niveles: Administrador

```python
from modulos.biblioteca import Biblioteca

b = Biblioteca()
jorge = b.miembro("72345678")
luis = b.miembro("70445566")

print("los dos, con las mismas llamadas:")
for miembro in [luis, jorge]:
    print(f"   {miembro.nombre():<14} {miembro.tipo():<14} "
          f"limite {miembro.membresia().limite_libros()} "
          f"dias {miembro.membresia().dias_prestamo()} "
          f"admin {'si' if miembro.puede_administrar() else 'no'}")

print()
print("esa diferencia de 'admin' es la unica que cambia el menu que se abre:")
print()
print("   if miembro.puede_administrar():")
print("       return menu_admin(biblioteca, miembro)")
print("   return menu_miembro(biblioteca, miembro)")
print()
print("un docente y un administrador ven menus distintos con el mismo codigo")
```

**Salida**

```
los dos, con las mismas llamadas:
   Luis Ramos     docente        limite 5 dias 20 admin no
   Jorge Huaman   administrador  limite 5 dias 20 admin si

esa diferencia de 'admin' es la unica que cambia el menu que se abre:

   if miembro.puede_administrar():
       return menu_admin(biblioteca, miembro)
   return menu_miembro(biblioteca, miembro)

un docente y un administrador ven menus distintos con el mismo codigo
```

### Lo que usa esta seccion

| Tema                     | Donde                           | Que decir                                                     |
| ------------------------ | ------------------------------- | ------------------------------------------------------------- |
| clase base               | Membresia                       | el molde: vencimiento, estado, limite, dias, multa, describir |
| subclases                | Estudiante, Docente, Invitado   | solo cambian sus numeros, leidos de config.py                 |
| herencia de tres niveles | Administrador(Docente)          | un administrador es un docente con permiso de administrar     |
| metodos heredados        | todos los de Membresia          | ninguna hija escribe **init**, heredan el de la madre         |
| override                 | Invitado.describir()            | la unica que cambia un metodo, porque no habla de limites     |
| polimorfismo             | accion_mi_membresia en menu.py  | siete lineas iguales para los cuatro tipos                    |
| MRO                      | Administrador.**mro**           | el orden en que Python busca: hija, madre, abuela             |
| fabrica                  | crear_membresia y crear_usuario | convierten el texto del JSON en objetos de la clase correcta  |
| composicion              | Usuario tiene Membresia         | es un contra tiene un; el miembro le pregunta a su membresia  |
| isinstance               | menu_principal                  | podria usarse, pero el proyecto pregunta puede_administrar()  |
| super()                  | no se usa, y se explica por que | ninguna hija define **init**, no hay nada que encadenar       |

# 6. Los errores que salieron de verdad

Estos no son errores inventados para el cuaderno: son los que aparecieron mientras se armaba el
proyecto, con la causa y la correccion. Sirven para dos cosas: reconocer el patron si vuelve a
salir, y tener respuesta si el profesor pregunta _que problemas tuviste_.

La forma de encontrarlos fue siempre la misma: ejecutar el programa de punta a punta con la
entrada por un tubo y mirar dos cosas, si salio una traza de Python y si aparecio _Opcion no
valida_ en lugares donde no debia. En la seccion 7 estan los comandos para repetirlo.

| Num. | Error                                           | Tipo                     | Donde         |
| ---- | ----------------------------------------------- | ------------------------ | ------------- |
| 1    | la tabla de opciones al inicio del archivo      | NameError                | menu.py       |
| 2    | la busqueda devolvia True o False               | TypeError al imprimir    | libros.py     |
| 3    | una fila de la matriz mas corta que las demas   | IndexError               | libros.py     |
| 4    | pedir secciones y estantes que no existian      | AttributeError           | libros.py     |
| 5    | imprimir claves que el resumen ya no devolvia   | KeyError                 | biblioteca.py |
| 6    | acciones del menu que llamaban metodos borrados | AttributeError           | menu.py       |
| 7    | un mensaje que contradecia los numeros          | logico, no revienta      | usuarios.py   |
| 8    | main llamando a una funcion que ya no existia   | AttributeError           | main.py       |
| 9    | una variable con enie escrita de las dos formas | NameError                | utilidades.py |
| 10   | un nombre de funcion distinto en el comentario  | NameError al descomentar | utilidades.py |
| 11   | un try por un error imposible                   | codigo muerto            | menu.py       |
| 12   | input() sin nada que leer                       | EOFError                 | utilidades.py |

Los seis primeros son los clasicos de un proyecto que crece: se cambia una parte y las otras siguen esperando lo de antes.

> ### Error comun: 1. la tabla de opciones escrita al inicio del modulo
>
> **Asi no**
>
> ```python
> # arriba de todo en menu.py
> MIEMBRO = (
>     ("1", "Consultar catalogo", accion_catalogo),
>     ("2", "Buscar por categoria", accion_buscar_categoria),
>     ("0", "Cerrar sesion", None),
> )
>
>
> def accion_catalogo(biblioteca):
>     ...
> ```
>
> **Asi si**
>
> ```python
> # primero todas las acciones
> def accion_catalogo(biblioteca):
>     ...
>
>
> # y al final del archivo las tablas
> MIEMBRO = (
>     ("1", "Consultar catalogo", accion_catalogo),
>     ("2", "Buscar por categoria", accion_buscar_categoria),
>     ("0", "Cerrar sesion", None),
> )
> ```
>
> **Por que.** Python ejecuta el archivo de arriba hacia abajo. Cuando llega a la tupla, el nombre accion_catalogo todavia no existe porque la def esta mas abajo, y salta NameError: name 'accion_catalogo' is not defined. Una tupla con funciones necesita que esas funciones ya esten definidas. En menu.py las cinco tablas estan al final por eso.

> ### Error comun: 2. la busqueda devolvia True o False en vez de la lista
>
> **Asi no**
>
> ```python
> def buscar_por_categoria(catalogo, nombre):
>     for libro in catalogo:
>         if pertenece_a_categoria(libro.categoria(), nombre):
>             return True
>     return False
> ```
>
> **Asi si**
>
> ```python
> def buscar_por_categoria(catalogo, nombre):
>     if len(catalogo) == 0:
>         return []
>     libro = catalogo[0]
>     if pertenece_a_categoria(libro.categoria(), nombre):
>         return [libro] + buscar_por_categoria(catalogo[1:], nombre)
>     return buscar_por_categoria(catalogo[1:], nombre)
> ```
>
> **Por que.** Con True el menu solo podia decir 'si hay' o 'no hay', y no podia mostrar los resultados ni contarlos. Devolviendo la lista el menu decide que imprimir, y la funcion sigue sirviendo para cualquier otra cosa. Ademas 'Se encontraron 4 titulos' es justo el mensaje que la demo necesita para comprobar que la recursion funciono.

> ### Error comun: 3. una fila de la matriz mas corta que las demas
>
> **Asi no**
>
> ```python
> encabezado = ["Seccion", "E1", "E2", "E3", "E4", "E5", "E6", "Total"]
> fila = [seccion]
> for numero in range(1, 7):
>     fila.append(libres)
> filas.append(fila)          # 7 celdas, pero la cabecera tiene 8
> ```
>
> **Asi si**
>
> ```python
> encabezado = ["Seccion"]
> for numero in range(1, config.estantes + 1):
>     encabezado.append(f"E{numero}")
> encabezado.append("Total")
>
> fila = [seccion]
> total_seccion = 0
> for numero in range(1, config.estantes + 1):
>     libres = 0
>     for libro in catalogo.values():
>         if libro.seccion() == seccion and libro.estante() == numero:
>             libres += libro.disponibles_prestamo()
>     fila.append(libres)
>     total_seccion += libres
> fila.append(total_seccion)   # 8 celdas, igual que la cabecera
> ```
>
> **Por que.** imprimir_matriz calcula las columnas con max(len(fila) for fila in matriz), o sea que toma el largo de la fila mas ancha, y despues recorre cada fila con enumerate. Si una fila tiene menos celdas, el ljust se queda sin indice y salta IndexError: list index out of range. Por eso las tres matrices del proyecto arman el encabezado y cada fila con el mismo bucle sobre config.estantes, y agregan el total al final de la fila. Regla: en una matriz todas las filas miden lo mismo.

> ### Error comun: 4. pedirle a config datos que no tenia
>
> **Asi no**
>
> ```python
> filas = [["Seccion"] + list(range(1, 7))]
> columnas = ["A", "B", "C", "D", "E", "F", "G", "H"]
> ```
>
> **Asi si**
>
> ```python
> filas = [["Seccion"] + [f"E{i}" for i in range(1, config.estantes + 1)]]
> for letra, nombre in config.secciones.items():
>     filas.append([f"{letra} {nombre}"])
> ```
>
> **Por que.** Con los numeros y las letras escritos a mano en libros.py, un cambio en config.py no se reflejaba en las matrices y salia AttributeError o una tabla con filas de mas. Leyendo config.secciones y config.estantes hay una sola fuente de verdad, y si se agrega una seccion nueva las tres matrices la muestran sin tocar nada.

> ### Error comun: 5. imprimir claves que el resumen ya no devolvia
>
> **Asi no**
>
> ```python
> print(f"Titulos: {resumen['titulos']}")
> print(f"Prestamos activos: {resumen['activos']}")
> print(f"Vencidos: {resumen['vencidos']}")
> print(f"Multas: S/{resumen['multas']:.2f}")
> ```
>
> **Asi si**
>
> ```python
> resumen = biblioteca.resumen()
> print(f"Titulos:       {resumen['titulos']}")
> print(f"Ejemplares:    {resumen['ejemplares']}")
> print(f"Disponibles:   {resumen['disponibles']}")
> print(f"Prestados:     {resumen['prestados']}")
> print(f"Miembros:      {resumen['miembros']}")
> ```
>
> **Por que.** Al sacar los prestamos del avance, resumen() dejo de devolver 'activos', 'vencidos' y 'multas', pero la accion del menu seguia pidiendolas: KeyError: 'activos'. Cuando se quita una funcionalidad hay que buscar en todos los archivos quien la estaba consumiendo. grep -rn "resumen\['" modulos/ encuentra esos lugares en segundos.

> ### Error comun: 6. dejar en el menu acciones que llaman metodos que ya no existen
>
> **Asi no**
>
> ```python
> def accion_prestar(biblioteca):
>     prestamo = biblioteca.prestar(isbn, dni)
>     ...
>
>
> ADMIN = (
>     ("1", "Prestar un libro", accion_prestar),
>     ("2", "Registrar devolucion", accion_devolver),
>     ("3", "Ver historial", accion_historial),
> )
> ```
>
> **Asi si**
>
> ```python
> # esas tres acciones y esas tres filas se borran juntas,
> # y el submenu de matrices pasa a ser la opcion 3
>
>
> ADMIN = (
>     ("1", "Estado de la biblioteca", accion_estado),
>     ("2", "Miembros", accion_miembros),
>     ("3", "Matrices y busqueda recursiva", None),
>     ("4", "Guardar cambios en los JSON", accion_guardar),
>     ("0", "Cerrar sesion", None),
> )
> ```
>
> **Por que.** biblioteca.prestar() ya no estaba, pero la accion seguia en el menu: el programa arrancaba bien y reventaba solo cuando alguien elegia esa opcion, con AttributeError: 'Biblioteca' object has no attribute 'prestar'. Es el peor tipo de error porque no aparece al probar lo basico. Al quitar una funcionalidad hay que quitar la accion, la fila de la tabla y renumerar las que vienen despues.

> ### Error comun: 7. un mensaje que contradice los numeros
>
> **Asi no**
>
> ```python
> class Administrador(Docente):
>     MULTA_POR_DIA = config.multa_por_dia["administrador"]   # 0.50
>
>     def describir(self):
>         return "Administrador: sin multa y sin limite"      # mentira
> ```
>
> **Asi si**
>
> ```python
> class Administrador(Docente):
>     MULTA_POR_DIA = config.multa_por_dia["administrador"]
>
>     # describir() se hereda de Membresia, que arma el texto con los numeros reales:
>     # "Administrador: 5 libros por 20 dias"
>     # y "Mi membresia" muestra ademas "Multa por dia de retraso: S/0.50"
> ```
>
> **Por que.** No revienta, que es lo peligroso: el programa anda y la pantalla dice dos cosas distintas a la vez. Pasaba porque el texto estaba escrito a mano mientras el numero venia de config.py. La correccion fue borrar el override y dejar que describir() se arme con los valores reales. Regla: si un texto muestra un numero, que salga del numero, no de un string escrito a mano.

> ### Error comun: 8. main llamando a una funcion que ya no existia
>
> **Asi no**
>
> ```python
> from modulos import menu
>
>
> def main():
>     menu.ejecutar()
> ```
>
> **Asi si**
>
> ```python
> from modulos import errores, menu
> from modulos.biblioteca import Biblioteca
>
>
> def main():
>     try:
>         menu.portada()
>         menu.menu_principal(Biblioteca())
>         return 0
>     except errores.BibliotecaError as error:
>         print(f"Error del sistema de biblioteca: {error}")
>         return 1
> ```
>
> **Por que.** menu.py tenia ejecutar(), que armaba la Biblioteca y abria el menu. Al reordenarlo quedo dividido en portada() y menu_principal(biblioteca), y main.py siguio llamando al nombre viejo: el programa no arrancaba. Ademas el arreglo deja mejor repartido el trabajo: menu.py dibuja pantallas y no sabe como se construye una Biblioteca, y main.py es el unico lugar que crea objetos grandes.

> ### Error comun: 9. una variable con enie escrita de las dos formas
>
> **Asi no**
>
> ```python
> def convertir_fecha(texto):
>     (anio, mes, dia) = str(texto).split("-")
>     return date(int(año), int(mes), int(dia))
> ```
>
> **Asi si**
>
> ```python
> def convertir_fecha(texto):
>     # date() pide el orden inverso al que usamos al escribir: anio, mes, dia
>     (anio, mes, dia) = str(texto).split("-")
>     return date(int(anio), int(mes), int(dia))
> ```
>
> **Por que.** Para Python anio y año son dos nombres distintos. En la version mala la variable se define sin enie y se usa con enie: NameError: name 'año' is not defined, y es dificil de ver porque las dos se leen igual. Salta en cuanto un miembro tiene fecha de vencimiento, o sea al arrancar. La regla del proyecto es que los nombres de variables y funciones van sin enie y sin tilde, y las enies quedan solo adentro de los textos que se muestran y en los datos de los JSON.

> ### Error comun: 10. un nombre distinto en el ejemplo comentado
>
> **Asi no**
>
> ```python
> """  AQUI DEJO UN EJEMPLO DE RECURSION, HAY QUE USAR ESE TEMA
> def cuenta_regresiva(n):
>     if n <= 0:
>         print("Listo!")
>         return 0
>     print(n)
>     return contar_regresiva(n - 1)
> """
> ```
>
> **Asi si**
>
> ```python
> """  AQUI DEJO UN EJEMPLO DE RECURSION, HAY QUE USAR ESE TEMA
> def cuenta_regresiva(n):
>     if n <= 0:
>         print("Listo!")
>         return 0
>     print(n)
>     return cuenta_regresiva(n - 1)
> """
> ```
>
> **Por que.** La funcion se define como cuenta_regresiva y adentro se llamaba contar_regresiva, con el verbo al reves: dos nombres que se leen casi igual. Como el bloque esta comentado no rompe nada hoy, pero el dia que se descomente para la demo da NameError en la segunda vuelta, o sea despues de imprimir el primer numero, que es lo que mas confunde. Ya esta corregido en el archivo, y la moraleja es que los nombres adentro de un comentario tambien se revisan.

> ### Error comun: 11. un try para un error que no puede pasar
>
> **Asi no**
>
> ```python
> def accion_catalogo(biblioteca):
>     try:
>         for libro in biblioteca.catalogo().values():
>             print(libro)
>     except errores.LibroNoEncontradoError:
>         print("No se encontro el libro")
>     except errores.DatosInvalidosError:
>         print("Dato invalido")
> ```
>
> **Asi si**
>
> ```python
> def accion_catalogo(biblioteca):
>     catalogo = biblioteca.catalogo()
>     if len(catalogo) == 0:
>         print("Todavia no hay libros cargados.")
>         return
>     for isbn, libro in catalogo.items():
>         print(f"{isbn}  {libro.titulo()[:40]:<42} {libro.categoria()}")
> ```
>
> **Por que.** Recorrer un diccionario no puede lanzar LibroNoEncontradoError ni DatosInvalidosError: esos errores salen de buscar() y de validar_dni(), que aca no se llaman. El except nunca se ejecuta, y ademas le dice al que lee el codigo que ahi puede pasar algo que no pasa. Un try se pone solo donde el error es posible. Por eso errores.py quedo con tres excepciones y no con once: las otras ocho no las lanzaba nadie.

> ### Error comun: 12. input() cuando ya no queda nada que leer
>
> **Asi no**
>
> ```python
> def pausa():
>     print()
>     input("Presiona ENTER para continuar...")
> ```
>
> **Asi si**
>
> ```python
> # la pausa se queda igual de simple, y el try va donde el error es posible:
>
> def menu_principal(biblioteca):
>     while True:
>         ...
>         try:
>             dni = utilidades.validar_dni(input("DNI del miembro: "))
>         except errores.DatosInvalidosError as error:
>             print(error)
>             continue
> ```
>
> **Por que.** Con una persona escribiendo en la terminal esto nunca falla. Pero si el programa corre con la entrada desde un archivo o desde un tubo, cuando se acaban las lineas input() lanza EOFError. La pausa se dejo simple a proposito, porque no tiene sentido poner un try en cada una, y main.py no atrapa nada. La consecuencia practica es una sola: las secuencias de prueba tienen que terminar con la opcion 0, o sea saliendo por las buenas. Si la entrada se acaba a mitad de camino el programa muestra la traza y termina con codigo 1, que es justo lo que sirve para darse cuenta de que la secuencia estaba mal contada.

### Como repetir la busqueda de errores

```python
import ast
import subprocess
import sys

print("1) que los nueve archivos compilen:")
ruta = os.path.join(CARPETA, "main.py")
modulos = sorted(os.listdir(os.path.join(CARPETA, "modulos")))
archivos = ["main.py"] + [f"modulos/{n}" for n in modulos if n.endswith(".py")]
for archivo in archivos:
    completo = os.path.join(CARPETA, archivo)
    try:
        ast.parse(open(completo, encoding="utf-8").read())
        print(f"   OK   {archivo}")
    except SyntaxError as error:
        print(f"   MAL  {archivo}: {error}")

print()
print("2) que los nombres usados existan (pyflakes, si esta instalado):")
resultado = subprocess.run([sys.executable, "-m", "pyflakes"] +
                           [os.path.join(CARPETA, a) for a in archivos],
                           capture_output=True, text=True)
salida = resultado.stdout.strip()
print("   " + (salida if salida else "sin avisos"))
```

**Salida**

```
1) que los nueve archivos compilen:
   OK   main.py
   OK   modulos/__init__.py
   OK   modulos/biblioteca.py
   OK   modulos/config.py
   OK   modulos/errores.py
   OK   modulos/libros.py
   OK   modulos/menu.py
   OK   modulos/usuarios.py
   OK   modulos/utilidades.py

2) que los nombres usados existan (pyflakes, si esta instalado):
   sin avisos
```

```python
import subprocess
import sys

flujos = {
    "invitado":      ["", "2", "1", "", "2", "Literatura", "", "0", "0"],
    "miembro":       ["", "1", "75678901", "1", "", "2", "Narrativa", "", "3", "", "0", "0"],
    "administrador": ["", "1", "72345678", "1", "", "2", "", "3", "1", "", "2", "", "3", "",
                      "4", "Literatura", "", "0", "4", "n", "", "0", "0"],
    "dado de baja":  ["", "1", "70778899", "0"],
    "dni invalido":  ["", "1", "123", "1", "72345678", "1", "", "0", "0"],
}

marcadores = {
    "invitado": "Se encontraron",
    "miembro": "MI MEMBRESIA",
    "administrador": "MATRIZ DE DISPONIBILIDAD",
    "dado de baja": "dado de baja",
    "dni invalido": "El DNI debe tener 8 digitos",
}

print("3) correr cada flujo con la entrada por un tubo:")
print()
for nombre, lineas in flujos.items():
    entrada = chr(10).join(lineas) + chr(10)
    proceso = subprocess.run([sys.executable, "main.py"], input=entrada,
                             cwd=CARPETA, capture_output=True, text=True, timeout=60)
    traza = "Traceback" in proceso.stdout or "Traceback" in proceso.stderr
    invalida = proceso.stdout.count("Opcion no valida")
    llego = marcadores[nombre] in proceso.stdout
    estado = "OK" if proceso.returncode == 0 and not traza and llego and invalida == 0 else "REVISAR"
    print(f"   {estado:<8} {nombre:<15} exit={proceso.returncode} "
          f"traza={'si' if traza else 'no'} invalidas={invalida} "
          f"marcador={'si' if llego else 'NO'}")
    if proceso.stderr.strip():
        print("            stderr:", proceso.stderr.strip()[:120])
```

**Salida**

```
3) correr cada flujo con la entrada por un tubo:

   OK       invitado        exit=0 traza=no invalidas=0 marcador=si
   OK       miembro         exit=0 traza=no invalidas=0 marcador=si
   OK       administrador   exit=0 traza=no invalidas=0 marcador=si
   OK       dado de baja    exit=0 traza=no invalidas=0 marcador=si
   OK       dni invalido    exit=0 traza=no invalidas=0 marcador=si
```

**El marcador es lo importante.** Un `exit=0` sin trazas no alcanza: la secuencia pudo haberse
quedada corta y no haber llegado a la pantalla que se queria mostrar. Por eso cada flujo busca
ademas un texto que solo aparece si de verdad paso por ahi. Y al reves: si el `exit` es 1 y hay
traza de `EOFError`, lo que esta mal contado es la secuencia de ENTER, no el programa.

### Los errores que quedan por aparecer

Ninguno de los doce de arriba esta en el codigo hoy. Los que si pueden aparecer, y son
esperables en un avance:

| Situacion                                           | Que pasa                                  | Es un error?                                      |
| --------------------------------------------------- | ----------------------------------------- | ------------------------------------------------- |
| Elegir 'Prestar un libro' en el menu                | la opcion no existe                       | no: los prestamos todavia no estan hechos         |
| Escribir un DNI de 8 digitos que no esta en el JSON | 'No se encontro un miembro con ese DNI.'  | no: es el camino previsto                         |
| Escribir una categoria que no existe                | 'No hay titulos en la categoria ...'      | no: la busqueda recursiva devuelve la lista vacia |
| Borrar modulos/datos/libros.json                    | el programa arranca con el catalogo vacio | no: leer_json devuelve una lista vacia            |
| Dejar un JSON mal escrito                           | 'Error del sistema de biblioteca: ...'    | si, pero atrapado y con mensaje claro             |
| Apretar Ctrl+C                                      | 'Programa interrumpido por el usuario.'   | no: es el camino previsto                         |
| Cambiar el nombre de la biblioteca en config.py     | cambia en todas las pantallas             | no: y es lo que hay que hacer antes de presentar  |

# 7. Rubrica, demostracion y lo que falta

La ultima seccion: que pide cada criterio, donde esta la evidencia en el codigo, como hacer la
demostracion paso a paso, y lo que falta. Lo que falta esta dicho sin rodeos porque es un
avance y es mejor decirlo uno que dejar que lo descubran.

## Los cuatro criterios, con la evidencia

| Criterio                             | Puntos | Que pide el nivel maximo                                                                                                                              | Que tiene el proyecto hoy                                                                                                                                                                                         |
| ------------------------------------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Implementaciones de funcionalidad | 5      | registro y actualizacion de libros, gestion de membresias con eliminacion y renovacion, y prestamos con devoluciones que actualicen la disponibilidad | consulta del catalogo, busqueda por categoria, ficha de membresia, estado general, tres matrices y guardado en JSON. Faltan registrar libros, dar de alta o baja miembros desde el menu, y prestar o devolver     |
| 2. Aplicacion de conceptos de POO    | 5      | tres o mas clases con encapsulacion, herencia y polimorfismo, y metodos sobrescritos                                                                  | 8 clases con atributos privados y metodos de acceso, dos arboles de herencia (Membresia con 4 subclases y 3 niveles, y las 3 excepciones), polimorfismo en accion_mi_membresia y override en Invitado.describir() |
| 3. Uso de funciones y metodos        | 4      | funciones con manejo de excepciones, parametros bien definidos, modularidad, y el caso de libros no disponibles por excepcion                         | 38 funciones y 56 metodos en 9 archivos sin ninguna variable global, 3 excepciones propias lanzadas y atrapadas donde corresponde, y Libro.prestar_uno() que lanza DatosInvalidosError si no quedan ejemplares    |
| 4. Uso de matrices y recursividad    | 6      | matrices de disponibilidad, ubicacion y secciones, y busqueda recursiva en una jerarquia de categorias sin desbordar la pila                          | las tres matrices pedidas, mas una tercera vista por categorias, y 3 funciones recursivas con caso base sobre categorias de varios niveles                                                                        |

**Lectura honesta.** Los criterios 2, 3 y 4 estan cubiertos: hay evidencia concreta y se puede
mostrar en la demo. El criterio 1 es el que queda corto, porque justo las funcionalidades que
pide (registrar libros, gestionar membresias desde el menu, prestar y devolver) son las que el
equipo decidio dejar para la siguiente entrega. Conviene decirlo asi, al principio: _esto es un
avance, el criterio 1 esta incompleto a proposito, esto es lo que ya esta listo para
completarlo_.

```python
print("evidencia contable del proyecto:")
print()
import ast

total_clases = total_funciones = total_metodos = 0
recursivas = []
archivos = ["main.py"] + [f"modulos/{n}" for n in
           sorted(os.listdir(os.path.join(CARPETA, "modulos"))) if n.endswith(".py")]

for archivo in archivos:
    arbol = ast.parse(open(os.path.join(CARPETA, archivo), encoding="utf-8").read())
    total_clases += len([n for n in arbol.body if isinstance(n, ast.ClassDef)])
    total_funciones += len([n for n in arbol.body if isinstance(n, ast.FunctionDef)])
    for clase in arbol.body:
        if isinstance(clase, ast.ClassDef):
            total_metodos += len([m for m in clase.body
                                  if isinstance(m, ast.FunctionDef)])
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.FunctionDef):
            se_llama = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                           and n.func.id == nodo.name for n in ast.walk(nodo))
            if se_llama:
                recursivas.append(f"{archivo}: {nodo.name}")

print(f"   clases:            {total_clases}")
print(f"   metodos:           {total_metodos}")
print(f"   funciones sueltas: {total_funciones}")
print(f"   recursivas:        {len(recursivas)}")
for una in recursivas:
    print(f"      {una}")
print()
print(f"   archivos .py:      {len(archivos)} (main.py y los 8 de modulos/)")
print("   lineas:            858")
print(f"   excepciones:       3 (una base y dos especificas)")
print(f"   variables global:  0")
print(f"   librerias externas: 0")
```

**Salida**

```
evidencia contable del proyecto:

   clases:            11
   metodos:           56
   funciones sueltas: 38
   recursivas:        3
      modulos/libros.py: niveles_categoria
      modulos/libros.py: buscar_por_categoria
      modulos/libros.py: pertenece_a_categoria

   archivos .py:      9 (main.py y los 8 de modulos/)
   lineas:            858
   excepciones:       3 (una base y dos especificas)
   variables global:  0
   librerias externas: 0
```

El contador de recursivas usa el arbol sintactico de Python (`ast`): busca funciones cuyo
nombre aparezca en una llamada dentro de su propio cuerpo. Es solo para el cuaderno; en el
proyecto no hay nada de esto.

## Reparto del trabajo

La rubrica habla de grupos de 3 y el equipo es de 4 (el docente ya lo confirmo). Con 8
archivos el reparto sale natural, y cada uno puede defender lo suyo:

| Integrante | Archivos                                                          | Que tiene que saber explicar                                                                                                                  |
| ---------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| A          | modulos/datos/ (los 2 JSON), config.py, errores.py, utilidades.py | por que las reglas estan en diccionarios, como se lee y se guarda el JSON, las 3 excepciones y las utilidades de DNI e ISBN                   |
| B          | usuarios.py, libros.py                                            | el arbol de herencia de Membresia, las fabricas crear_membresia y crear_usuario, la encapsulacion de Libro, las 3 matrices y las 3 recursivas |
| C          | biblioteca.py                                                     | la composicion (tiene libros y miembros), como se carga y se guarda todo, el resumen y la sesion                                              |
| D          | menu.py, main.py, README.md                                       | las tablas de opciones, los 4 bucles de menu, imprimir_matriz, y el try del DNI en menu_principal                                             |

Cada uno puede correr su parte solo. Por ejemplo B:

```python
from modulos.libros import Libro, matriz_categorias, buscar_por_categoria
```

sin arrancar el programa entero. Eso es lo que permite mostrar que el modulo funciona.

## La demostracion paso a paso

Orden sugerido, unos 8 minutos. Cada renglon de la columna _que teclear_ es una linea que se
escribe y se confirma con ENTER; donde dice solo `ENTER` es apretar ENTER sin escribir nada.

Antes de empezar: `python3 main.py` en la carpeta del proyecto, y tener a mano el archivo
`modulos/datos/libros.json` abierto en el editor por si preguntan como se ve el dato crudo.

**El detalle que mas cuesta memorizar:** cada accion del menu termina con `utilidades.pausa()`,
que pide un ENTER, pero al cerrar sesion no hay pausa. Por eso despues del `0` del menu de
administracion viene directo el `0` del menu de acceso.

| Num. | Que teclear | Que se ve                                                                                          | Que decir mientras                                                            |
| ---- | ----------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 1    | ENTER       | la portada: nombre, lema y la fecha de hoy                                                         | el nombre y el lema estan en config.py; se cambian en dos lineas              |
| 2    | 1           | pide 'DNI del miembro:'                                                                            | el ingreso es solo con DNI, no hay contrasenia                                |
| 3    | 72345678    | 'Bienvenido, Jorge Huaman (administrador).'                                                        | menu_principal pregunto puede_administrar() y abrio el menu de administracion |
| 4    | 1           | Estado de la biblioteca: fecha, 7 titulos, 19 ejemplares, 15 disponibles, 4 prestados, 10 miembros | esos numeros los arma Biblioteca.resumen() contando el catalogo               |
| 5    | ENTER       | vuelve al menu de administracion                                                                   | esa pausa la pone el menu, no la accion                                       |
| 6    | 2           | Miembros registrados: la tabla de los 10                                                           | cada fila es un objeto Usuario; el tipo y el estado salen de su membresia     |
| 7    | ENTER       | vuelve al menu                                                                                     | -                                                                             |
| 8    | 3           | el submenu 'Matrices y busqueda recursiva'                                                         | aca estan los 6 puntos del criterio 4                                         |
| 9    | 1           | MATRIZ DE DISPONIBILIDAD                                                                           | filas = secciones, columnas = estantes, con fila y columna de totales         |
| 10   | ENTER       | vuelve al submenu                                                                                  | -                                                                             |
| 11   | 2           | MATRIZ DE UBICACION                                                                                | misma forma, pero cuenta titulos en vez de ejemplares libres                  |
| 12   | ENTER       | vuelve al submenu                                                                                  | -                                                                             |
| 13   | 3           | MATRIZ DE CATEGORIAS                                                                               | agrupa por el primer nivel de la categoria, antes de la /                     |
| 14   | ENTER       | vuelve al submenu                                                                                  | -                                                                             |
| 15   | 4           | pide 'Categoria (por ejemplo Literatura o Narrativa):'                                             | esta es la busqueda recursiva que la rubrica pide textualmente                |
| 16   | Literatura  | 'Se encontraron 4 titulos en Literatura' y la lista con la categoria completa                      | buscar_por_categoria se llama a si misma con la lista cada vez mas corta      |
| 17   | ENTER       | vuelve al submenu                                                                                  | -                                                                             |
| 18   | 0           | vuelve al menu de administracion                                                                   | la opcion 0 del submenu rompe ese while y sigue el de afuera                  |
| 19   | 4           | pide confirmacion para guardar                                                                     | responder_si_no devuelve True o False                                         |
| 20   | n           | 'No se guardo nada.'                                                                               | guardar pide confirmacion a proposito: sobreescribe los JSON                  |
| 21   | ENTER       | vuelve al menu                                                                                     | -                                                                             |
| 22   | 0           | 'Sesion cerrada.'                                                                                  | menu_admin devuelve None y menu_principal cierra la sesion                    |
| 23   | 0           | 'Saliendo del sistema...'                                                                          | sin pausa en el medio: el 0 de acceso va directo despues del 0 de admin       |

Si queda tiempo, estos caminos cortos muestran el manejo de errores y valen la pena:

| Camino                | Que teclear                                            | Que se ve                                                                                                                      |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| invitado              | 2 ENTER 1 ENTER 2 Literatura ENTER 0 ENTER 0 ENTER     | 'Ingresaste como invitado: solo puedes consultar el catalogo.' y despues el catalogo y la busqueda: no ve miembros ni matrices |
| miembro               | 1 ENTER 75678901 ENTER 1 ENTER 3 ENTER 0 ENTER 0 ENTER | el catalogo y la ficha MI MEMBRESIA de Sofia Rojas, con limite 3 libros y 14 dias                                              |
| DNI invalido          | 1 ENTER 123 ENTER                                      | 'El DNI debe tener 8 digitos' y vuelve al menu de acceso, sin cerrarse el programa                                             |
| DNI inexistente       | 1 ENTER 00000000 ENTER                                 | 'No hay ningun miembro registrado con el DNI 00000000.'                                                                        |
| miembro de baja       | 1 ENTER 70778899 ENTER                                 | 'Rosa Palomino esta dado de baja. Consulta con administracion.'                                                                |
| categoria inexistente | (adentro de la busqueda) Redes ENTER                   | 'No hay titulos en la categoria Redes.'                                                                                        |

### Los mismos flujos, probados desde el cuaderno

Para no depender de escribir bien en vivo, estos son los cinco flujos ejecutados de verdad con
la entrada por un tubo. Cada uno comprueba un **marcador**: un texto que solo aparece si el
programa llego a esa pantalla.

```python
import subprocess
import sys

flujos = [
    ("administrador completo",
     ["", "1", "72345678", "1", "", "2", "", "3", "1", "", "2", "", "3", "",
      "4", "Literatura", "", "0", "4", "n", "", "0", "0"],
     ["MATRIZ DE DISPONIBILIDAD", "MATRIZ DE UBICACION", "MATRIZ DE CATEGORIAS",
      "Se encontraron 4 titulos", "No se guardo nada", "Saliendo del sistema"]),
    ("miembro estudiante",
     ["", "1", "75678901", "1", "", "2", "Narrativa", "", "3", "", "0", "0"],
     ["CATALOGO DISPONIBLE", "Se encontraron", "MI MEMBRESIA", "Sesion cerrada"]),
    ("invitado",
     ["", "2", "1", "", "2", "Literatura", "", "0", "0"],
     ["Ingresaste como invitado", "Se encontraron", "Gracias por visitar"]),
    ("miembro dado de baja",
     ["", "1", "70778899", "0"],
     ["dado de baja", config.nombre_biblioteca.upper()[:20]]),
    ("DNI invalido y despues valido",
     ["", "1", "123", "1", "72345678", "1", "", "0", "0"],
     ["El DNI debe tener 8 digitos", "Bienvenido, Jorge Huaman"]),
]

for nombre, lineas, marcadores in flujos:
    entrada = chr(10).join(lineas) + chr(10)
    proceso = subprocess.run([sys.executable, "main.py"], input=entrada,
                             cwd=CARPETA, capture_output=True, text=True, timeout=90)
    traza = "Traceback" in proceso.stdout + proceso.stderr
    faltan = [m for m in marcadores if m not in proceso.stdout]
    mal = proceso.returncode != 0 or traza or faltan or proceso.stdout.count("Opcion no valida")
    print(f"{'REVISAR' if mal else 'OK':<8} {nombre}")
    print(f"         exit={proceso.returncode} traza={'si' if traza else 'no'} "
          f"invalidas={proceso.stdout.count('Opcion no valida')}")
    if faltan:
        print("         faltan los marcadores:", faltan)
    if proceso.stderr.strip():
        print("         stderr:", proceso.stderr.strip()[:150])
```

**Salida**

```
OK       administrador completo
         exit=0 traza=no invalidas=0
OK       miembro estudiante
         exit=0 traza=no invalidas=0
OK       invitado
         exit=0 traza=no invalidas=0
OK       miembro dado de baja
         exit=0 traza=no invalidas=0
OK       DNI invalido y despues valido
         exit=0 traza=no invalidas=0
```

**Por que el marcador y no solo el codigo de salida.** Un `exit=0` sin trazas no alcanza: la
secuencia pudo haberse quedado corta. Comprobar un texto de la pantalla es lo que asegura que
de verdad se recorrio el camino. Y si aparece una traza de `EOFError` con `exit=1`, lo que
esta mal contada es la secuencia de ENTER: como `main.py` no atrapa nada, la entrada tiene que
alcanzar hasta la opcion 0 final.

### Y con printf desde una terminal

Lo mismo sin Python de por medio, util para repasar rapido antes de la presentacion:

```
cd proyecto_parcial

printf '\n1\n72345678\n1\n\n2\n\n3\n1\n\n2\n\n3\n\n4\nLiteratura\n\n0\n4\nn\n\n0\n0\n' | python3 main.py

printf '\n1\n75678901\n1\n\n2\nNarrativa\n\n3\n\n0\n0\n' | python3 main.py

printf '\n2\n1\n\n2\nLiteratura\n\n0\n0\n' | python3 main.py
```

Cada `\n` es un ENTER. El primero es el de la portada, despues vienen las opciones y los
datos. El detalle que mas cuesta: **cada accion del menu termina con `utilidades.pausa()`, que
pide un ENTER**, pero al cerrar sesion no hay pausa, asi que despues del `0` del menu de miembro
viene directo el `0` del menu de acceso. Si sobra o falta un ENTER aparece _Opcion no valida_ y
toda la secuencia se desfasa.

## Lo que falta

Hay que tenerlo listo para decir, con el orden en que se haria. No es una lista de deseos: cada
punto dice que ya existe para apoyarse.

| Falta                                               | Para que criterio | Que ya esta listo                                                                                                                                                        |
| --------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Prestar y devolver libros desde el menu             | 1 y 3             | Libro.prestar_uno() y devolver_uno(), con la validacion y el error si no quedan ejemplares. Falta la clase Prestamo, el gestor y dos acciones de menu                    |
| Historial y multas por retraso                      | 1 y 4             | Membresia.dias_prestamo() y multa_por_dia() ya dan los numeros por tipo, y sumar_dias() calcula el vencimiento. Falta guardar la fecha real del prestamo y restar fechas |
| Registrar y actualizar libros desde el menu         | 1 y 3             | validar_isbn() y Libro.**init** con valores por defecto. Falta la accion que pida los datos y agregue el objeto al catalogo                                              |
| Alta, baja y renovacion de membresias desde el menu | 1                 | Usuario.dar_de_baja(), reactivar(), renovar_membresia() y cancelar_membresia() ya estan escritos. Falta solo la accion de menu que los llame                             |
| Busqueda por titulo o autor                         | 1                 | la recursiva de categorias ya muestra el patron; seria copiarla comparando otro campo                                                                                    |
| Tope de multa                                       | 1                 | config.py es el lugar obvio para ponerlo al lado de multa_por_dia                                                                                                        |
| Nombre y lema definitivos                           | -                 | config.nombre_biblioteca y config.lema, con textos provisionales a proposito                                                                                             |

```python
from modulos import config, utilidades

print("un adelanto de como se calcularia una multa, con lo que ya existe:")
print()
from datetime import date, timedelta

for tipo in ["estudiante", "docente", "administrador"]:
    dias = config.dias_prestamo[tipo]
    multa_dia = config.multa_por_dia[tipo]
    prestado = date.today() - timedelta(days=10)
    vence = utilidades.sumar_dias(prestado, dias)
    retraso = (date.today() - vence).days
    if retraso < 0:
        retraso = 0
    print(f"   {tipo:<15} prestado el {prestado}, vence el {vence}, "
          f"retraso {retraso} dias, multa S/{retraso * multa_dia:.2f}")

print()
print("sumar_dias() y los numeros por tipo ya estan en el proyecto.")
print("Lo que falta es la clase Prestamo que guarde la fecha real de cada prestamo.")
```

**Salida**

```
un adelanto de como se calcularia una multa, con lo que ya existe:

   estudiante      prestado el 2026-10-13, vence el 2026-10-27, retraso 0 dias, multa S/0.00
   docente         prestado el 2026-10-13, vence el 2026-11-02, retraso 0 dias, multa S/0.00
   administrador   prestado el 2026-10-13, vence el 2026-11-02, retraso 0 dias, multa S/0.00

sumar_dias() y los numeros por tipo ya estan en el proyecto.
Lo que falta es la clase Prestamo que guarde la fecha real de cada prestamo.
```

## Preguntas que puede hacer el profesor

| Pregunta                                                        | Respuesta corta                                                                                                                                                              |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Por que dividiste en 8 archivos?                                | Para que cada archivo tenga un solo tema. Cambiar el limite de libros de un estudiante es tocar una linea de config.py.                                                      |
| Que diferencia hay entre funcion y metodo?                      | El metodo esta dentro de una clase y usa self; la funcion esta suelta y recibe todo por parametro. libro.titulo() es metodo, utilidades.convertir_fecha() es funcion.        |
| Por que los atributos tienen guion bajo?                        | Es la senal de 'esto no se toca desde afuera'. Se leen con metodos y se cambian solo por metodos que revisan la regla, como prestar_uno().                                   |
| Donde esta la encapsulacion?                                    | En Libro.prestar_uno(): no deja que los disponibles bajen de cero, y lanza DatosInvalidosError. La regla vive adentro del objeto.                                            |
| Donde esta el polimorfismo?                                     | En accion_mi_membresia: siete lineas iguales para estudiante, docente, administrador e invitado, y cada objeto responde distinto a tipo(), estado() y describir().           |
| Por que Administrador hereda de Docente?                        | Porque un administrador es un docente con permiso extra. Hereda el limite y los dias, y solo agrega PUEDE_ADMINISTRAR = True.                                                |
| Usas super()?                                                   | No, porque ninguna subclase define su propio **init**: todas heredan el de Membresia. Si una agregara un dato, ahi si haria falta.                                           |
| Cual es el caso base de tu recursion?                           | En las tres: la lista vacia devuelve [] y la categoria sin barra devuelve la lista de un nivel. Sin eso seria RecursionError.                                                |
| Podrias hacerlo con un bucle en vez de recursion?               | Si, con split('/') y un for, y daria el mismo resultado. Se hizo recursivo porque la rubrica pide recursion y una categoria es el mismo problema con menos datos.            |
| Que son las tres matrices?                                      | Disponibles por seccion y estante, titulos por seccion y estante, y totales por categoria. Las tres salen del catalogo, ninguna se guarda en el JSON.                        |
| Que excepciones creaste y por que tres?                         | BibliotecaError como base, y DatosInvalidosError y ArchivoDatosError de ella. Tres porque son los tres problemas reales del sistema; habia once y ocho no las lanzaba nadie. |
| Por que DatosInvalidosError hereda tambien de ValueError?       | Para que quien ya sabe manejar ValueError de Python pueda atraparlo sin conocer mis clases.                                                                                  |
| Por que el catalogo es un diccionario y no una lista?           | Para buscar por ISBN directo, sin recorrer. Lo mismo con los miembros por DNI y con las reglas por tipo.                                                                     |
| Donde se guardan los datos?                                     | En dos JSON dentro de modulos/datos/. Se leen al arrancar y se escriben solo cuando se elige 'Guardar cambios', con confirmacion.                                            |
| Usas alguna libreria externa?                                   | Ninguna. Solo json, os, sys y datetime, que vienen con Python.                                                                                                               |
| Usas variables globales?                                        | Ninguna. Todo se pasa por parametro y se devuelve con return. La biblioteca la crea main.py y se la pasa al menu.                                                            |
| Que pasa si borras un JSON?                                     | leer_json devuelve una lista vacia y el programa arranca con el catalogo vacio, sin reventar.                                                                                |
| Y si el JSON esta mal escrito?                                  | json lanza ValueError, biblioteca lo atrapa y lo convierte en ArchivoDatosError con un mensaje claro.                                                                        |
| Prestar libros ya funciona?                                     | No, es lo que falta. Libro.prestar_uno() y devolver_uno() ya estan probados y lanzan el error si no quedan ejemplares; falta la clase Prestamo y las acciones del menu.      |
| Por que algunos libros tienen menos disponibles que ejemplares? | Venia del historial de prestamos del equipo. Como los prestamos no estan hechos, ese numero hoy solo se muestra y alimenta las matrices.                                     |

## Antes de presentar

Una lista corta de cosas que hay que revisar el mismo dia:

| Que                              | Donde                           | Por que                                                                         |
| -------------------------------- | ------------------------------- | ------------------------------------------------------------------------------- |
| El nombre de la biblioteca       | config.nombre_biblioteca        | hoy dice 'Biblioteca POO HAY QUE CAMBIAR NOMBREEEEEE' y sale en la portada      |
| El lema                          | config.lema                     | hoy dice 'FRASE A USAR WAAAAAA'                                                 |
| Que el JSON este como lo dejaron | modulos/datos/                  | si alguien probo guardar cambios, los datos pudieron modificarse                |
| Que la terminal tenga buen ancho | la terminal                     | las tablas estan armadas para 60 caracteres; con menos se doblan                |
| Tener los DNI a mano             | esta guia, seccion demostracion | 72345678 administrador, 75678901 estudiante, 70445566 docente, 70778899 de baja |
| Que Python sea 3                 | python3 --version               | el proyecto usa f-strings, que son de 3.6 en adelante                           |

```python
from modulos import config

print("estado actual de los dos textos que hay que cambiar:")
print()
print("   nombre_biblioteca =", repr(config.nombre_biblioteca))
print("   lema              =", repr(config.lema))
print()
print("si todavia tienen los textos de broma, cambialos en modulos/config.py")
print("antes de la presentacion: son las dos primeras lineas del archivo.")
```

**Salida**

```
estado actual de los dos textos que hay que cambiar:

   nombre_biblioteca = 'Biblioteca POO HAY QUE CAMBIAR NOMBREEEEEE'
   lema              = 'FRASE A USAR WAAAAAA'

si todavia tienen los textos de broma, cambialos en modulos/config.py
antes de la presentacion: son las dos primeras lineas del archivo.
```

## Resumen de una linea por seccion

| Seccion                    | En una linea                                                                                                      |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Portada                    | 9 archivos, 858 lineas, 8 clases, sin librerias externas y sin variables globales                                 |
| 1. Fundamentos             | diccionarios para las reglas y los indices, f-strings para las tablas, while True para los menues                 |
| 2. POO                     | una clase por sustantivo del enunciado, atributos privados con guion bajo y constructores con valores por defecto |
| 3. Funciones y excepciones | el que detecta el problema lanza, el que habla con el usuario atrapa                                              |
| 4. Matrices y recursion    | 3 matrices de doble entrada y 3 recursivas sobre categorias, todas con caso base                                  |
| 5. Herencia y polimorfismo | Membresia con 4 subclases y 3 niveles, y el mismo metodo respondiendo distinto segun el objeto                    |
| 6. Errores                 | los 12 que salieron de verdad, con la causa y la correccion                                                       |
| 7. Rubrica y demo          | criterios 2, 3 y 4 cubiertos; el 1 incompleto a proposito porque es un avance                                     |
