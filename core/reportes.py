"""Reportes de la biblioteca: matrices de libros por sección/categoría y estante.

La lógica de negocio vive acá y no importa PyQt5: la interfaz solo pide los datos
y decide cómo mostrarlos. Las matrices son listas de listas (filas × estantes)
y el total de cada fila se calcula con una función recursiva.
"""

from datetime import date

from . import configuracion, libros

ARCHIVO_REPORTE = "reporte.txt"

TIPOS_DE_REPORTE = ("Sección", "Categoría")

CABECERAS_HISTORIAL = (
    "ID",
    "DNI",
    "Usuario",
    "ISBN",
    "Libro",
    "Fecha préstamo",
    "Fecha límite",
    "Devolución",
    "Estado",
)

CABECERAS_INVENTARIO = (
    "ISBN",
    "Título",
    "Autor",
    "Categoría",
    "Sección",
    "Estante",
    "Ejemplares",
    "Prestados",
    "Disponibles",
)


def sumar_fila(fila, indice=0):
    """Suma una fila de la matriz de forma recursiva (caso base + paso)."""
    if indice >= len(fila):
        return 0
    return fila[indice] + sumar_fila(fila, indice + 1)


def construir_matriz(libros, filas, obtener_fila):
    """Arma una matriz de filas × estantes con la cantidad de ejemplares.

    `obtener_fila` es una función que devuelve la etiqueta de fila de cada libro:
    su sección o su categoría, según el reporte elegido.
    """
    matriz = [[0 for _ in range(configuracion.CANTIDAD_DE_ESTANTES)] for _ in filas]
    for libro in libros:
        etiqueta = obtener_fila(libro)
        if etiqueta not in filas:
            continue
        fila = filas.index(etiqueta)
        columna = libro.estante() - 1
        matriz[fila][columna] += libro.disponibles()
    return matriz


def generar(biblioteca, tipo="Sección"):
    """Genera un reporte con una matriz y el resumen de préstamos activos."""
    if tipo not in TIPOS_DE_REPORTE:
        tipo = "Sección"

    if tipo == "Categoría":
        filas = list(configuracion.CATEGORIAS)
        obtener_fila = lambda libro: libro.categoria()
    else:
        filas = list(configuracion.SECCIONES)
        obtener_fila = lambda libro: libro.seccion()

    matriz = construir_matriz(biblioteca.todos_los_libros(), filas, obtener_fila)
    activos = biblioteca.prestamos_activos()
    vencidos = [prestamo for prestamo in activos if prestamo.esta_vencido()]

    return {
        "titulo": f"Disponibilidad por {tipo.lower()}",
        "tipo": tipo,
        "fecha": str(date.today()),
        "filas": filas,
        "matriz": matriz,
        "totales": [sumar_fila(fila) for fila in matriz],
        "activos": len(activos),
        "vencidos": len(vencidos),
    }


def resumen_visible(biblioteca):
    """Arma el texto corto de resumen que se muestra arriba de los reportes."""
    datos = biblioteca.resumen()
    activos = biblioteca.prestamos_activos()
    vencidos = [prestamo for prestamo in activos if prestamo.esta_vencido()]
    return (
        f"{datos['titulos']} títulos · {datos['ejemplares']} ejemplares · "
        f"{datos['disponibles']} disponibles · {datos['prestados']} prestados · "
        f"{datos['usuarios']} usuarios · {len(activos)} préstamos activos "
        f"({len(vencidos)} vencidos)"
    )


def historial_de_prestamos(biblioteca):
    """Devuelve una fila por préstamo: quién lo pidió, qué libro y en qué estado."""
    nombres = {
        usuario.dni(): usuario.nombre() for usuario in biblioteca.todos_los_usuarios()
    }
    titulos = {
        libro.isbn(): libro.titulo() for libro in biblioteca.todos_los_libros()
    }
    filas = []
    for prestamo in biblioteca.todos_los_prestamos():
        datos = prestamo.datos_para_pantalla()
        if datos["esta_vencido"]:
            estado = "Vencido"
        elif datos["esta_activo"]:
            estado = "Activo"
        else:
            estado = "Devuelto"
        filas.append(
            [
                datos["id"],
                datos["dni"],
                nombres.get(datos["dni"], "Sin registrar"),
                datos["isbn"],
                titulos.get(datos["isbn"], "Sin registrar"),
                datos["fecha_prestamo"],
                datos["fecha_limite"],
                datos["fecha_devolucion"] or "-",
                estado,
            ]
        )
    return filas


def inventario_de_libros(biblioteca):
    """Devuelve una fila por libro con ejemplares, prestados y disponibles."""
    filas = []
    datos_de_libros = libros.datos_del_catalogo(biblioteca.todos_los_libros())
    for datos in datos_de_libros:
        filas.append(
            [
                datos["isbn"],
                datos["titulo"],
                datos["autor"],
                datos["categoria"],
                datos["seccion"],
                str(datos["estante"]),
                str(datos["ejemplares"]),
                str(datos["prestados"]),
                str(datos["disponibles"]),
            ]
        )
    return filas


def filas_del_reporte(reporte):
    """Generador que entrega cada fila de la matriz lista para mostrar."""
    for fila, etiqueta in enumerate(reporte["filas"]):
        yield fila, etiqueta, reporte["matriz"][fila], reporte["totales"][fila]


def _tabla_como_texto(cabeceras, filas):
    """Alinea una tabla en texto plano para el archivo exportado."""
    anchos = [len(str(cabecera)) for cabecera in cabeceras]
    for fila in filas:
        for indice, valor in enumerate(fila):
            anchos[indice] = max(anchos[indice], len(str(valor)))

    def dibujar(valores):
        return "  ".join(
            str(valor).ljust(anchos[indice])
            for indice, valor in enumerate(valores)
        ).rstrip()

    return "\n".join([dibujar(cabeceras)] + [dibujar(fila) for fila in filas])


def a_texto(reporte, biblioteca=None):
    """Convierte el reporte a texto plano para exportarlo a un archivo .txt."""
    lineas = [
        reporte["titulo"],
        f"Fecha: {reporte['fecha']}",
        "",
    ]
    encabezado = "Filas".ljust(24)
    for estante in range(1, configuracion.CANTIDAD_DE_ESTANTES + 1):
        encabezado += f"E{estante}".rjust(8)
    encabezado += "Total".rjust(8)
    lineas.append(encabezado)

    for _fila, etiqueta, valores, total in filas_del_reporte(reporte):
        linea = etiqueta.ljust(24)
        for valor in valores:
            linea += str(valor).rjust(8)
        linea += str(total).rjust(8)
        lineas.append(linea)

    lineas.extend(
        [
            "",
            f"Préstamos activos: {reporte['activos']}",
            f"Préstamos vencidos: {reporte['vencidos']}",
        ]
    )
    if biblioteca is not None:
        lineas.extend(
            [
                "",
                "HISTORIAL DE PRÉSTAMOS",
                _tabla_como_texto(
                    CABECERAS_HISTORIAL, historial_de_prestamos(biblioteca)
                ),
                "",
                "INVENTARIO DE LIBROS",
                _tabla_como_texto(
                    CABECERAS_INVENTARIO, inventario_de_libros(biblioteca)
                ),
            ]
        )
    return "\n".join(lineas) + "\n"


def a_html(reporte):
    """Convierte el reporte a HTML simple para mostrarlo en un QTextEdit."""
    filas_html = []
    for _fila, etiqueta, valores, total in filas_del_reporte(reporte):
        celdas = "".join(f"<td>{valor}</td>" for valor in valores)
        filas_html.append(
            f"<tr><td><b>{etiqueta}</b></td>{celdas}"
            f"<td><b>{total}</b></td></tr>"
        )

    cabeceras = "".join(
        f"<th>E{estante}</th>"
        for estante in range(1, configuracion.CANTIDAD_DE_ESTANTES + 1)
    )
    return (
        f"<h2>{reporte['titulo']}</h2>"
        f"<p><b>Fecha:</b> {reporte['fecha']}</p>"
        "<table border='1' cellpadding='4' cellspacing='0'>"
        f"<tr><th>Filas</th>{cabeceras}<th>Total</th></tr>"
        + "".join(filas_html)
        + "</table>"
        f"<p><b>Préstamos activos:</b> {reporte['activos']} · "
        f"<b>Vencidos:</b> {reporte['vencidos']}</p>"
    )


def exportar(biblioteca, tipo="Sección"):
    """Guarda el reporte en data/reporte.txt y devuelve la ruta y los datos."""
    reporte = generar(biblioteca, tipo)
    ruta = configuracion.ruta_del_archivo(ARCHIVO_REPORTE)
    ruta.write_text(a_texto(reporte, biblioteca), encoding="utf-8")
    return ruta, reporte
