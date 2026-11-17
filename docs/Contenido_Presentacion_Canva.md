# Contenido para presentación en Canva

**Sistema de Biblioteca General POSTDATA — Programación Orientada a Objetos**

- Formato: 16:9, tema oscuro, acento rojo `#ff5a5a`.
- Extensión: **13 diapositivas** (límite de la rúbrica final: máximo 15).
- Tiempo: **12 minutos de exposición + 5 minutos de preguntas** = 17 minutos (límite del equipo: 22).
- Equipo: la rúbrica final indica **3 integrantes**; el guion se organiza en 4 bloques de 3 minutos para hacer más clara la demo.
- Regla nueva a destacar: **no hay calendario**. La fecha límite se calcula sola a **15 días** del inicio del préstamo y un préstamo vencido bloquea nuevos préstamos hasta devolverlo. No se cobran multas.
- Lema actual: **“Un libro es un viaje de ida y vuelta: llévalo contigo y devuélvelo cuando el viaje haya terminado.”**

> Recomendación de diseño: máximo 6 líneas por diapositiva, una idea por diapositiva, iconos simples y capturas reales de la app en las diapositivas 8, 9 y 13.

---

## Diapositivas

| # | Título | Texto listo para Canva | Visual sugerido | Tiempo |
| --- | --- | --- | --- | --- |
| 1 | **Sistema de Gestión de Biblioteca** | Biblioteca General POSTDATA<br>Programación Orientada a Objetos · IDAT<br>Proyecto gráfico con PyQt5<br>“Un libro es un viaje de ida y vuelta…” | Portada oscura, icono de libro y logo del curso | 0:20 |
| 2 | **Alcance objetivo** | Una sola entrada: `main.py`<br>CRUD de libros, catálogo, préstamos, devoluciones, membresía y reportes<br>Datos persistentes en JSON<br>Fuera de alcance: multas, beneficios de membresía y calendario | Esquema de alcance: “Sí incluye” vs. “No incluye” | 0:50 |
| 3 | **Problema → solución** | Problema: registrar libros y controlar préstamos a mano es lento y propenso a errores<br>Solución: interfaz intuitiva + reglas automáticas + reportes<br>Resultado: stock y vencimientos siempre visibles | Flecha grande del problema a la solución | 0:50 |
| 4 | **Arquitectura modular** | `main.py` → acceso → panel principal<br>`core/`: reglas de negocio, sin PyQt5<br>`ui/`: ventanas `.ui` + lógica `.py`<br>`data/`: libros, usuarios y préstamos<br>`Biblioteca` coordina todo | Mapa de carpetas con flechas | 1:00 |
| 5 | **POO aplicada** | Encapsulación: atributos privados y validación en constructores<br>Herencia: `Administrador` extiende `Usuario`<br>Polimorfismo: `puede_administrar()` responde distinto<br>Abstracción: fábricas `crear_libro`, `crear_usuario`, `crear_prestamo` | Diagrama de clases simple | 1:00 |
| 6 | **Interfaz: componentes básicos** | Qt Designer dibuja el `.ui`; PyQt5 carga con `uic.loadUi()`<br>Labels, Line Edits, Text Edit, Push Buttons y Checkboxes<br>Señales y slots conectan cada acción<br>QSS oscuro organizado por secciones | Captura del inicio: solo texto arriba y espacio libre para una imagen | 1:00 |
| 7 | **Componentes avanzados y fecha** | Spin Box, List Widget, Combo Box, Table Widget, Stacked Widget y Splitter<br>El plazo se muestra como texto, sin calendario ni selector<br>Fecha límite = inicio + 15 días | Captura de “Registrar préstamo” con la fecha calculada | 1:00 |
| 8 | **Flujo de préstamo** | La ficha del catálogo tiene **Registrar préstamo**<br>Emite `prestamo_solicitado(isbn)` y carga el ISBN<br>`Biblioteca.prestar()` valida usuario, vencidos, activos y stock<br>Vencido → bloqueo; devuelto → habilitado | Captura del catálogo + flecha al formulario | 1:20 |
| 9 | **Reportes: historial e inventario** | Resumen general arriba<br>Tabla 1: quién prestó qué libro, DNI, ISBN, fechas y estado<br>Tabla 2: todos los libros con ejemplares, prestados y disponibles<br>Ambas separadas y exportables a `data/reporte.txt` | Captura de Reportes con las dos tablas | 1:10 |
| 10 | **Recursividad, generadores y cierres** | Matriz filas × estantes sigue en `core/reportes.py`<br>`sumar_fila()`: caso base + caso recursivo<br>`filas_del_reporte()` usa `yield` y entrega filas bajo demanda<br>`lambda` elige sección o categoría y se pasa como cierre | Pila de llamadas LIFO + icono de `yield` | 1:10 |
| 11 | **Persistencia, regex y errores** | `pathlib` para rutas; JSON para guardar<br>`PATRON_DNI` y `PATRON_ISBN` validan con `fullmatch`<br>`convertir_fecha()` verifica formato y fecha real<br>`ErrorDeDatos` da mensajes claros al usuario | Iconos de archivo, lupa regex y escudo | 0:50 |
| 12 | **Calidad y verificación** | `compileall` sin errores<br>7 archivos `.ui` cargan con `uic.loadUi`<br>20 pruebas unitarias en modo offscreen<br>Firebase queda preparado en un módulo aparte | Checklist verde con cada verificación | 0:40 |
| 13 | **Demo y cierre** | Flujo breve: acceso → catálogo → préstamo → devolución → reportes<br>Mensajes clave: plazo fijo, vencido bloquea, sin multas<br>Preguntas | Captura final de Reportes con las dos tablas + “¿Preguntas?” | 0:50 |

**Total exposición: 12:00. Preguntas: 5:00.**

---

## Mapa de cobertura de la rúbrica y el sílabo

| Tema del sílabo / criterio de rúbrica | Dónde se evidencia |
| --- | --- |
| 1. Fundamentos de Python | Diapositivas 4 y 11: estructuras, funciones y validaciones. |
| 2. Principios de POO | Diapositiva 5: clases, encapsulación, constructores y abstracción. |
| 3. Métodos y funciones / módulos | Diapositivas 4 y 5: paquetes `core` y `ui`, factories y getters. |
| 4. Matrices y recursividad | Diapositiva 10: matrices filas × estantes en `core/reportes.py`, `sumar_fila()` y pila de llamadas. |
| 5. Herencia y polimorfismo | Diapositiva 5: `Usuario` → `Administrador` y `puede_administrar()`. |
| 6. Interfaces gráficas con PyQt5 y Qt Designer | Diapositivas 6 y 7: `.ui`, `loadUi`, señales, slots y QSS. |
| 7. Componentes avanzados | Diapositivas 7 y 8: Combo, Tabla, Lista, Spin, Splitter y plazo como texto. |
| 8. Manejo de archivos | Diapositiva 11: `pathlib`, JSON y generadores en reportes. |
| 9. Procesamiento de texto y errores | Diapositiva 11: regex, validación de fechas y excepciones propias. |
| Generadores y cierres | Diapositiva 10: `yield` y `lambda` con captura de `tipo`. |
| Documentación del código | Diapositiva 12: docstrings, README, plan y guion de exposición. |
| Presentación máximo 15 diapositivas | 13 diapositivas. |

**Nota sobre el Calendar Widget:** el sílabo y la rúbrica final lo mencionan como componente posible, pero el requerimiento del proyecto fija un plazo de 15 días. Por eso el plazo y la fecha límite se muestran como texto calculado, sin calendario ni selector. La decisión está explicada en `docs/Plan_proyecto.md`.
