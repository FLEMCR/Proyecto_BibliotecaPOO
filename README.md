# Parcial de POO - sistema de biblioteca

Trabajo grupal del parcial de Programacion Orientada a Objetos (IDAT, 2do ciclo). Es un
sistema de biblioteca universitaria que corre en consola: catalogo de libros, miembros con
membresia, consulta por categoria con una funcion recursiva, tres matrices de datos y un menu
de gestion para el administrador. Los datos estan en dos archivos JSON, se pueden editar a
mano y el programa los vuelve a leer al arrancar.

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

## Los datos

- `modulos/datos/libros.json`: 7 titulos, con categoria, seccion, estante, ejemplares y
  disponibles.
- `modulos/datos/miembros.json`: 10 miembros, con tipo, vencimiento de membresia y si esta
  activo.

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
