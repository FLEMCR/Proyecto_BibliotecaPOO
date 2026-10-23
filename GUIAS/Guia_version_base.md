# Guia de la version base

Esta guia y el archivo `.md` que esta al lado tienen el mismo contenido. El `.md` es para leer en el celular, este cuaderno es para ejecutar las pruebas.

## Indice

1. Que hace esta version
2. Las carpetas
3. Que hay en cada archivo
4. Los datos
5. Como arranca el programa
6. La clase Libro
7. La clase Usuario y la clase Administrador
8. La clase Biblioteca
9. Los errores
10. La recursion
11. Los menus
12. Donde cambiar cada cosa
13. Errores comunes
14. Lo que falta para llegar a la version final

## 1. Que hace esta version

La version base abre los dos JSON, arma los libros y los usuarios en la memoria y los deja listos para verse en pantalla.

Tiene menus de consola para:

- entrar con el DNI,
- ver el catalogo completo,
- buscar un libro escribiendo un pedazo del titulo, del autor o de la categoria,
- ver un solo libro por su ISBN,
- ver la membresia (ahi dice si el usuario es Estudiante, Docente o Administrador),
- y, si el usuario es administrador, ver la lista de todos los usuarios.

Esta version no presta libros, no devuelve libros, no agrega libros y no guarda nada en los JSON. Todo eso esta en la version final.

## 2. Las carpetas

```
base/
    main.py          arranca el programa
    modulos/         todo el codigo
    datos/           los 2 JSON
    interfaces/      aca van las pantallas .ui (por ahora esta vacia)
    cuadernos/       esta guia
```

`datos/` e `interfaces/` estan fuera de `modulos/` porque no son codigo: son los archivos que el codigo lee y las pantallas que despues lo van a usar.

Para correr el programa hay que pararse en la carpeta `base/`:

```
cd base
python main.py
```

## 3. Que hay en cada archivo

| archivo                    | que tiene                                                                                            |
| -------------------------- | ---------------------------------------------------------------------------------------------------- |
| `main.py`                  | crea la Biblioteca y abre el menu de acceso                                                          |
| `modulos/configuracion.py` | el nombre de la biblioteca, las secciones, los estantes, las rutas y las funciones que leen los JSON |
| `modulos/errores.py`       | las 3 excepciones del programa                                                                       |
| `modulos/utilidades.py`    | revisar el DNI, el ISBN y las fechas                                                                 |
| `modulos/libros.py`        | la clase `Libro` y las funciones que recorren el catalogo                                            |
| `modulos/usuarios.py`      | las clases `Usuario` y `Administrador`                                                               |
| `modulos/biblioteca.py`    | la clase `Biblioteca`, que junta los libros y los usuarios                                           |
| `modulos/menu.py`          | los menus y lo que se imprime en la consola                                                          |

Los archivos que estan juntos se necesitan entre si: `libros.py` y `usuarios.py` usan `utilidades.py` y `errores.py`, y `biblioteca.py` usa los dos.

## 4. Los datos

En `datos/` hay dos archivos.

`libros.json` tiene 22 libros. Cada uno se ve asi:

```json
{
  "isbn": "9788437604947",
  "titulo": "Cien años de soledad",
  "autor": "Gabriel Garcia Marquez",
  "categoria": "Literatura",
  "seccion": "A",
  "estante": 1,
  "ejemplares": 3,
  "en_estante": 2
}
```

| campo                          | que es                                 |
| ------------------------------ | -------------------------------------- |
| `isbn`                         | 13 digitos, no se repite               |
| `titulo`, `autor`, `categoria` | los datos del libro                    |
| `seccion`                      | una letra de la A a la E               |
| `estante`                      | un numero del 1 al 3                   |
| `ejemplares`                   | cuantas copias compro la biblioteca    |
| `en_estante`                   | cuantas copias hay ahora en el estante |

De `ejemplares` y `en_estante` sale el resto: `prestados = ejemplares - en_estante`.

`usuarios.json` tiene 13 usuarios:

```json
{
  "dni": "11111111",
  "nombre": "P_ESTUDIANTE",
  "tipo": "Estudiante",
  "vencimiento_membresia": "2027-12-31",
  "activo": true
}
```

El `tipo` puede ser `Estudiante`, `Docente` o `Administrador`. Ese dato es el que decide que menu se abre.

Los JSON si llevan tildes y enie, porque son los nombres reales de los libros. En el codigo no.

```python

import os
import sys

CARPETA_DEL_PROYECTO = os.path.dirname(os.getcwd())
if CARPETA_DEL_PROYECTO not in sys.path:
    sys.path.insert(0, CARPETA_DEL_PROYECTO)

from modulos import biblioteca, configuracion, errores, libros, usuarios

print("proyecto:", CARPETA_DEL_PROYECTO)
print("datos:", configuracion.CARPETA_DATOS)

```

Salida:

```

proyecto: /home/user/proyecto_parcial/base
datos: /home/user/proyecto_parcial/base/datos

```

## 5. Como arranca el programa

`main.py` hace tres cosas:

```python
from modulos import biblioteca, errores, menu


def main():
    try:
        mi_biblioteca = biblioteca.Biblioteca()
    except errores.ErrorDeArchivo as error:
        print("No se pudieron leer los datos: " + str(error))
        return
    menu.portada(mi_biblioteca)
    menu.menu_de_acceso(mi_biblioteca)


main()
```

1. Crea la `Biblioteca`. En ese momento se leen los dos JSON y se arman los objetos.
2. Si un JSON esta roto, el programa lo dice y se cierra en vez de reventar.
3. Muestra la portada y abre el menu de acceso.

Veamos que devuelve la Biblioteca apenas se crea:

```python

mi_biblioteca = biblioteca.Biblioteca()

resumen = mi_biblioteca.resumen()
for clave in resumen:
    print(clave, "=", resumen[clave])

```

Salida:

```

biblioteca = Biblioteca IDAT
fecha_de_hoy = 2026-10-23
titulos = 22
ejemplares = 45
en_estante = 41
prestados = 4
usuarios = 13

```

Ese diccionario es lo que va en la portada de la consola y, despues, en las etiquetas de la ventana principal.

Adentro de `cargar_datos()` pasa esto:

```python
self._catalogo = {}
for registro in configuracion.leer_archivo(configuracion.ARCHIVO_LIBROS):
    libro = libros.crear_libro(registro)
    self._catalogo[libro.isbn()] = libro
```

El catalogo es un diccionario cuya clave es el ISBN. Buscar un libro por ISBN es entonces directo, no hay que recorrer la lista.

Con los usuarios pasa lo mismo, pero la clave es el DNI.

## 6. La clase Libro

Un `Libro` guarda sus datos en atributos privados, con guion bajo adelante:

```python
self._isbn = utilidades.validar_isbn(isbn)
self._titulo = str(titulo).strip()
```

Y se leen con metodos:

```python
def titulo(self):
    return self._titulo
```

Eso es la encapsulacion: nadie cambia `libro._titulo` desde afuera por accidente, y si un dia hay que revisar algo antes de devolver el titulo, se cambia en un solo lugar.

El constructor tambien revisa los datos apenas se crea el libro, con `revisar_datos()`. Si algo no sirve, tira un error en ese momento y no despues, cuando ya nadie sabe de donde salio.

```python

un_libro = mi_biblioteca.libro("9788437604947")

print("titulo:", un_libro.titulo())
print("autor:", un_libro.autor())
print("categoria:", un_libro.categoria())
print("seccion:", un_libro.seccion())
print("estante:", un_libro.estante())
print("ejemplares:", un_libro.ejemplares())
print("en el estante:", un_libro.en_estante())
print("prestados:", un_libro.prestados())
print("se puede prestar:", un_libro.se_puede_prestar())

```

Salida:

```

titulo: Cien años de soledad
autor: Gabriel Garcia Marquez
categoria: Literatura
seccion: A
estante: 1
ejemplares: 3
en el estante: 2
prestados: 1
se puede prestar: True

```

`prestados()` y `se_puede_prestar()` no guardan nada, se calculan:

```python
def prestados(self):
    return self._ejemplares - self._en_estante

def se_puede_prestar(self):
    return self._en_estante > 1
```

`se_puede_prestar()` dice que si solo cuando en el estante hay mas de un ejemplar. La regla es que siempre queda uno en la biblioteca: si hay 2 ejemplares se presta 1 y el otro se queda; si queda 1 solo, no se presta.

```python

libro_de_uno = mi_biblioteca.libro("9789972433353")
print(libro_de_uno.titulo())
print("ejemplares:", libro_de_uno.ejemplares(), "| en el estante:", libro_de_uno.en_estante())
print("se puede prestar:", libro_de_uno.se_puede_prestar())

```

Salida:

```

Deus absconditus: retrospectiva de Manuel Moncloa 1980-2011
ejemplares: 1 | en el estante: 1
se puede prestar: False

```

Los dos metodos que devuelven diccionarios:

- `a_diccionario()` devuelve los datos tal como estan en el JSON. Sirve para guardar.
- `datos_para_pantalla()` devuelve lo mismo mas tres cosas que la pantalla necesita: el nombre de la seccion, los prestados y el `Si` o `No` de si se puede prestar.

Ninguno de los dos devuelve `True` o `False` suelto: `datos_para_pantalla()` ya lo convierte en `Si` o `No`, que es lo que se lee en una etiqueta.

```python

print("a_diccionario:", un_libro.a_diccionario())
print()
print("datos_para_pantalla:", un_libro.datos_para_pantalla())

```

Salida:

```

a_diccionario: {'isbn': '9788437604947', 'titulo': 'Cien años de soledad', 'autor': 'Gabriel Garcia Marquez', 'categoria': 'Literatura', 'seccion': 'A', 'estante': 1, 'ejemplares': 3, 'en_estante': 2}

datos_para_pantalla: {'isbn': '9788437604947', 'titulo': 'Cien años de soledad', 'autor': 'Gabriel Garcia Marquez', 'categoria': 'Literatura', 'seccion': 'A', 'estante': 1, 'ejemplares': 3, 'en_estante': 2, 'seccion_nombre': 'Literatura', 'prestados': 1, 'se_puede_prestar': 'Si'}

```

## 7. La clase Usuario y la clase Administrador

`Usuario` es la unica clase para las personas. El tipo (Estudiante, Docente, Administrador) es un dato, no una clase aparte.

`Administrador` hereda de `Usuario`:

```python
class Administrador(Usuario):
    def puede_administrar(self):
        return True

    def datos_de_membresia(self):
        datos = super().datos_de_membresia()
        datos["puede_administrar"] = utilidades.si_o_no(self.puede_administrar())
        return datos
```

En `Usuario` el metodo `puede_administrar()` devuelve `False`. En `Administrador` devuelve `True`. Eso es polimorfismo: el mismo metodo, llamado igual, se comporta segun la clase del objeto.

Y `crear_usuario()` es la que decide cual de las dos clases crear:

```python
if str(tipo).strip().lower() == "administrador":
    return Administrador(dni, nombre, tipo, vencimiento_membresia, activo)
return Usuario(dni, nombre, tipo, vencimiento_membresia, activo)
```

```python

estudiante = mi_biblioteca.usuario("11111111")
docente = mi_biblioteca.usuario("70445566")
administrador = mi_biblioteca.usuario("33333333")

print("clase del estudiante:", type(estudiante).__name__)
print("clase del docente:", type(docente).__name__)
print("clase del administrador:", type(administrador).__name__)
print()
print("puede administrar el estudiante:", estudiante.puede_administrar())
print("puede administrar el administrador:", administrador.puede_administrar())

```

Salida:

```

clase del estudiante: Usuario
clase del docente: Usuario
clase del administrador: Administrador

puede administrar el estudiante: False
puede administrar el administrador: True

```

```python

print("membresia del estudiante:")
for clave, valor in estudiante.datos_de_membresia().items():
    print("  ", clave, "=", valor)

print()
print("membresia del administrador:")
for clave, valor in administrador.datos_de_membresia().items():
    print("  ", clave, "=", valor)

```

Salida:

```

membresia del estudiante:
   dni = 11111111
   nombre = P_ESTUDIANTE
   tipo = Estudiante
   vencimiento_membresia = 2027-12-31
   estado = Al dia

membresia del administrador:
   dni = 33333333
   nombre = P_ADMINISTRADOR
   tipo = Administrador
   vencimiento_membresia = 2027-12-31
   estado = Al dia
   puede_administrar = Si

```

El administrador tiene una clave mas en su diccionario: `puede_administrar`. Los otros no la tienen, asi que en la pantalla esa linea aparece solo para los administradores.

El `estado` se calcula con `estado()`:

```python
def estado(self):
    if not self.esta_activo():
        return "De baja"
    if not self.tiene_membresia_vigente():
        return "Membresia vencida"
    return "Al dia"
```

```python

for datos in mi_biblioteca.datos_de_los_usuarios():
    print(datos["dni"], "|", datos["nombre"], "|", datos["tipo"], "|", datos["estado"])

```

Salida:

```

11111111 | P_ESTUDIANTE | Estudiante | Al dia
22222222 | P_DOCENTE | Docente | Al dia
33333333 | P_ADMINISTRADOR | Administrador | Al dia
70445566 | Luis Ramos | Docente | Al dia
71234567 | Carla Mendoza | Docente | De baja
76789012 | Diego Vargas | Docente | Membresia vencida
70778899 | Rosa Palomino | Estudiante | De baja
70889900 | Marco Perez | Estudiante | Al dia
72345678 | Jorge Huaman | Estudiante | Al dia
73456789 | Lucia Torres | Estudiante | De baja
74567890 | Pedro Castillo | Estudiante | De baja
75678901 | Sofia Rojas | Estudiante | Al dia
78901234 | Valeria Sanchez | Administrador | Membresia vencida

```

## 8. La clase Biblioteca

`Biblioteca` es el unico objeto con el que hablan los menus. Adentro tiene el catalogo y los usuarios, y afuera devuelve siempre datos listos para mostrar.

| metodo                    | que devuelve                                           |
| ------------------------- | ------------------------------------------------------ |
| `cargar_datos()`          | lee los JSON y devuelve el resumen                     |
| `todos_los_libros()`      | la lista de objetos `Libro`                            |
| `todos_los_usuarios()`    | la lista de objetos `Usuario`                          |
| `libro(isbn)`             | un objeto `Libro`                                      |
| `usuario(dni)`            | un objeto `Usuario`                                    |
| `datos_del_catalogo()`    | una lista de diccionarios, uno por libro               |
| `datos_de_un_libro(isbn)` | un diccionario con los datos de ese libro              |
| `buscar(texto)`           | una lista de diccionarios con los libros que coinciden |
| `datos_de_los_usuarios()` | una lista de diccionarios, uno por usuario             |
| `datos_de_membresia(dni)` | un diccionario con la membresia                        |
| `resumen()`               | un diccionario con los numeros generales               |

Los que devuelven objetos (`libro`, `usuario`, `todos_los_libros`) son para usar adentro del codigo. Los que devuelven diccionarios son para la pantalla.

```python

catalogo = mi_biblioteca.datos_del_catalogo()
print("libros en el catalogo:", len(catalogo))
print()
print("los primeros tres:")
for datos in catalogo[:3]:
    print("  ", datos["titulo"], "|", datos["autor"], "| se puede prestar:", datos["se_puede_prestar"])

```

Salida:

```

libros en el catalogo: 22

los primeros tres:
   Cien años de soledad | Gabriel Garcia Marquez | se puede prestar: Si
   El Señor de los Anillos: La Comunidad del Anillo | J. R. R. Tolkien | se puede prestar: Si
   Maze Runner: Correr o morir | James Dashner | se puede prestar: Si

```

## 9. Los errores

En `errores.py` hay tres clases:

```python
class ErrorBiblioteca(Exception):
    pass


class ErrorDeDatos(ErrorBiblioteca, ValueError):
    pass


class ErrorDeArchivo(ErrorBiblioteca):
    pass
```

- `ErrorDeDatos` salta cuando el DNI no tiene 8 digitos, cuando el ISBN no tiene 13, cuando no existe ese libro o ese usuario, cuando una fecha no es fecha.
- `ErrorDeArchivo` salta cuando un JSON esta mal escrito.
- `ErrorBiblioteca` es la madre de las dos, y es la que atrapan los menus. Con un solo `except errores.ErrorBiblioteca` se atrapan las dos.

`ErrorDeDatos` hereda tambien de `ValueError`, que es la excepcion normal de Python para un valor malo. Asi, si alguien atrapa un `ValueError` generico, tambien atrapa los nuestros.

```python

intentos = ["12345", "99999999", "97884376049470"]

for texto in intentos:
    try:
        mi_biblioteca.usuario(texto)
    except errores.ErrorBiblioteca as error:
        print("con", texto, "->", type(error).__name__, ":", error)

```

Salida:

```

con 12345 -> ErrorDeDatos : El DNI debe tener 8 digitos
con 99999999 -> ErrorDeDatos : No hay ningun usuario con el DNI 99999999
con 97884376049470 -> ErrorDeDatos : El DNI debe tener 8 digitos

```

```python

try:
    mi_biblioteca.libro("9780000000000")
except errores.ErrorDeDatos as error:
    print("ErrorDeDatos:", error)

try:
    mi_biblioteca.libro("12")
except errores.ErrorDeDatos as error:
    print("ErrorDeDatos:", error)

```

Salida:

```

ErrorDeDatos: No hay ningun libro con el ISBN 9780000000000
ErrorDeDatos: El ISBN debe tener 13 digitos

```

## 10. La recursion

Hay dos funciones que se llaman a si mismas, las dos en `libros.py`.

La primera recorre el catalogo para armar la lista de datos:

```python
def datos_del_catalogo(libros):
    if len(libros) == 0:
        return []
    primer_libro = libros[0]
    libros_que_faltan = libros[1:]
    return [primer_libro.datos_para_pantalla()] + datos_del_catalogo(libros_que_faltan)
```

La idea es siempre la misma:

1. Si la lista esta vacia, no hay nada que hacer. Ese es el caso base, el que corta la recursion.
2. Si no, se toma el primer libro y se junta con lo que salga de llamar a la misma funcion con el resto.

Cada llamada recibe una lista mas corta, asi que tarde o temprano llega a la lista vacia.

```python

primeros_tres = mi_biblioteca.todos_los_libros()[:3]

print("con la lista vacia:", libros.datos_del_catalogo([]))
print("con 1 libro:", len(libros.datos_del_catalogo(primeros_tres[:1])), "diccionario")
print("con 3 libros:", len(libros.datos_del_catalogo(primeros_tres)), "diccionarios")
print("con los 22:", len(libros.datos_del_catalogo(mi_biblioteca.todos_los_libros())), "diccionarios")

```

Salida:

```

con la lista vacia: []
con 1 libro: 1 diccionario
con 3 libros: 3 diccionarios
con los 22: 22 diccionarios

```

La segunda busca por un pedazo de texto:

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

Es la misma forma, con una decision en el medio: si el primer libro coincide se queda en la lista, si no se descarta.

Y `coincide_con_la_busqueda()` es la que mira si el texto esta en el titulo, en el autor o en la categoria, todo en minusculas para que no importe si escriben con mayusculas o sin tildes.

```python

encontrados = libros.buscar_por_texto(mi_biblioteca.todos_los_libros(), "ma")

print("con 'ma' salieron", len(encontrados), "libros:")
for libro in encontrados:
    print("  ", libro.titulo(), "|", libro.autor())

```

Salida:

```

con 'ma' salieron 14 libros:
   Cien años de soledad | Gabriel Garcia Marquez
   Maze Runner: Correr o morir | James Dashner
   Don Quijote de la Mancha | Miguel de Cervantes
   La ciudad y los perros | Mario Vargas Llosa
   El sistema jurídico: Introducción al derecho | Marcial Antonio Rubio Correa
   Tradiciones peruanas | Ricardo Palma
   El capital: Crítica de la economía política (Tomo I) | Karl Marx
   Matemáticas 1 | Miguel Angel Gonzaga Ramirez, Josué Aguirre Enciso, Richard Santiago Quispe Rivas
   Cálculo Diferencial | Nancy Edith Saravia Molina, Cecilia Gaita Iparraguirre, Diana Bances Vento, Jack Arce Flores, Wilson Edwar Díaz Cajo
   Eloquent JavaScript | Marijn Haverbeke
   Aplicaciones de Inteligencia Artificial en la Educación Superior Universitaria | Gloria Teresita Huamaní Huamaní, Paul Miller Tocto Inga
   Franquicias imaginarias: las opciones estéticas en las artes plásticas en el Perú de fin de siglo | Max Hernández Calvo, Jorge Villacorta Chávez
   Imaginación visual y cultura en el Perú | Gisela Cánepa (Editora)
   Deus absconditus: retrospectiva de Manuel Moncloa 1980-2011 | Gustavo Buntinx

```

```python

for texto in ["arte", "vargas", "fisica", "xyz", ""]:
    encontrados = libros.buscar_por_texto(mi_biblioteca.todos_los_libros(), texto)
    print("'" + texto + "' ->", len(encontrados), "libros")

```

Salida:

```

'arte' -> 4 libros
'vargas' -> 1 libros
'fisica' -> 1 libros
'xyz' -> 0 libros
'' -> 0 libros

```

Con `xyz` no sale ninguno y con el texto vacio tampoco: `coincide_con_la_busqueda()` devuelve `False` si no escribieron nada, para no devolver el catalogo entero por error.

## 11. Los menus

Todo lo de la consola esta en `menu.py`. Son tres menus:

**Menu de acceso**, el primero que se ve:

```
MENU DE ACCESO
1) Entrar con mi DNI
0) Salir
```

**Menu de sesion**, el que se abre despues de entrar. Es el mismo para todos, pero la opcion 5 solo se imprime si el usuario puede administrar:

```
MENU DE ESTUDIANTE            MENU DE ADMINISTRADOR
1) Ver el catalogo            1) Ver el catalogo
2) Buscar un libro            2) Buscar un libro
3) Ver un libro por ISBN      3) Ver un libro por ISBN
4) Mi membresia               4) Mi membresia
0) Cerrar sesion              5) Ver los usuarios
                              0) Cerrar sesion
```

El titulo del menu sale del tipo de usuario, por eso dice `MENU DE ESTUDIANTE`, `MENU DE DOCENTE` o `MENU DE ADMINISTRADOR`.

Las tres cosas que hacen que el menu no se rompa:

- es un `while True`, asi que vuelve a mostrar las opciones hasta que elijan `0`;
- si escriben cualquier otra cosa, dice "Esa opcion no existe" y sigue;
- cada accion esta dentro de un `try` que atrapa `ErrorBiblioteca`, asi que un DNI o un ISBN mal escrito se muestra como un mensaje y no como un traceback.

```python

print("las opciones del menu se imprimen segun el usuario:")
print()
for dni in ["11111111", "33333333"]:
    usuario = mi_biblioteca.usuario(dni)
    print("MENU DE " + usuario.tipo().upper())
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

las opciones del menu se imprimen segun el usuario:

MENU DE ESTUDIANTE
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

## 12. Donde cambiar cada cosa

| si quiero cambiar...                             | voy a                                                |
| ------------------------------------------------ | ---------------------------------------------------- |
| el nombre de la biblioteca o el lema             | `configuracion.py`, arriba                           |
| las secciones y sus nombres                      | `configuracion.py`, el diccionario `SECCIONES`       |
| cuantos estantes hay                             | `configuracion.py`, `CANTIDAD_DE_ESTANTES`           |
| los tipos de usuario que se aceptan              | `configuracion.py`, `TIPOS_DE_USUARIO`               |
| cuantos digitos tiene el DNI o el ISBN           | `utilidades.py`                                      |
| que campos se revisan al crear un libro          | `libros.py`, el metodo `revisar_datos()`             |
| que datos salen en la pantalla de un libro       | `libros.py`, el metodo `datos_para_pantalla()`       |
| que datos salen en la pantalla de la membresia   | `usuarios.py`, el metodo `datos_de_membresia()`      |
| que busca la busqueda (titulo, autor, categoria) | `libros.py`, la funcion `coincide_con_la_busqueda()` |
| las opciones de los menus                        | `menu.py`, la funcion `menu_de_sesion()`             |
| los libros y los usuarios                        | los JSON de `datos/`                                 |

```python

print("asi se cambia el nombre de la biblioteca sin tocar el resto del codigo:")
print("ahora dice:", configuracion.NOMBRE_BIBLIOTECA)

configuracion.NOMBRE_BIBLIOTECA = "Biblioteca de la universidad"
otra_biblioteca = biblioteca.Biblioteca()
print("ahora dice:", otra_biblioteca.resumen()["biblioteca"])

```

Salida:

```

asi se cambia el nombre de la biblioteca sin tocar el resto del codigo:
ahora dice: Biblioteca IDAT
ahora dice: Biblioteca de la universidad

```

## 13. Errores comunes

**Poner tildes o enie en el codigo.** En los JSON si van, porque son los nombres reales de los libros. En el codigo no: se escribe `anio`, `informacion`, `catalogo`, `prestamo`. Si el profesor busca una palabra en el codigo, la tiene que encontrar sin que el teclado cambie el resultado.

**Buscar un libro recorriendo la lista.** El catalogo es un diccionario con el ISBN como clave, asi que `self._catalogo[isbn]` lo encuentra directo.

**Cambiar un atributo desde afuera.** `libro._titulo = "otro"` funciona en Python, pero se salta todas las revisiones. Para eso estan los metodos.

**Devolver `True` o `False` a la pantalla.** La pantalla muestra texto. Por eso existe `utilidades.si_o_no()`, que convierte `True` en `"Si"` y `False` en `"No"`.

**Olvidar el caso base en una funcion recursiva.** Sin el `if len(libros) == 0: return []` la funcion sigue llamandose con una lista cada vez mas corta hasta que intenta leer `lista[0]` de una lista vacia y salta un `IndexError`. Y si la lista no se achica, lo que salta es un `RecursionError`.

**Atrapar `Exception` a secas.** Si se atrapa todo, tambien se tapa un error de nuestro propio codigo y nunca nos enteramos. Se atrapa `ErrorBiblioteca`.

```python

print("el caso base corta la recursion:")
print("lista vacia ->", libros.datos_del_catalogo([]))

def sin_caso_base(lista):
    return [lista[0]] + sin_caso_base(lista[1:])

print()
print("y sin caso base, al llegar a la lista vacia pasa esto:")
try:
    sin_caso_base(mi_biblioteca.todos_los_libros())
except IndexError as error:
    print("IndexError:", error)

```

Salida:

```

el caso base corta la recursion:
lista vacia -> []

y sin caso base, al llegar a la lista vacia pasa esto:
IndexError: list index out of range

```

## 14. Lo que falta para llegar a la version final

La version final tiene las mismas carpetas y los mismos modulos, y agrega lo que aca no esta:

| que falta aca                      | donde esta en la version final                                                  |
| ---------------------------------- | ------------------------------------------------------------------------------- |
| los prestamos y las devoluciones   | `modulos/prestamos.py` y los metodos `prestar()` y `devolver()` de `Biblioteca` |
| el archivo `prestamos.json`        | `datos/prestamos.json`                                                          |
| guardar los cambios en los JSON    | `configuracion.guardar_archivo()` y `Biblioteca.guardar_datos()`                |
| agregar libros nuevos              | `Biblioteca.agregar_libro()`                                                    |
| editar la informacion de un libro  | `Libro.cambiar_datos()` y `Biblioteca.editar_libro()`                           |
| renovar la membresia               | `Usuario.renovar_membresia()`                                                   |
| dar de baja y reactivar un usuario | `Usuario.dar_de_baja()` y `Usuario.reactivar()`                                 |
| los reportes en matriz             | `modulos/reportes.py`                                                           |
| los dias de prestamo               | `configuracion.DIAS_DE_PRESTAMO`, que vale 15                                   |

En la version final no hay menu de consola: todo son funciones que devuelven listas y diccionarios, listos para ponerlos en etiquetas y botones. Se prueba con `pruebas.py`.

Y en las dos versiones falta lo mismo: las pantallas `.ui` en la carpeta `interfaces/`, que se hacen con Qt Designer.

```python

print("lo que tiene esta version:")
print("  libros:", len(mi_biblioteca.todos_los_libros()))
print("  usuarios:", len(mi_biblioteca.todos_los_usuarios()))
print("  funciones recursivas: datos_del_catalogo y buscar_por_texto")
print("  clases:", len(["Libro", "Usuario", "Administrador", "Biblioteca",
                       "ErrorBiblioteca", "ErrorDeDatos", "ErrorDeArchivo"]))
print()
print("lo que no tiene: prestamos, devoluciones, guardado, edicion ni reportes")

```

Salida:

```

lo que tiene esta version:
  libros: 22
  usuarios: 13
  funciones recursivas: datos_del_catalogo y buscar_por_texto
  clases: 7

lo que no tiene: prestamos, devoluciones, guardado, edicion ni reportes

```
