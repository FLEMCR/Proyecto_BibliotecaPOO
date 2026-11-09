# Guía de la versión base

> **Nota de estructura:** esta guía describe la primera versión de consola, cuando el código estaba en `modulos/`. La versión actual usa `core/` para la lógica y `ui/` para las pantallas. Para la estructura vigente, los comandos y las tareas pendientes, revisa `README.md` y `docs/Plan_del_proyecto.md`.

Esta guía recorre lo que se maneja por consola: se entra con el DNI, se navega por un menú según el tipo de usuario y se puede leer el catálogo, buscar, ver la ficha de un libro, ver la membresía y ver la lista de usuarios.

## Índice

1. Qué hace esta versión
2. Las carpetas y los archivos
3. Los datos
4. Arrancar el cuaderno
5. `configuracion.py`, donde se cambia todo lo que se repite
6. `errores.py`, los errores propios del programa
7. `utilidades.py`, las revisiones sueltas
8. La clase `Libro`
9. Las funciones recursivas del catálogo
10. `Usuario` y `Administrador`, herencia y polimorfismo
11. La clase `Biblioteca`
12. Los menús
13. Una corrida completa
14. f-strings y concatenación con `+`
15. Qué temas se abarcaron
16. Qué temas se podrían usar
17. Cómo se podría avanzar el proyecto
18. Qué corregir o mejorar
19. Dónde está cada cosa

## 1. Qué hace esta versión

- muestra una portada con el nombre de la biblioteca, el lema, la fecha de hoy y
  cuántos títulos y usuarios hay;
- deja entrar con un DNI y revisa que el usuario exista, que esté activo y que su
  membresía no haya vencido;
- arma un menú distinto según el tipo de usuario, y la opción de ver los usuarios
  aparece solamente para los administradores;
- lista el catálogo completo;
- busca por un pedazo de texto, que puede estar en el título, en el autor o en la
  categoría;
- muestra la ficha de un libro buscado por su ISBN exacto;
- muestra la membresía de quien entró;
- lista todos los usuarios con su estado.

## 2. Las carpetas y los archivos

```
base/
├── main.py                  arranca todo
├── README.md                qué hay que hacer y qué reglas sigue el grupo
├── datos/
│   ├── libros.json          22 libros
│   └── usuarios.json        13 usuarios
├── docs/
│   ├── Guia_base.ipynb   esta guía, para abrir en la PC
│   ├── Guia_base.md      esta misma guía, para leer en el celular
│   └── 3.1. Rúbrica Parcial_IDAT_POO.pdf
├── interfaces/
│   └── leeme.txt            explica por qué esta carpeta queda vacía acá
└── modulos/
    ├── __init__.py          vacío, es lo que hace que modulos sea un paquete
    ├── configuracion.py     rutas, nombres, secciones, estantes, tipos de usuario
    ├── errores.py           las dos clases de error del programa
    ├── utilidades.py        validar DNI, validar ISBN, convertir fecha, pausa
    ├── libros.py            la clase Libro y las funciones del catálogo
    ├── usuarios.py          las clases Usuario y Administrador
    ├── biblioteca.py        la clase Biblioteca, que junta todo
    └── menu.py              lo que se imprime y lo que se pregunta
```

La regla que sigue el reparto es que **lo que está relacionado esté junto**: todo lo
de los libros en `libros.py`, todo lo de los usuarios en `usuarios.py`, y nada de la
consola fuera de `menu.py`. Las clases no imprimen nunca; las que imprimen son las
funciones de `menu.py`.

## 3. Los datos

Los dos archivos son listas de diccionarios. Cada libro tiene estas claves:

```
isbn, titulo, autor, categoria, seccion, estante, ejemplares, disponibles
```

`disponibles` es la cantidad de ejemplares que están en la biblioteca en este
momento. De ahí sale la regla más importante del préstamo:

> De un libro siempre se queda un ejemplar en la biblioteca. Si hay 10 ejemplares,
> como máximo salen 9.

Esa regla no se guarda en ningún lado, se calcula: `se_puede_prestar()` devuelve
`disponibles > 1`, así que cuando queda uno solo ya no se presta más.

Cada usuario tiene estas claves:

```
dni, nombre, tipo, vencimiento_membresia, activo
```

`tipo` puede ser `Estudiante`, `Docente` o `Administrador`. `activo` es `true` o
`false` en el JSON, que en Python llegan como `True` y `False`.

En los datos sí se usan tildes y ñ, porque son los títulos reales de los libros
(`Cien años de soledad`). En el código no, para que los archivos se abran igual en
cualquier computadora; la sección 18 lista las dos palabras que quedaron con tilde.

```python

import os
import sys

CARPETA_DOCS = os.getcwd()
CARPETA_DEL_PROYECTO = os.path.dirname(CARPETA_DOCS)
if CARPETA_DEL_PROYECTO not in sys.path:
    sys.path.insert(0, CARPETA_DEL_PROYECTO)

from modulos import biblioteca, configuracion, errores, libros, menu, usuarios, utilidades

print("esta guia corre sobre el proyecto que esta en:")
print(CARPETA_DEL_PROYECTO)

```

Salida:

```

esta guia corre sobre el proyecto que esta en:
/home/user/proyecto_parcial/base

```

## 4. Arrancar el cuaderno

La celda de arriba es la única preparación que hace falta. El cuaderno se ejecuta
desde la carpeta `docs/`, así que para llegar al proyecto hay que subir un nivel con
`os.path.dirname()` y agregarlo al `sys.path`. Sin eso, `from modulos import ...` no
encuentra nada.

Cuando se corre `main.py` desde la consola eso no hace falta, porque ahí la carpeta
del proyecto ya está en el camino.

```python

mi_biblioteca = biblioteca.Biblioteca()

resumen = mi_biblioteca.resumen()
for clave in resumen:
    print(clave, "=", resumen[clave])

```

Salida:

```

biblioteca = Biblioteca PO WAAAAAAAAAA
fecha_de_hoy = 2026-10-26
titulos = 22
ejemplares = 45
disponibles = 41
prestados = 4
usuarios = 13

```

Ese diccionario es lo que alimenta la portada de la consola. Una sola llamada y ya están todos los números.

`prestados` no se guarda en ningún archivo: sale de restar `ejemplares` menos
`disponibles` sumando todo el catálogo.

## 5. `configuracion.py`, donde se cambia todo lo que se repite

Este módulo no tiene clases ni lógica. Tiene los valores que aparecen en más de un
lado, para cambiarlos en un solo lugar:

| nombre                                | qué guarda                                               |
| ------------------------------------- | -------------------------------------------------------- |
| `CARPETA_DEL_PROYECTO`                | la carpeta del proyecto, calculada desde `__file__`      |
| `CARPETA_DATOS`                       | dónde están los JSON                                     |
| `ARCHIVO_LIBROS` y `ARCHIVO_USUARIOS` | los nombres de los archivos                              |
| `NOMBRE_BIBLIOTECA` y `LEMA`          | los textos de la portada                                 |
| `SECCIONES`                           | el diccionario de las 5 secciones, de la letra al nombre |
| `CANTIDAD_DE_ESTANTES`                | hasta qué estante existe                                 |
| `TIPOS_DE_USUARIO`                    | los tres tipos aceptados                                 |

Y tres funciones: `ruta_del_archivo()`, que arma el camino completo, y
`leer_archivo()`, que devuelve una lista vacía si el archivo no existe o está vacío,
así el programa no se rompe con una carpeta `datos/` recién creada.

```python

print("nombre de la biblioteca:", configuracion.NOMBRE_BIBLIOTECA)
print("lema:", configuracion.LEMA)
print("carpeta de datos:", configuracion.CARPETA_DATOS)
print("cantidad de estantes:", configuracion.CANTIDAD_DE_ESTANTES)
print("tipos de usuario:", configuracion.TIPOS_DE_USUARIO)
print()
for letra in configuracion.SECCIONES:
    print(letra, "->", configuracion.SECCIONES[letra])

```

Salida:

```

nombre de la biblioteca: Biblioteca PO WAAAAAAAAAA
lema: LEMA QUE USAREMOS WAAAAAA
carpeta de datos: /home/user/proyecto_parcial/base/datos
cantidad de estantes: 3
tipos de usuario: ['Estudiante', 'Docente', 'Administrador']

A -> Literatura
B -> Ciencias sociales
C -> Ciencias e ingenieria
D -> Tecnologia
E -> Arte

```

```python

print("la ruta completa se arma con una sola funcion:")
print(configuracion.ruta_del_archivo(configuracion.ARCHIVO_LIBROS))
print()
registros = configuracion.leer_archivo(configuracion.ARCHIVO_LIBROS)
print("el JSON de libros tiene", len(registros), "registros")
print("las claves del primero son:", list(registros[0].keys()))
print()
print("y un archivo que no existe devuelve una lista vacia, no un error:")
print(configuracion.leer_archivo("no_existe.json"))

```

Salida:

```

la ruta completa se arma con una sola funcion:
/home/user/proyecto_parcial/base/datos/libros.json

el JSON de libros tiene 22 registros
las claves del primero son: ['isbn', 'titulo', 'autor', 'categoria', 'seccion', 'estante', 'ejemplares', 'disponibles']

y un archivo que no existe devuelve una lista vacia, no un error:
[]

```

## 6. `errores.py`, los errores propios del programa

Son dos clases y nada más:

```python
class ErrorBiblioteca(Exception):
    pass


class ErrorDeDatos(ErrorBiblioteca, ValueError):
    pass
```

`ErrorBiblioteca` es la general. `ErrorDeDatos` hereda de ella **y además de
`ValueError`**, que es lo que permite que un dato mal escrito se pueda atrapar de
las dos maneras:

- `except errores.ErrorBiblioteca`, que es lo que hace el menú, y atrapa cualquier
  problema del programa;
- `except ValueError`, si algún día una parte del código prefiere la excepción
  estándar de Python.

Todo lo que el programa rechaza a propósito se lanza como `ErrorDeDatos` con un
mensaje en español que dice exactamente qué está mal. Ese mensaje es el que termina
en la pantalla, así que nunca se ve un traceback por un DNI corto o un ISBN que no
existe.

```python

print("la herencia de los errores:")
print("ErrorDeDatos es ErrorBiblioteca?", issubclass(errores.ErrorDeDatos, errores.ErrorBiblioteca))
print("ErrorDeDatos es ValueError?", issubclass(errores.ErrorDeDatos, ValueError))
print()

intentos = ["12345", "99999999", "97884376049470"]
for intento in intentos:
    try:
        if len(intento) == 13:
            utilidades.validar_isbn(intento)
        else:
            utilidades.validar_dni(intento)
    except errores.ErrorBiblioteca as error:
        print("atrapado como ErrorBiblioteca:", error)

```

Salida:

```

la herencia de los errores:
ErrorDeDatos es ErrorBiblioteca? True
ErrorDeDatos es ValueError? True

atrapado como ErrorBiblioteca: El DNI debe tener 8 digitos
atrapado como ErrorBiblioteca: El DNI debe tener 8 digitos

```

## 7. `utilidades.py`, las revisiones sueltas

Cinco funciones que no pertenecen a ninguna clase porque las usan varias:

| función                  | qué hace                                           |
| ------------------------ | -------------------------------------------------- |
| `validar_dni(texto)`     | 8 dígitos, y si no, `ErrorDeDatos`                 |
| `validar_isbn(codigo)`   | 13 dígitos, y si no, `ErrorDeDatos`                |
| `convertir_fecha(texto)` | `"AAAA-MM-DD"` a `date`, y si no, `ErrorDeDatos`   |
| `si_o_no(valor)`         | `True` se vuelve `"Si"` y `False` se vuelve `"No"` |
| `pausa()`                | imprime el aviso y espera un ENTER                 |

`si_o_no()` existe porque las pantallas muestran texto. En vez de que cada menú
decida cómo se escribe un booleano, se llama a esta función y siempre sale igual.

`convertir_fecha()` tiene dos rechazos distintos, y vale la pena ver la diferencia:

- si el texto no tiene tres partes separadas por guiones, el mensaje es sobre el
  formato;
- si tiene la forma correcta pero la fecha no existe (`2026-02-30`), el `ValueError`
  de `date()` se atrapa y se vuelve a lanzar como `ErrorDeDatos`.

```python

print(utilidades.validar_dni("  11111111  "))
print(utilidades.validar_isbn("9788437604947"))
print(utilidades.convertir_fecha("2026-12-31"))
print(utilidades.si_o_no(True), "/", utilidades.si_o_no(False))
print()

malos = ["12345", "1234567a", "97884376", "31-12-2026", "2026-02-30", "2026-13-01"]
for malo in malos:
    try:
        if "-" in malo:
            utilidades.convertir_fecha(malo)
        elif len(malo) > 8:
            utilidades.validar_isbn(malo)
        else:
            utilidades.validar_dni(malo)
    except errores.ErrorDeDatos as error:
        print(repr(malo), "->", error)

```

Salida:

```

11111111
9788437604947
2026-12-31
Si / No

'12345' -> El DNI debe tener 8 digitos
'1234567a' -> El DNI debe tener 8 digitos
'31-12-2026' -> La fecha 31-12-2026 no es una fecha real
'2026-02-30' -> La fecha 2026-02-30 no es una fecha real
'2026-13-01' -> La fecha 2026-13-01 no es una fecha real

```

## 8. La clase `Libro`

El constructor recibe los ocho datos y los guarda en atributos **privados**, con el
guion bajo adelante:

```python
self._isbn = utilidades.validar_isbn(isbn)
self._titulo = str(titulo).strip()
...
self.revisar_datos()
```

Nadie de afuera toca `self._titulo` directamente. Para leerlo hay un método con el
mismo nombre sin guion: `libro.titulo()`. Y en esta versión no hay ningún método que
lo cambie, porque la base es de solo lectura: los datos se cambian editando el JSON.
Eso es la encapsulación, los atributos quedan adentro y la única puerta son los
métodos.

Lo último que hace el constructor es llamarse a `revisar_datos()`. Eso quiere decir
que **no puede existir un objeto `Libro` mal formado**: si algún dato no sirve, el
objeto no llega a crearse.

```python

un_libro = mi_biblioteca.libro("9788437604947")

print("isbn:          ", un_libro.isbn())
print("titulo:        ", un_libro.titulo())
print("autor:         ", un_libro.autor())
print("categoria:     ", un_libro.categoria())
print("seccion:       ", un_libro.seccion(), "->", configuracion.SECCIONES[un_libro.seccion()])
print("estante:       ", un_libro.estante())
print("ejemplares:    ", un_libro.ejemplares())
print("disponibles:   ", un_libro.disponibles())
print("se puede prestar:", un_libro.se_puede_prestar())

```

Salida:

```

isbn:           9788437604947
titulo:         Cien años de soledad
autor:          Gabriel Garcia Marquez
categoria:      Literatura
seccion:        A -> Literatura
estante:        1
ejemplares:     3
disponibles:    2
se puede prestar: True

```

```python

print("y el metodo que todavia no esta terminado:")
print()
print("  prestados() devuelve:", repr(un_libro.prestados()))
print("  lo que deberia devolver:", un_libro.ejemplares() - un_libro.disponibles())
print()
print("ese texto fijo es el que aparece en el catalogo de la consola.")
print("esta anotado como pendiente en la seccion 18.")

```

Salida:

```

y el metodo que todavia no esta terminado:

  prestados() devuelve: 'AUN POR HACER'
  lo que deberia devolver: 1

ese texto fijo es el que aparece en el catalogo de la consola.
esta anotado como pendiente en la seccion 18.

```

```python

print("el libro que tiene un solo ejemplar:")
libro_de_uno = mi_biblioteca.libro("9789972433353")
print(" ", libro_de_uno.titulo())
print("  ejemplares:", libro_de_uno.ejemplares())
print("  disponibles:", libro_de_uno.disponibles())
print("  se puede prestar:", libro_de_uno.se_puede_prestar())
print()
print("y el que ya tiene uno prestado y le queda otro:")
otro = mi_biblioteca.libro("9788420677300")
print(" ", otro.titulo())
print("  ejemplares:", otro.ejemplares(), "disponibles:", otro.disponibles())
print("  se puede prestar:", otro.se_puede_prestar())

```

Salida:

```

el libro que tiene un solo ejemplar:
  Deus absconditus: retrospectiva de Manuel Moncloa 1980-2011
  ejemplares: 1
  disponibles: 1
  se puede prestar: False

y el que ya tiene uno prestado y le queda otro:
  Aplicaciones de Inteligencia Artificial en la Educación Superior Universitaria
  ejemplares: 1 disponibles: 1
  se puede prestar: False

```

Ahí está la regla del ejemplar que siempre se queda, funcionando sola: con
`disponibles` en 1, `se_puede_prestar()` da `False`.

Los dos métodos que devuelven diccionarios cumplen tareas distintas:

- `a_diccionario()` devuelve exactamente las ocho claves del JSON. Es lo que se
  usaría para volver a escribir el archivo.
- `datos_para_pantalla()` arranca de ese mismo diccionario y le agrega lo que la
  pantalla necesita ya resuelto: el nombre de la sección, si se puede prestar como
  `"Si"` o `"No"`, y los ejemplares prestados.

Ninguno de los dos modifica el libro, los dos arman un diccionario nuevo.

```python

print("a_diccionario, las ocho claves del JSON:")
for clave, valor in un_libro.a_diccionario().items():
    print("  ", clave, "=", valor)
print()
print("datos_para_pantalla, lo que va directo a la consola o a un QLabel:")
for clave, valor in un_libro.datos_para_pantalla().items():
    print("  ", clave, "=", valor)

```

Salida:

```

a_diccionario, las ocho claves del JSON:
   isbn = 9788437604947
   titulo = Cien años de soledad
   autor = Gabriel Garcia Marquez
   categoria = Literatura
   seccion = A
   estante = 1
   ejemplares = 3
   disponibles = 2

datos_para_pantalla, lo que va directo a la consola o a un QLabel:
   isbn = 9788437604947
   titulo = Cien años de soledad
   autor = Gabriel Garcia Marquez
   categoria = Literatura
   seccion = A
   estante = 1
   ejemplares = 3
   disponibles = 2
   seccion_nombre = Literatura
   prestados = AUN POR HACER
   se_puede_prestar = Si

```

```python

print("revisar_datos() se llama solo al crear el objeto, y rechaza:")

casos_malos = [
    {"isbn": "9780000000001", "titulo": "", "autor": "Alguien", "categoria": "Arte",
     "seccion": "E", "estante": 1, "ejemplares": 2, "disponibles": 2},
    {"isbn": "9780000000002", "titulo": "Sin autor", "autor": "  ", "categoria": "Arte",
     "seccion": "E", "estante": 1, "ejemplares": 2, "disponibles": 2},
    {"isbn": "9780000000003", "titulo": "Seccion que no existe", "autor": "Alguien",
     "categoria": "Arte", "seccion": "Z", "estante": 1, "ejemplares": 2, "disponibles": 2},
    {"isbn": "9780000000004", "titulo": "Estante pasado", "autor": "Alguien",
     "categoria": "Arte", "seccion": "E", "estante": 9, "ejemplares": 2, "disponibles": 2},
    {"isbn": "9780000000005", "titulo": "Cero ejemplares", "autor": "Alguien",
     "categoria": "Arte", "seccion": "E", "estante": 1, "ejemplares": 0, "disponibles": 0},
    {"isbn": "9780000000006", "titulo": "Disponibles de menos", "autor": "Alguien",
     "categoria": "Arte", "seccion": "E", "estante": 1, "ejemplares": 2, "disponibles": -1},
    {"isbn": "9780000000007", "titulo": "Presta mas de lo que tiene", "autor": "Alguien",
     "categoria": "Arte", "seccion": "E", "estante": 1, "ejemplares": 2, "disponibles": 5},
]

for caso in casos_malos:
    try:
        libros.crear_libro(caso)
    except errores.ErrorDeDatos as error:
        print("  ", error)

```

Salida:

```

revisar_datos() se llama solo al crear el objeto, y rechaza:
   El titulo no puede quedar vacio
   El autor no puede quedar vacio
   La seccion Z no existe.
   El estante debe estar entre 1 y 3
   Un libro debe tener por lo menos 1 ejemplar
   La cantidad para realizar prestamos no puede ser menor a 0
   No se puede prestar más de lo que se tiene

```

Siete rechazos distintos y los siete con un mensaje que se entiende. Ninguno llega a
crear el objeto.

## 9. Las funciones recursivas del catálogo

En `libros.py` hay tres funciones sueltas, aparte de la clase. Dos son recursivas:

```python
def buscar_por_texto(libros, texto):
    if len(libros) == 0:
        return []
    primer_libro = libros[0]
    libros_que_faltan = libros[1:]
    if coincide_con_la_busqueda(primer_libro, texto):
        return [primer_libro] + buscar_por_texto(libros_que_faltan, texto)
    return buscar_por_texto(libros_que_faltan, texto)
```

Las tres partes de cualquier recursión están ahí y conviene tenerlas ubicadas:

- **el caso base**: `if len(libros) == 0: return []`. Con la lista vacía se corta.
- **el paso**: se mira `libros[0]` y se vuelve a llamar con `libros[1:]`, que es la
  lista un elemento más corta.
- **lo que se acumula**: el libro que coincide se pone adelante con `+`.

`datos_del_catalogo()` tiene exactamente la misma forma, pero en vez de filtrar
convierte cada libro con `datos_para_pantalla()`.

La tercera función, `coincide_con_la_busqueda()`, no es recursiva: pasa el texto a
minúsculas y pregunta si está en el título, en el autor o en la categoría. Como los
dos lados están en minúsculas, buscar `arte` encuentra `Arte` y buscar `VARGAS`
encuentra `Vargas`.

```python

encontrados = libros.buscar_por_texto(mi_biblioteca.todos_los_libros(), "ma")
print("buscando 'ma' salieron", len(encontrados), "libros:")
for libro in encontrados:
    print("   ", libro.titulo())

```

Salida:

```

buscando 'ma' salieron 14 libros:
    Cien años de soledad
    Maze Runner: Correr o morir
    Don Quijote de la Mancha
    La ciudad y los perros
    El sistema jurídico: Introducción al derecho
    Tradiciones peruanas
    El capital: Crítica de la economía política (Tomo I)
    Matemáticas 1
    Cálculo Diferencial
    Eloquent JavaScript
    Aplicaciones de Inteligencia Artificial en la Educación Superior Universitaria
    Franquicias imaginarias: las opciones estéticas en las artes plásticas en el Perú de fin de siglo
    Imaginación visual y cultura en el Perú
    Deus absconditus: retrospectiva de Manuel Moncloa 1980-2011

```

```python

print("la misma funcion con otros textos:")
for texto in ["arte", "peru", "vargas", "fisica", "xyz", ""]:
    resultado = libros.buscar_por_texto(mi_biblioteca.todos_los_libros(), texto)
    print("   ", repr(texto), "->", len(resultado), "libros")

```

Salida:

```

la misma funcion con otros textos:
    'arte' -> 4 libros
    'peru' -> 1 libros
    'vargas' -> 1 libros
    'fisica' -> 1 libros
    'xyz' -> 0 libros
    '' -> 0 libros

```

Con `xyz` no sale ninguno y con el texto vacío tampoco. Ese último caso es
deliberado: `coincide_con_la_busqueda()` devuelve `False` si no escribieron nada,
para que buscar sin escribir no devuelva el catálogo entero por error.

Y acá se ve para qué sirve el caso base. Si se saca, la función se llama a sí misma
para siempre:

```python

def buscar_sin_caso_base(lista, texto):
    primer_elemento = lista[0]
    return [primer_elemento] + buscar_sin_caso_base(lista[1:], texto)

try:
    buscar_sin_caso_base(["a", "b", "c"], "a")
except RecursionError as error:
    print("RecursionError:", error)
except IndexError as error:
    print("IndexError:", error)
    print("(la lista se fue achicando hasta quedar vacia y lista[0] ya no existe)")

print()
print("el limite de recursion de este Python es", sys.getrecursionlimit())

```

Salida:

```

IndexError: list index out of range
(la lista se fue achicando hasta quedar vacia y lista[0] ya no existe)

el limite de recursion de este Python es 1000

```

## 10. `Usuario` y `Administrador`, herencia y polimorfismo

`usuarios.py` tiene dos clases:

```python
class Usuario:
    ...

class Administrador(Usuario):
    ...
```

`Administrador` hereda todo de `Usuario`: el constructor, los ocho métodos de
lectura, `estado()`, `datos_de_membresia()`. No se repite ni una línea de eso.

Lo único que hace distinto son dos cosas:

- `puede_administrar()` devuelve `True`. En `Usuario` devuelve `False`.
- `datos_de_membresia()` llama a `super().datos_de_membresia()` para conseguir el
  diccionario común y después le agrega la clave `puede_administrar`.

Eso es **polimorfismo**: el menú llama a `usuario.puede_administrar()` sin saber qué
clase tiene adelante, y cada clase responde lo suyo. El mismo llamado, dos
comportamientos.

En el constructor de `Usuario` hay una decisión que vale la pena ver:

```python
if vencimiento_membresia is None:
    raise errores.ErrorDeDatos(
        f"El usuario {self._nombre} no tiene fecha de vencimiento de membresia"
    )
```

El parámetro tiene `None` por defecto, pero si llega `None` de verdad el objeto no se
crea: mejor un mensaje claro que un usuario sin fecha que después rompa en
`tiene_membresia_vigente()`.

Y `crear_usuario()` es la fábrica: mira el `tipo` y decide qué clase instanciar.

```python

estudiante = mi_biblioteca.usuario("11111111")
administrador = mi_biblioteca.usuario("33333333")

print("de que clase es cada uno:")
print("  ", estudiante.nombre(), "->", type(estudiante).__name__)
print("  ", administrador.nombre(), "->", type(administrador).__name__)
print()
print("los dos son Usuario?", isinstance(estudiante, usuarios.Usuario),
      isinstance(administrador, usuarios.Usuario))
print("el estudiante es Administrador?", isinstance(estudiante, usuarios.Administrador))
print("el administrador es Administrador?", isinstance(administrador, usuarios.Administrador))
print()
print("el mismo llamado, dos respuestas:")
print("  ", estudiante.nombre(), "puede administrar:", estudiante.puede_administrar())
print("  ", administrador.nombre(), "puede administrar:", administrador.puede_administrar())

```

Salida:

```

de que clase es cada uno:
   P_ESTUDIANTE -> Usuario
   P_ADMINISTRADOR -> Administrador

los dos son Usuario? True True
el estudiante es Administrador? False
el administrador es Administrador? True

el mismo llamado, dos respuestas:
   P_ESTUDIANTE puede administrar: False
   P_ADMINISTRADOR puede administrar: True

```

```python

print("la diferencia en el diccionario:")
print()
print("un usuario comun devuelve", len(estudiante.datos_de_membresia()), "claves:")
for clave, valor in estudiante.datos_de_membresia().items():
    print("   ", clave, "=", valor)
print()
print("un administrador devuelve", len(administrador.datos_de_membresia()), "claves:")
for clave, valor in administrador.datos_de_membresia().items():
    print("   ", clave, "=", valor)

```

Salida:

```

la diferencia en el diccionario:

un usuario comun devuelve 5 claves:
    dni = 11111111
    nombre = P_ESTUDIANTE
    tipo = Estudiante
    vencimiento_membresia = 2027-12-31
    estado = Activo y con membresia vigente

un administrador devuelve 6 claves:
    dni = 33333333
    nombre = P_ADMINISTRADOR
    tipo = Administrador
    vencimiento_membresia = 2027-12-31
    estado = Activo y con membresia vigente
    puede_administrar = Si

```

```python

print("los tres estados posibles de una cuenta:")
print()
for datos in mi_biblioteca.datos_de_los_usuarios():
    print("   ", datos["dni"], "|", datos["nombre"][:24].ljust(24),
          "|", datos["tipo"][:13].ljust(13), "|", datos["vencimiento_membresia"],
          "|", datos["estado"])

```

Salida:

```

los tres estados posibles de una cuenta:

    11111111 | P_ESTUDIANTE             | Estudiante    | 2027-12-31 | Activo y con membresia vigente
    22222222 | P_DOCENTE                | Docente       | 2027-12-31 | Activo y con membresia vigente
    33333333 | P_ADMINISTRADOR          | Administrador | 2027-12-31 | Activo y con membresia vigente
    70445566 | Luis Ramos               | Docente       | 2027-05-21 | Activo y con membresia vigente
    71234567 | Carla Mendoza            | Docente       | 2025-12-15 | De baja
    76789012 | Diego Vargas             | Docente       | 2026-10-20 | Membresia vencida
    70778899 | Rosa Palomino            | Estudiante    | 2026-09-18 | De baja
    70889900 | Marco Perez              | Estudiante    | 2026-11-23 | Activo y con membresia vigente
    72345678 | Jorge Huaman             | Estudiante    | 2027-01-10 | Activo y con membresia vigente
    73456789 | Lucia Torres             | Estudiante    | 2024-06-30 | De baja
    74567890 | Pedro Castillo           | Estudiante    | 2026-08-05 | De baja
    75678901 | Sofia Rojas              | Estudiante    | 2027-10-02 | Activo y con membresia vigente
    78901234 | Valeria Sanchez          | Administrador | 2026-03-15 | Membresia vencida

```

Los tres estados salen de `estado()`, que pregunta en este orden:

1. si no está activo, `"De baja"`;
2. si la fecha de vencimiento ya pasó, `"Membresia vencida"`;
3. si no, `"Activo y con membresia vigente"`.

El orden importa: un usuario dado de baja con la membresía vencida se muestra como
`De baja`, que es lo más importante de los dos.

`tiene_membresia_vigente()` compara `date.today()` con la fecha guardada, así que no
hay ninguna fecha de "hoy" escrita a mano en el código: el programa dice la verdad
el día que se ejecuta.

## 11. La clase `Biblioteca`

`Biblioteca` es la que junta todo. Adentro guarda dos diccionarios privados:

```python
self._catalogo = {}     la clave es el ISBN
self._usuarios = {}     la clave es el DNI
```

Diccionarios y no listas porque así buscar un libro por su ISBN es directo, sin
recorrer nada. `cargar_datos()` lee los dos JSON, convierte cada registro con
`crear_libro()` y `crear_usuario()`, y los guarda con su clave.

Después, todo lo que ofrece son métodos cortos que devuelven **listas y
diccionarios con texto listo para mostrar**:

| método                    | qué devuelve                                   |
| ------------------------- | ---------------------------------------------- |
| `todos_los_libros()`      | la lista de objetos `Libro`                    |
| `todos_los_usuarios()`    | la lista de objetos `Usuario`                  |
| `libro(isbn)`             | el objeto, o `ErrorDeDatos` si no existe       |
| `usuario(dni)`            | el objeto, o `ErrorDeDatos` si no existe       |
| `datos_del_catalogo()`    | el catálogo completo, un diccionario por libro |
| `datos_de_un_libro(isbn)` | la ficha de uno solo                           |
| `buscar(texto)`           | los libros que coinciden, ya en diccionarios   |
| `datos_de_los_usuarios()` | la lista de usuarios con su estado             |
| `datos_de_membresia(dni)` | la membresía de uno solo                       |
| `resumen()`               | los números de la portada                      |

```python

print("buscar() devuelve diccionarios, no objetos:")
resultado = mi_biblioteca.buscar("arte")
print("  libros encontrados:", len(resultado))
print("  el primero es un", type(resultado[0]).__name__)
print()
for libro in resultado:
    print("   ", libro["titulo"][:52].ljust(52), "|", libro["categoria"],
          "| seccion", libro["seccion"], "| estante", libro["estante"])

```

Salida:

```

buscar() devuelve diccionarios, no objetos:
  libros encontrados: 4
  el primero es un dict

    Franquicias imaginarias: las opciones estéticas en l | Arte | seccion E | estante 1
    Imaginación visual y cultura en el Perú              | Arte | seccion E | estante 2
    Deus absconditus: retrospectiva de Manuel Moncloa 19 | Arte | seccion E | estante 3
    Patrimonio, Kukuli Velarde                           | Arte | seccion E | estante 3

```

```python

print("los dos errores que lanza Biblioteca:")
try:
    mi_biblioteca.libro("9780000000000")
except errores.ErrorDeDatos as error:
    print("  ", error)

try:
    mi_biblioteca.usuario("12345678")
except errores.ErrorDeDatos as error:
    print("  ", error)

try:
    mi_biblioteca.libro("97884376")
except errores.ErrorDeDatos as error:
    print("  ", error)

```

Salida:

```

los dos errores que lanza Biblioteca:
   No hay ningun libro con el ISBN 9780000000000
   No hay ningun usuario con el DNI 12345678
   El ISBN debe tener 13 digitos

```

## 12. Los menús

Todo lo de la consola está en `menu.py`. Son tres menús:

**La portada**, que se imprime una vez al arrancar, con el nombre de la biblioteca,
el lema, la fecha de hoy y los totales.

**El menú de acceso**, el primero que se ve:

```
MENU DE ACCESO
1) Acceder con DNI
0) Salir
```

**El menú de sesión**, el que se abre después de entrar. Es el mismo para todos,
pero la opción 5 se imprime solamente si el usuario puede administrar:

```
MENU DE ESTUDIANTE             MENU DE ADMINISTRADOR
1) Ver el catalogo             1) Ver el catalogo
2) Buscar un libro             2) Buscar un libro
3) Ver un libro por ISBN       3) Ver un libro por ISBN
4) Mi membresia                4) Mi membresia
0) Cerrar sesion               5) Ver los usuarios
                               0) Cerrar sesion
```

El título sale del tipo de usuario, por eso dice `MENU DE ESTUDIANTE`,
`MENU DE DOCENTE` o `MENU DE ADMINISTRADOR`.

Las tres cosas que hacen que el menú no se rompa:

- es un `while True`, así que vuelve a mostrar las opciones hasta que elijan `0`;
- si escriben cualquier otra cosa, dice que la opción no existe y sigue;
- cada acción está dentro de un `try` que atrapa `ErrorBiblioteca`, así que un DNI o
  un ISBN mal escrito se muestra como un mensaje y no como un traceback.

Y antes de entrar, `entrar()` revisa tres cosas en orden: que el DNI exista, que el
usuario no esté de baja y que su membresía no haya vencido. Cada rechazo tiene su
propio mensaje.

```python

print("las opciones se imprimen segun el usuario:")
print()
for dni in ["11111111", "22222222", "33333333"]:
    usuario = mi_biblioteca.usuario(dni)
    print(f"MENU DE {usuario.tipo().upper()}")
    print("1) Ver el catalogo")
    print("2) Buscar un libro")
    print("3) Ver un libro por ISBN")
    print("4) Mi membresia")
    if usuario.puede_administrar():
        print("5) Ver los usuarios")
    print("0) Cerrar sesion")
    print()

```

Salida:

```

las opciones se imprimen segun el usuario:

MENU DE ESTUDIANTE
1) Ver el catalogo
2) Buscar un libro
3) Ver un libro por ISBN
4) Mi membresia
0) Cerrar sesion

MENU DE DOCENTE
1) Ver el catalogo
2) Buscar un libro
3) Ver un libro por ISBN
4) Mi membresia
0) Cerrar sesion

MENU DE ADMINISTRADOR
1) Ver el catalogo
2) Buscar un libro
3) Ver un libro por ISBN
4) Mi membresia
5) Ver los usuarios
0) Cerrar sesion

```

```python

print("los tres rechazos al entrar:")
print()
for dni in ["70778899", "76789012", "99999999"]:
    try:
        usuario = mi_biblioteca.usuario(dni)
        if not usuario.esta_activo():
            raise errores.ErrorDeDatos(
                f"{usuario.nombre()} no puede entrar, su usuario esta de baja"
            )
        if not usuario.tiene_membresia_vigente():
            raise errores.ErrorDeDatos(
                f"{usuario.nombre()} no puede entrar, su membresia vencio el "
                + str(usuario.vencimiento_membresia())
            )
    except errores.ErrorBiblioteca as error:
        print("  No se pudo entrar:", error)

```

Salida:

```

los tres rechazos al entrar:

  No se pudo entrar: Rosa Palomino no puede entrar, su usuario esta de baja
  No se pudo entrar: Diego Vargas no puede entrar, su membresia vencio el 2026-10-20
  No se pudo entrar: No hay ningun usuario con el DNI 99999999

```

## 13. Una corrida completa

Acá se ejecuta `main.py` de verdad, mandándole por teclado lo que escribiría una
persona. Es la prueba más rápida de que todo está conectado.

La corrida hace esto: entra con el DNI de un estudiante, ve el catálogo, busca un
libro, sale; vuelve a entrar con el DNI del administrador, ve la lista de usuarios,
prueba una opción que no existe y cierra.

```python

import subprocess

lineas_del_teclado = [
    "1", "11111111", "1", "", "2", "arte", "", "3", "9788437604947", "",
    "4", "", "0",
    "1", "33333333", "5", "", "9", "", "0",
    "0",
]
entrada = chr(10).join(lineas_del_teclado) + chr(10)

proceso = subprocess.run(
    [sys.executable, "main.py"],
    cwd=CARPETA_DEL_PROYECTO,
    input=entrada,
    capture_output=True,
    text=True,
)

print("codigo de salida:", proceso.returncode)
print("errores en stderr:", repr(proceso.stderr))
print("lineas que imprimio:", len(proceso.stdout.splitlines()))

```

Salida:

```

codigo de salida: 0
errores en stderr: ''
lineas que imprimio: 211

```

```python

salida = proceso.stdout.splitlines()

donde_empieza_el_catalogo = salida.index("CATALOGO: 22 libros")
print(chr(10).join(salida[:donde_empieza_el_catalogo]))

```

Salida:

```


Biblioteca PO WAAAAAAAAAA
LEMA QUE USAREMOS WAAAAAA
Hoy es 2026-10-26

////////////////////
Hay 22 titulos y 13 usuarios registrados
////////////////////

MENU DE ACCESO
1) Acceder con DNI
0) Salir
Elige una opcion: Escribe tu DNI:
Hola P_ESTUDIANTE, tu tipo de membresia es Estudiante

MENU DE ESTUDIANTE

1) Ver el catalogo
2) Buscar un libro
3) Ver un libro por ISBN
4) Mi membresia
0) Cerrar sesion
Elige una opcion:

```

```python

print("el catalogo, las primeras lineas:")
print()
print(chr(10).join(salida[donde_empieza_el_catalogo:donde_empieza_el_catalogo + 10]))

```

Salida:

```

el catalogo, las primeras lineas:

CATALOGO: 22 libros

9788437604947 | Cien años de soledad | Gabriel Garcia Marquez
   Literatura, seccion A (Literatura), estante 1, ejemplares 3, en el estante 2, prestados AUN POR HACER, se puede prestar: Si

9788445073728 | El Señor de los Anillos: La Comunidad del Anillo | J. R. R. Tolkien
   Literatura, seccion A (Literatura), estante 1, ejemplares 2, en el estante 2, prestados AUN POR HACER, se puede prestar: Si

9789876122672 | Maze Runner: Correr o morir | James Dashner
   Literatura, seccion A (Literatura), estante 2, ejemplares 2, en el estante 2, prestados AUN POR HACER, se puede prestar: Si

```

```python

donde_empieza_la_membresia = salida.index("MEMBRESIA")
print("la membresia del estudiante:")
print()
print(chr(10).join(salida[donde_empieza_la_membresia:donde_empieza_la_membresia + 7]))

donde_empieza_el_administrador = salida.index("MENU DE ADMINISTRADOR")
print()
print("y el administrador si ve la opcion 5:")
print()
print(chr(10).join(salida[donde_empieza_el_administrador:donde_empieza_el_administrador + 11]))

```

Salida:

```

la membresia del estudiante:

MEMBRESIA
Nombre: P_ESTUDIANTE
DNI: 11111111
Tipo de membresia: Estudiante
Vencimiento: 2027-12-31
Estado: Activo y con membresia vigente


y el administrador si ve la opcion 5:

MENU DE ADMINISTRADOR

1) Ver el catalogo
2) Buscar un libro
3) Ver un libro por ISBN
4) Mi membresia
5) Ver los usuarios
0) Cerrar sesion
Elige una opcion:
USUARIOS: 13
11111111 | P_ESTUDIANTE | Estudiante | vence 2027-12-31 | Activo y con membresia vigente

```

```python

print("el final: una opcion que no existe, cerrar sesion y salir")
print()
print(chr(10).join(salida[-9:]))

```

Salida:

```

el final: una opcion que no existe, cerrar sesion y salir

3) Ver un libro por ISBN
4) Mi membresia
5) Ver los usuarios
0) Cerrar sesion
Elige una opcion:
MENU DE ACCESO
1) Acceder con DNI
0) Salir
Elige una opcion: Cerrando el programa...

```

El programa termina con código de salida 0 y el `stderr` vacío, que es la señal de
que no hubo ningún traceback.

Los DNIs que sirven para probar:

| DNI        | qué pasa                             |
| ---------- | ------------------------------------ |
| `11111111` | entra, estudiante                    |
| `22222222` | entra, docente                       |
| `33333333` | entra, administrador, ve la opción 5 |
| `78901234` | entra, el otro administrador         |
| `70778899` | rechazado, está de baja              |
| `76789012` | rechazado, su membresía venció       |
| `99999999` | rechazado, no existe                 |

## 14. f-strings y concatenación con `+`

En el proyecto conviven las dos formas de armar un texto con datos adentro, y están
puestas así a propósito para compararlas.

**La que se usa en casi todo el código es el f-string.** Se escribe una `f` antes de
la comilla y los valores van entre llaves, en el lugar exacto donde se quieren ver:

```python
print(f"Hola {usuario.nombre()}, tu tipo de membresia es {usuario.tipo()}")
print(f"MENU DE {usuario.tipo().upper()}")
raise errores.ErrorDeDatos(f"No hay ningun libro con el ISBN {isbn_buscado}")
```

Dentro de las llaves va cualquier expresión, no solo una variable:
`{usuario.tipo().upper()}` llama a un método y después lo pasa a mayúsculas, todo en
la misma línea.

**En algunos lugares quedó la concatenación con `+`**, que era la forma que se usaba
antes:

```python
print("Hoy es " + resumen["fecha_de_hoy"])
print("No se pudo entrar: " + str(error))
raise errores.ErrorDeDatos("La fecha " + str(texto) + " no es una fecha real")
```

Las dos dan exactamente el mismo resultado. La diferencia es cómo se escribe:

|                         | f-string           | con `+`                          |
| ----------------------- | ------------------ | -------------------------------- |
| cómo se ve              | `f"Hola {nombre}"` | `"Hola " + nombre`               |
| si el valor no es texto | lo convierte solo  | hay que poner `str()` a mano     |
| si el texto es largo    | se lee de corrido  | se cortan las comillas y los `+` |
| para unir muchas partes | una sola expresión | una cadena de `+`                |

El `+` tiene una trampa que el f-string no: **solo une textos**. Si un lado es un
número, Python lanza un `TypeError`. Por eso en los tres casos que quedaron con `+`
hay un `str()` envolviendo el valor, o el valor ya era un texto.

Los f-strings quedaron donde el mensaje tiene varios datos juntos, que es donde más
se nota la diferencia. Los `+` quedaron en mensajes cortos de una sola pieza, donde
las dos formas se leen igual de bien.

```python

nombre = "Ana Torres"
tipo = "Estudiante"
cantidad = 3

print("las dos formas, el mismo resultado:")
print("  con +      :", "Hola " + nombre + ", tu tipo de membresia es " + tipo)
print("  con f-string:", f"Hola {nombre}, tu tipo de membresia es {tipo}")
print()
print("iguales?", ("Hola " + nombre + ", tu tipo de membresia es " + tipo)
      == f"Hola {nombre}, tu tipo de membresia es {tipo}")

```

Salida:

```

las dos formas, el mismo resultado:
  con +      : Hola Ana Torres, tu tipo de membresia es Estudiante
  con f-string: Hola Ana Torres, tu tipo de membresia es Estudiante

iguales? True

```

```python

print("con un numero adentro se ve la diferencia:")
print()
try:
    print("  con +      :", "hay " + cantidad + " ejemplares")
except TypeError as error:
    print("  con +      : TypeError ->", error)

print("  con str()  :", "hay " + str(cantidad) + " ejemplares")
print("  con f-string:", f"hay {cantidad} ejemplares")
print()
print("el f-string convirtio el numero solo, sin pedir str()")

```

Salida:

```

con un numero adentro se ve la diferencia:

  con +      : TypeError -> can only concatenate str (not "int") to str
  con str()  : hay 3 ejemplares
  con f-string: hay 3 ejemplares

el f-string convirtio el numero solo, sin pedir str()

```

```python

print("y dentro de las llaves va cualquier expresion:")
print()
libro = mi_biblioteca.libro("9788437604947")
print(f"  metodo adentro       : {libro.titulo().upper()}")
print(f"  cuenta adentro       : prestados = {libro.ejemplares() - libro.disponibles()}")
print(f"  un if adentro        : {'se presta' if libro.se_puede_prestar() else 'no se presta'}")
print(f"  texto con comillas   : el titulo es \"{libro.titulo()}\"")

```

Salida:

```

y dentro de las llaves va cualquier expresion:

  metodo adentro       : CIEN AÑOS DE SOLEDAD
  cuenta adentro       : prestados = 1
  un if adentro        : se presta
  texto con comillas   : el titulo es "Cien años de soledad"

```

```python

print("cuantos hay de cada forma en el proyecto:")
print()

total_fstrings = 0
total_mas = 0
for nombre_del_archivo in ["configuracion.py", "errores.py", "utilidades.py", "libros.py",
                           "usuarios.py", "biblioteca.py", "menu.py"]:
    ruta = os.path.join(CARPETA_DEL_PROYECTO, "modulos", nombre_del_archivo)
    with open(ruta, encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    fstrings = 0
    concatenaciones = 0
    for linea in lineas:
        if 'f"' in linea or "f'" in linea:
            fstrings = fstrings + 1
        if '" + ' in linea or "' + " in linea or ' + str(' in linea:
            concatenaciones = concatenaciones + 1
    total_fstrings = total_fstrings + fstrings
    total_mas = total_mas + concatenaciones
    if fstrings > 0 or concatenaciones > 0:
        print(f"  {nombre_del_archivo:20} f-strings: {fstrings:2}   con +: {concatenaciones}")

print()
print(f"  total: {total_fstrings} lineas con f-string y {total_mas} con concatenacion")

```

Salida:

```

cuantos hay de cada forma en el proyecto:

  utilidades.py        f-strings:  0   con +: 1
  libros.py            f-strings:  2   con +: 0
  usuarios.py          f-strings:  2   con +: 0
  biblioteca.py        f-strings:  2   con +: 0
  menu.py              f-strings: 33   con +: 2

  total: 39 lineas con f-string y 3 con concatenacion

```

## 15. Qué temas se abarcaron

Todo lo que aparece en esta versión, con el archivo donde está:

| tema                                        | dónde se ve                                                                          |
| ------------------------------------------- | ------------------------------------------------------------------------------------ |
| Programas modulares e importaciones         | 8 módulos en `modulos/` y `main.py` que solo importa `menu` y `Biblioteca`           |
| Clases y objetos                            | `Libro`, `Usuario`, `Administrador`, `Biblioteca`                                    |
| Atributos y métodos                         | los ocho atributos de `Libro` y sus métodos de lectura                               |
| Constructores con valores por defecto       | `Usuario(dni, nombre, tipo="Estudiante", vencimiento_membresia=None, activo=True)`   |
| Encapsulación                               | atributos con `_` adelante y métodos para leerlos                                    |
| Herencia                                    | `Administrador(Usuario)`                                                             |
| Polimorfismo                                | `puede_administrar()` y `datos_de_membresia()` responden distinto según la clase     |
| `super()`                                   | `Administrador.datos_de_membresia()` reusa la del padre y le agrega una clave        |
| Estructuras de control                      | `if`/`elif`/`else` en `revisar_datos()` y en `estado()`, `while True` en los menús   |
| Bucles `for`                                | en `cargar_datos()`, en `resumen()`, en los menús                                    |
| Operadores                                  | comparaciones, `and`/`or`, `in`, `not in`, resta y suma                              |
| Listas y diccionarios                       | el catálogo y los usuarios son diccionarios; los reportes son listas de diccionarios |
| Recursión                                   | `buscar_por_texto()` y `datos_del_catalogo()`                                        |
| Excepciones                                 | `ErrorBiblioteca`, `ErrorDeDatos`, `raise`, `try`/`except`/`else`                    |
| Fechas                                      | `date.today()`, `str()` de una fecha, comparación de fechas                          |
| Archivos JSON                               | `leer_archivo()` con `json.loads()`                                                  |
| Manejo de entradas                          | `input()` en los menús, `validar_dni()`, `validar_isbn()`                            |
| Funciones que devuelven datos para pantalla | `datos_para_pantalla()`, `datos_de_membresia()`, `resumen()`                         |

## 16. Qué temas se podrían usar

Cosas que el proyecto todavía no toca y que encajarían sin romper nada:

- **Más recursión.** `cargar_datos()` arma los diccionarios con un `for`; se podría
  escribir recursivo igual que `datos_del_catalogo()`. También se podría recorrer el
  catálogo al revés, o contar los títulos de una sección sin bucle.
- **Matrices.** En esta versión las tablas son listas de una dimensión. La versión
  final ya deberia armar matrices de secciones por estantes, que es el siguiente paso natural.
- **Escritura en archivos.** `configuracion.py` ya sabe leer; falta el espejo, una
  función `guardar_archivo()` con `json.dump()`.
- **Más excepciones.** Una clase `ErrorDeArchivo` para cuando un JSON viene mal
  escrito o no se puede abrir, y un `finally` para cerrar cosas.
- **Interfaces gráficas.** PyQt5 con las ventanas `.ui`. La lógica no cambia: los métodos de `Biblioteca` devuelven
  diccionarios y esos diccionarios llenan `QLabel` y `QTableWidget`.
- **Validaciones más finas.** Que el DNI no empiece en cero, que el ISBN cumpla el
  dígito de control real, que una fecha no venga del futuro.
- **Ordenamiento.** El catálogo sale en el orden del JSON. Se podría ordenar por
  título o por autor, con `sorted()` y una función `key`, o con un ordenamiento
  escrito a mano.
- **Comprensión de listas.** `datos_de_los_usuarios()` ya usa una; se podría usar en
  más lugares, aunque el `for` común se lee más fácil.
- **Archivos de texto plano.** Un `.txt` con el historial, además del JSON.
- **Métodos para cambiar datos.** Esta versión es de solo lectura. Un
  `cambiar_datos(titulo=..., autor=...)` con parámetros por nombre dejaría corregir un
  libro sin reescribir el JSON a mano.

## 17. Cómo se podría avanzar el proyecto

El camino de la versión base a la versión final, en el orden en que conviene
hacerlo:

1. **Escribir en los archivos.** Agregar `guardar_archivo()` en `configuracion.py` y
   un método `guardar_datos()` en `Biblioteca` que vuelque los tres diccionarios a
   sus JSON. Con eso el programa ya puede cambiar algo de verdad.
2. **Los préstamos.** Una clase `Prestamo` con su código, el ISBN, el DNI, la fecha
   en que se lo llevaron, la fecha límite y la fecha de devolución. Un archivo
   `prestamos.json` y una constante `DIAS_DE_PRESTAMO = 15` en `configuracion.py`.
3. **Las reglas del préstamo.** Que sean 15 días para todos, que una persona pueda
   tener un solo libro sin devolver a la vez, y que siempre quede un ejemplar en la
   biblioteca. Las tres se revisan antes de prestar y cada una lanza su
   `ErrorDeDatos`.
4. **La devolución.** Buscar el préstamo por su código, ponerle la fecha de hoy, y
   devolverle el ejemplar al libro.
5. **Los reportes.** Matrices de secciones por estantes y de categorías, más el
   resumen del historial. Ahí entran las matrices que pide la rúbrica.
6. **Quitar la consola.** Que `Biblioteca` devuelva todo y nadie imprima, para poder
   enchufarle las ventanas. `menu.py` se deja de usar y aparece `pruebas.py`, que
   llama a los métodos y muestra lo que devuelven.
7. **Las ventanas.** Cargar cada `.ui` con `uic.loadUi()` y conectar los botones a
   los métodos de `Biblioteca`.

## 18. Qué corregir o mejorar

Cosas que están pendientes o que se podrían pulir, con el archivo y la línea donde
tocar:

1. **`prestados()` en `libros.py` devuelve un texto fijo.** Ahora mismo devuelve
   `"Aun por hacer".upper()`, así que el catálogo imprime `prestados AUN POR HACER`
   en cada libro. El cálculo es una línea:
   `return self._ejemplares - self._disponibles`.
2. **Dos palabras con tilde en el código.** `año` en `convertir_fecha()` de
   `utilidades.py`, y `más` en el mensaje `"No se puede prestar más de lo que se
tiene"` de `libros.py`. Se cambian por `año` y `mas`.
3. **Un error de tipeo en el menú.** En `menu_de_acceso()` dice
   `"Opción invalida. Preube de nuevo"`: `Preube` es `Pruebe`, y `Opción` lleva
   tilde cuando el resto del código no.
4. **`crear_libro()` no tiene valores por defecto para todo.** `isbn`, `titulo` y
   `autor` usan `datos.get("isbn", "")`, pero `categoria`, `seccion`, `estante`,
   `ejemplares` y `disponibles` usan `datos.get(...)` sin segundo argumento. Si un
   JSON viene sin el estante, llega `None` y `int(None)` lanza un `TypeError` en vez
   de un `ErrorDeDatos`. Poner `0` o `1` por defecto lo arregla.
5. **Un JSON mal escrito termina en traceback.** `leer_archivo()` hace
   `json.loads(contenido)` sin `try`. Si alguien edita el archivo a mano y le falta
   una coma, el programa se cierra con un error de la librería `json`. Se podría
   atrapar y volver a lanzar como un error propio que diga qué archivo está mal.
6. **El nombre y el lema de la biblioteca están con textos de prueba.**
   `NOMBRE_BIBLIOTECA` y `LEMA` en `configuracion.py` tienen los textos con
   `WAAAAAA`. Se cambian ahí y en ningún otro lado.
7. **Las etiquetas dicen "en el estante" y el campo se llama `disponibles`.** En
   `mostrar_catalogo()` y `mostrar_libro()` de `menu.py` el texto dice
   `en el estante` pero la clave es `disponibles`. Los dos nombres apuntan a lo
   mismo; conviene elegir uno para que no queden dos palabras para la misma cosa.
8. **`menu.py` repite la lista de opciones.** El menú de sesión se imprime dos
   veces, una en el `if` del administrador y otra en el `else`. Se podría imprimir
   una sola vez y agregar la opción 5 con un `if` adentro.

## 19. Dónde está cada cosa

Para responder rápido cuando pregunten:

| si preguntan por...                                     | está en                                           |
| ------------------------------------------------------- | ------------------------------------------------- |
| el nombre de la biblioteca, las secciones, los estantes | `modulos/configuracion.py`                        |
| las clases de error                                     | `modulos/errores.py`                              |
| la validación del DNI y del ISBN                        | `modulos/utilidades.py`                           |
| la conversión de fechas                                 | `modulos/utilidades.py`                           |
| la clase `Libro` y sus revisiones                       | `modulos/libros.py`                               |
| la regla del ejemplar que siempre se queda              | `Libro.se_puede_prestar()` en `modulos/libros.py` |
| la búsqueda por texto y la recursión                    | `modulos/libros.py`, al final                     |
| la clase `Usuario` y la herencia                        | `modulos/usuarios.py`                             |
| la fábrica que decide qué clase crear                   | `crear_usuario()` en `modulos/usuarios.py`        |
| el catálogo y los usuarios cargados                     | `modulos/biblioteca.py`                           |
| los números de la portada                               | `Biblioteca.resumen()`                            |
| lo que se imprime y lo que se pregunta                  | `modulos/menu.py`                                 |
| por dónde arranca todo                                  | `main.py`                                         |
| los libros y los usuarios                               | `datos/libros.json` y `datos/usuarios.json`       |
| la rúbrica del parcial                                  | `docs/`                                           |
