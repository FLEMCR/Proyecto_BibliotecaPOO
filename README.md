# Parcial de POO - sistema de biblioteca

Trabajo grupal del parcial de Programacion Orientada a Objetos (IDAT, 2do ciclo). Es un
sistema de biblioteca universitaria que corre en consola: catalogo de libros, miembros con
membresia, consulta por categoria con una funcion recursiva, tres matrices de datos y un menu
de gestion para el administrador. Los datos estan en dos archivos JSON, se pueden editar a
mano y el programa los vuelve a leer al arrancar.

**Es un avance.** La parte de prestamos, devoluciones y multas todavia no esta hecha: esta
quitada del menu a proposito y se retoma en la siguiente entrega. Abajo, en "Lo que falta",
esta la lista completa y que piezas ya existen para completarla.

Todo es Python estandar, no hay que instalar nada.

**Ojo antes de presentar:** en `modulos/config.py` estan los nombres provisionales
`nombre_biblioteca` y `lema`, hay que cambiarlos.

## Que hay en esta carpeta

| Carpeta o archivo                   | Que es                                                                                       |
| ----------------------------------- | -------------------------------------------------------------------------------------------- |
| `main.py`                           | arranca el programa: portada, biblioteca y menu                                              |
| `modulos/`                          | el codigo, un archivo por tema                                                               |
| `modulos/datos/`                    | los dos JSON con los datos de ejemplo                                                        |
| `cuadernos/Guia_del_proyecto.ipynb` | la guia que explica el programa bloque por bloque                                            |
| `cuadernos/Guia_del_proyecto.md`    | la misma guia en texto plano                                                                 |
| `h_prestamos_sin_usar.json`         | el historial de prestamos del equipo, guardado aparte mientras los prestamos no esten hechos |
| `3.1. Rubrica Parcial_IDAT_POO.pdf` | la rubrica con la que nos califican                                                          |

## Como se ejecuta

```
python3 main.py
```

El ingreso es solo con DNI. Para ver el menu de administracion hay que entrar con
`72345678` (Jorge Huaman), que es el unico miembro de tipo Administrador. Con cualquier
otro DNI activo se abre el menu de miembro, y la opcion 2 del menu principal entra como
invitado (solo puede consultar el catalogo y buscar por categoria).

Miembros de ejemplo para probar:

| DNI        | Quien es                    | Que abre                                         |
| ---------- | --------------------------- | ------------------------------------------------ |
| `72345678` | Jorge Huaman, administrador | estado, miembros, matrices y busqueda, guardar   |
| `75678901` | Sofia Rojas, estudiante     | catalogo, busqueda por categoria, mi membresia   |
| `70445566` | Luis Ramos, docente         | el mismo menu de miembro, con limite 5 y 20 dias |
| `70778899` | Rosa Palomino, dada de baja | no entra, el programa lo avisa                   |
| `123`      | DNI de 3 cifras             | no entra: "El DNI debe tener 8 digitos"          |

### Ensayar la demo sin escribir

Se le puede pasar la entrada por tubo. El primer ENTER es el de la portada, y despues de cada
accion hay que dejar un ENTER vacio porque todas terminan en `pausa()`. Al cerrar sesion no
hay pausa, asi que el `0` del menu de adentro y el `0` del menu de acceso van seguidos:

```
printf '\n1\n72345678\n1\n\n2\n\n3\n1\n\n2\n\n3\n\n4\nLiteratura\n\n0\n4\nn\n\n0\n0\n' | python3 main.py
printf '\n1\n75678901\n1\n\n2\nNarrativa\n\n3\n\n0\n0\n' | python3 main.py
printf '\n2\n1\n\n2\nLiteratura\n\n0\n0\n' | python3 main.py
printf '\n1\n70778899\n0\n' | python3 main.py
printf '\n1\n123\n1\n72345678\n1\n\n0\n0\n' | python3 main.py
```

Son, en orden: administrador que recorre el estado, los miembros, las tres matrices, la
busqueda recursiva y el guardado (diciendo que no); estudiante que mira el catalogo, busca por
categoria y ve su membresia; invitado; un miembro dado de baja; y un DNI invalido seguido de
uno correcto.

**La secuencia tiene que terminar con la opcion 0**, o sea saliendo por las buenas. Como
`main.py` no atrapa `EOFError`, si los ENTER se acaban antes de tiempo el programa muestra la
traza y termina con codigo 1; eso quiere decir que la secuencia estaba mal contada, no que el
programa este mal. Si se pone un ENTER de mas o de menos, el programa no se cae: muestra
`Opcion no valida` y vuelve a pedir, que es justo lo que hace `leer_opcion` para no confiar
nunca en lo que se escribe.

## Los modulos

| Archivo         | Lineas | Que hace                                                         |
| --------------- | ------ | ---------------------------------------------------------------- |
| `config.py`     | 62     | rutas de los JSON, reglas por tipo de miembro, leer y guardar    |
| `errores.py`    | 10     | las 3 excepciones del sistema                                    |
| `utilidades.py` | 54     | titulo, pausa, validar DNI e ISBN, responder si/no, fechas       |
| `usuarios.py`   | 184    | Membresia y sus 4 subclases, Usuario, y las dos fabricas         |
| `libros.py`     | 187    | Libro, las 3 matrices y las 3 funciones recursivas de categorias |
| `biblioteca.py` | 96     | une todo: carga los JSON, resume, guarda                         |
| `menu.py`       | 253    | las tablas de opciones y todas las acciones                      |
| `main.py`       | 12     | arranca: portada, biblioteca y menu                              |

En total 858 lineas repartidas en 11 clases, 56 metodos y 38 funciones. No hay ninguna
variable `global` ni librerias externas. En el codigo solo hay un comentario y un ejemplo de
recursion comentado, los dos en `utilidades.py`; todo lo demas esta explicado en la guia de
`cuadernos/`.

El manejo de errores esta en dos lugares: `menu_principal` atrapa `DatosInvalidosError` al leer
el DNI y vuelve a mostrar el menu, y `Biblioteca.cargar_datos` atrapa `ValueError` para
convertir un JSON roto en `ArchivoDatosError`. `main.py` no atrapa nada a proposito: si pasa
algo que no esta previsto se ve la traza de Python con el archivo y la linea.

## Los datos

- `modulos/datos/libros.json`: 7 titulos, con categoria, seccion, estante, ejemplares y
  disponibles.
- `modulos/datos/miembros.json`: 10 miembros, con tipo, vencimiento de membresia y si esta
  activo.

Cuando el programa arranca lee los dos y arma los objetos. Al elegir "Guardar cambios" en el
menu de administracion se reescriben con lo que haya en memoria, y por eso pide confirmacion
antes.

Un detalle de los datos: en `libros.json` algunos titulos tienen menos
`disponibles_prestamo` que `ejemplares` (por ejemplo Eloquent JavaScript tiene 2 ejemplares y
1 disponible). Venia del historial de prestamos del equipo. Como los prestamos todavia no
estan hechos, ese numero hoy simplemente se muestra y alimenta las matrices.

## Que pide la rubrica y donde esta

| Criterio                        | Puntos | Donde se ve                                                                                                                                                                                                   |
| ------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Implementacion de funcionalidad | 5      | menus de miembro, invitado y administrador; consulta de catalogo, busqueda por categoria, ficha de membresia, estado y guardado. **Queda corto a proposito: faltan prestamos y el alta y baja desde el menu** |
| Aplicacion de conceptos de POO  | 5      | atributos privados con `_`, metodos publicos, encapsulacion en `Libro.prestar_uno()`, herencia de tres niveles y polimorfismo en `describir()`                                                                |
| Uso de funciones y metodos      | 4      | 38 funciones sueltas y 56 metodos, 3 excepciones propias lanzadas y atrapadas donde corresponde, y ningun `global`                                                                                            |
| Matrices y recursividad         | 6      | 3 matrices en el menu de administracion y 3 funciones recursivas sobre categorias                                                                                                                             |

Las funciones recursivas son `niveles_categoria`, `pertenece_a_categoria` y
`buscar_por_categoria`, todas en `libros.py` y todas con su caso base. En `utilidades.py`
quedo ademas una cuenta regresiva comentada, como ejemplo basico del tema.

Las matrices son disponibilidad por seccion y estante, titulos por seccion y estante, y
totales por categoria.

La herencia esta en `Membresia` -> `Estudiante`, `Docente`, `Invitado`, y `Administrador`
hereda de `Docente`. El polimorfismo se ve en `accion_mi_membresia`, que usa las mismas siete
lineas para los cuatro tipos, y en `Invitado.describir()`, que es la unica subclase que
reescribe un metodo.

## Lo que falta (es un avance)

- Prestar y devolver libros. `Libro.prestar_uno()` y `Libro.devolver_uno()` ya estan escritos
  y probados, con la validacion y el error si no quedan ejemplares. Falta la clase `Prestamo`,
  el gestor y las dos acciones del menu.
- Historial y multas por retraso. `Membresia.dias_prestamo()` y `multa_por_dia()` ya dan los
  numeros por tipo y `utilidades.sumar_dias()` calcula el vencimiento; falta guardar la fecha
  real de cada prestamo y restar fechas.
- Registrar y actualizar libros desde el menu: hoy el catalogo solo se edita cambiando el
  JSON. `utilidades.validar_isbn()` y el constructor de `Libro` con valores por defecto ya
  estan para eso.
- Dar de alta, de baja o renovar la membresia de un miembro desde el menu. Los metodos
  `dar_de_baja()`, `reactivar()`, `renovar_membresia()` y `cancelar_membresia()` ya existen en
  `Usuario`, falta la opcion del menu que los llame.
- Buscar libros por titulo o autor (solo hay busqueda por categoria).
- El tope de multa por prestamo.
- El nombre y el lema definitivos en `config.py`.

## Quien hizo que

- A: `modulos/datos/`, `config.py`, `errores.py`, `utilidades.py`
- B: `usuarios.py`, `libros.py`
- C: `biblioteca.py`
- D: `menu.py`, `main.py`, `README.md`

Cronograma: del sabado 3 al viernes 16 de octubre de 2026.
