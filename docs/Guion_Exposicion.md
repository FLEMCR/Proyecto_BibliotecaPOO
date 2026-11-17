# Guion de exposición

**Sistema de Gestión de Biblioteca General POSTDATA**

- Exposición: **12 minutos** en 4 bloques de 3 minutos.
- Preguntas: **5 minutos** con el banco de respuestas al final.
- Total previsto: **17 minutos** (el límite del equipo es 22).
- La rúbrica final indica **3 integrantes**; los 4 bloques son una división del tiempo, no una cantidad de personas.
- Mensaje central: **interfaz gráfica, reglas automáticas y fecha límite fija de 15 días sin calendario; vencido bloquea nuevos préstamos y no hay multas.**
- Lema: **“Un libro es un viaje de ida y vuelta: llévalo contigo y devuélvelo cuando el viaje haya terminado.”**

---

## Bloque 1 — Presentación y alcance (0:00–3:00)

**Diapositivas 1–4. Objetivo:** explicar qué se construyó y por qué está organizado así.

**0:00–0:20 — Apertura**

> “Buenos días. Presentamos el sistema de gestión de la Biblioteca General POSTDATA, desarrollado en Python con PyQt5. Es una aplicación gráfica: `main.py` es la única entrada y desde ahí se abre el acceso, el panel principal y el resto de las páginas.”

*Acción:* mostrar la diapositiva 1 y, si hay proyección, abrir la app en `python3 main.py`.

**0:20–1:10 — Alcance**

> “El alcance objetivo es cubrir lo esencial de una biblioteca universitaria: alta de usuarios, CRUD de libros desde el catálogo, préstamos, devoluciones, membresía y reportes. Todo se guarda en JSON y se recarga al iniciar. Quedaron fuera las multas, los beneficios de membresía y, por requerimiento del proyecto, el calendario.”

*Acción:* señalar las dos columnas de “Sí incluye / No incluye” de la diapositiva 2.

**1:10–2:00 — Problema y solución**

> “El problema era el registro manual: era difícil saber cuántos ejemplares quedaban, quién tenía un libro y cuándo debía devolverlo. La solución combina una interfaz clara con reglas automáticas: al prestar baja el stock, al devolver lo repone, y la fecha límite se calcula sola.”

**2:00–3:00 — Arquitectura**

> “Sepamos las responsabilidades. En `core/` está la lógica pura, sin importar PyQt5: libros, usuarios, préstamos, biblioteca y reportes. En `ui/` están los siete formularios, cada uno con su `.ui` de Qt Designer y su `.py` de señales. En `data/` están los JSON. La clase `Biblioteca` es el controlador: valida y coordina, mientras la interfaz solo muestra y llama métodos.”

*Acción:* recorrer el mapa de carpetas de la diapositiva 4.

---

## Bloque 2 — POO e interfaz (3:00–6:00)

**Diapositivas 5–7. Objetivo:** evidenciar POO, componentes y el cambio de calendario por fecha automática.

**3:00–4:00 — POO aplicada**

> “Aplicamos los cuatro principios. Encapsulación: los atributos son privados y se accede por métodos como `dni()` o `isbn()`, con validación en el constructor. Herencia: `Administrador` hereda de `Usuario`. Polimorfismo: `puede_administrar()` devuelve `False` en `Usuario` y `True` en `Administrador`; la misma llamada produce un comportamiento distinto. Abstracción: las fábricas `crear_libro`, `crear_usuario` y `crear_prestamo` ocultan cómo se construye cada objeto.”

**4:00–5:00 — Componentes básicos**

> “La interfaz se diseñó en Qt Designer y se carga con `uic.loadUi()`. Usamos Labels, Line Edits, un Text Edit para los reportes, Push Buttons, Radio Buttons para elegir el tipo de reporte y Checkboxes. Cada botón se conecta con `connect()` a un slot. El estilo oscuro vive en `app.qss`, organizado por secciones para poder editarlo rápido.”

*Acción:* mostrar el inicio con el saludo `Hola, nombre` y las tarjetas en columna.

**5:00–6:00 — Componentes avanzados y fecha**

> “También usamos Spin Box, List Widget, Combo Box, Table Widget, Stacked Widget y Splitter. Un punto importante es la fecha: originalmente se podía usar un calendario, pero el requerimiento final fija 15 días desde el inicio del préstamo. Por eso el plazo y la fecha límite son solo texto: se calculan con `date.today() + timedelta(days=15)` y el usuario no tiene ningún control para cambiarlos.”

*Acción:* abrir “Registrar préstamo” y señalar la fecha límite calculada.

---

## Bloque 3 — Flujo de préstamo y reportes (6:00–9:00)

**Diapositivas 8–10. Objetivo:** mostrar el flujo completo y profundizar en matrices y recursividad.

**6:00–7:20 — Flujo de préstamo**

> “Desde la ficha de un libro, el botón **Registrar préstamo** emite la señal `prestamo_solicitado(isbn)`. El panel principal escucha esa señal, navega a la página de préstamos y llama a `cargar_isbn()`, que completa el campo y consulta el libro. Al confirmar, `Biblioteca.prestar()` valida en este orden: usuario activo con membresía vigente, préstamo vencido, préstamo activo y stock disponible. Si hay un vencido, se muestra: ‘El usuario tiene un préstamo vencido; debe devolverlo antes de pedir otro libro’. No hay multa: solo se bloquea hasta la devolución.”

*Acción:* demo rápida: catálogo → ficha → préstamo → mensaje de validación.

**7:20–8:30 — Reportes en dos tablas**

> “La página Reportes muestra primero un resumen general y después dos tablas separadas por una línea. La primera es el historial de préstamos: ID, DNI, usuario, ISBN, libro, fecha de préstamo, fecha límite, devolución y estado; ahí se ve quién prestó qué. La segunda es el inventario: todos los libros con sus ejemplares, cuántos están prestados y cuántos disponibles. El resumen que antes estaba en Inicio se movió acá.”

*Acción:* abrir Reportes y recorrer las dos tablas de arriba abajo.

**8:30–9:00 — Recursividad, generadores y cierres**

> “Aunque la vista ya no muestra la matriz, la lógica sigue en `core/reportes.py` para evidenciar el tema del sílabo. El total de cada fila se calcula con `sumar_fila()`: caso base cuando el índice llega al final, y caso recursivo sumando el valor actual más la llamada al siguiente índice. Al llegar al caso base, la pila de llamadas se desapila en orden LIFO. Además, `filas_del_reporte()` es un generador que entrega cada fila con `yield`, y el `lambda` que elige `seccion()` o `categoria()` actúa como cierre: recuerda la decisión de `tipo` y se lo pasamos a `construir_matriz()`. Toda esa matriz se escribe al exportar `data/reporte.txt`.”

---

## Bloque 4 — Persistencia, calidad y cierre (9:00–12:00)

**Diapositivas 11–13. Objetivo:** cerrar con datos, errores, pruebas y una demo final.

**9:00–10:30 — Persistencia, regex y errores**

> “La modernización permitida fue `pathlib`: las rutas se construyen con `Path` y los JSON se leen y escriben con `read_text` y `write_text` en UTF-8. La validación de texto usa expresiones regulares: `PATRON_DNI` exige 8 dígitos y `PATRON_ISBN` exige 13, ambos con `fullmatch`. Las fechas se convierten con `convertir_fecha()`, que comprueba formato y existencia real. Los errores de reglas se lanzan como `ErrorDeDatos`, para que la interfaz muestre un mensaje entendible en vez de cortarse.”

**10:30–11:10 — Calidad y verificación**

> “Verificamos el proyecto con `compileall`, cargamos los siete archivos `.ui` con `uic.loadUi`, ejecutamos 20 pruebas unitarias en modo offscreen y hicimos un smoke test de la interfaz. En ese smoke test confirmamos que el plazo dice solo ‘Plazo’, que la fecha límite aparece como texto a 15 días y que ya no existe ningún calendario ni selector. Firebase quedó preparado en `integracion/firebase_sync.py`, sin importarse en `main.py`.”

**11:10–12:00 — Demo y cierre**

> “Para cerrar, mostramos el flujo completo: acceso con DNI, catálogo, ficha, préstamo con fecha automática, devolución y reportes con sus dos tablas. La idea final es que el sistema no solo registra datos: aplica las reglas de negocio y deja evidencia de los temas de la unidad. Quedamos atentos a sus preguntas.”

*Acción:* ejecutar el flujo en 40 segundos y quedar en la diapositiva 13 durante el Q&A.

---

## Banco de preguntas técnicas (5 minutos)

1. **¿Por qué `main.py` es la única entrada?** Porque crea la `QApplication`, carga el QSS, instancia `Biblioteca` y coordina acceso y panel principal. Evita tener scripts sueltos con estados diferentes.

2. **¿Cómo se logra la modularidad?** `core/` no importa PyQt5 y contiene las reglas; `ui/` contiene vista y señales; `data/` guarda JSON. `Biblioteca` es el único controlador de alto nivel.

3. **¿Dónde se aplica encapsulamiento?** En atributos como `_dni`, `_isbn`, `_fecha_limite` y `_estado`, con métodos públicos que validan antes de construir o devolver valores.

4. **¿Qué diferencia hay entre herencia y polimorfismo aquí?** Herencia: `Administrador` obtiene los atributos de `Usuario`. Polimorfismo: `puede_administrar()` se comporta distinto según el objeto, aunque se llame igual.

5. **¿Qué hace la fábrica `crear_usuario()`?** Decide entre `Usuario` y `Administrador` según el tipo guardado en JSON. Lo mismo hacen `crear_libro()` y `crear_prestamo()`.

6. **¿Por qué no se usa Calendar Widget si el sílabo lo menciona?** Porque el requerimiento del proyecto fija siempre 15 días. El plazo y la fecha límite se muestran como texto calculado, sin calendario ni selector que permita elegir otra fecha.

7. **¿Cómo se calcula la fecha límite?** En `Biblioteca.prestar()`: `hoy = date.today()` y `fecha_limite = hoy + timedelta(days=configuracion.DIAS_DE_PRESTAMO)`. `Prestamo` además valida que no supere ese plazo.

8. **¿Qué significa que un préstamo esté vencido?** `esta_vencido()` exige que esté activo y que la fecha actual sea mayor a la fecha límite. Un préstamo devuelto nunca cuenta como vencido.

9. **¿Qué ocurre si el usuario tiene un vencido?** `prestar()` lo detecta antes de revisar los préstamos activos y lanza: “El usuario tiene un préstamo vencido; debe devolverlo antes de pedir otro libro”. Se habilita recién al devolverlo.

10. **¿Cómo se actualiza el stock?** `Biblioteca.prestar()` llama a `libro.prestar_ejemplar()` y `devolver()` llama a `libro.devolver_ejemplar()`. Después guarda libros y préstamos en JSON.

11. **¿Cómo se arma la matriz del reporte?** Filas = secciones o categorías, columnas = 3 estantes. Se inicializa en ceros y cada libro suma sus `disponibles()` en `[fila][estante - 1]`. Hoy no se ve en pantalla porque Reportes muestra tablas, pero se exporta en `data/reporte.txt`.

12. **Explique la recursividad de `sumar_fila()`.** Caso base: si `indice >= len(fila)`, devuelve 0. Caso recursivo: devuelve `fila[indice] + sumar_fila(fila, indice + 1)`. Cada llamada se apila y se desapila al llegar al caso base (LIFO).

13. **¿Para qué sirve `filas_del_reporte()`?** Es un generador: con `yield` entrega índice, etiqueta, valores y total uno por uno. Permite reutilizar el mismo recorrido en el texto exportado, que además incluye el historial y el inventario.

14. **¿Dónde está el cierre lambda?** En `reportes.generar()`: `obtener_fila = lambda libro: libro.categoria()` o `libro.seccion()`. Esa función recuerda el `tipo` elegido y se pasa a `construir_matriz()`.

15. **¿Cómo se validan DNI, ISBN y fechas?** Con `PATRON_DNI = \d{8}`, `PATRON_ISBN = \d{13}` y `fullmatch()`. `convertir_fecha()` valida el formato `AAAA-MM-DD` y que la fecha exista; los fallos lanzan `ErrorDeDatos`.

16. **¿Cómo se guardan los datos y qué pasa con los modos de archivo?** Usamos `pathlib` y `read_text`/`write_text` con UTF-8 sobre JSON. En términos generales, `r` lee, `w` reemplaza, `a` agrega y `b` es binario; este proyecto usa lectura y escritura completa de JSON, sin modo binario.

17. **¿Cómo renueva el administrador una membresía?** En la página “Usuarios” selecciona una fila y pulsa **Renovar membresía**. `Biblioteca.renovar_membresia()` llama a `Usuario.renovar_membresia()`, que toma la fecha más tardía entre hoy y el vencimiento actual, le suma 3 meses con `sumar_meses()` y guarda el JSON. Así una renovación nunca acorta una membresía vigente. El administrador principal tiene su propio vencimiento a 10 años en `data/usuarios.json` para no perder el acceso.
