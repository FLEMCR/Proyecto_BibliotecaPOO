from modulos import config, errores, utilidades


class Libro:
    def __init__(
        self,
        isbn,
        titulo,
        autor,
        categoria="General",
        seccion="A",
        estante=1,
        ejemplares=1,
        disponibles_prestamo=None,
    ):
        self._isbn = utilidades.validar_isbn(isbn)
        self._titulo = str(titulo or "").strip() or "Sin titulo"
        self._autor = str(autor or "").strip() or "Desconocido"
        self._categoria = str(categoria or "General").strip()
        self._seccion = str(seccion or "A").strip().upper()
        self._estante = int(estante) if estante else 1
        self._ejemplares = int(ejemplares) if ejemplares else 1
        self._disponibles = (
            int(disponibles_prestamo)
            if disponibles_prestamo is not None
            else self._ejemplares
        )

    def isbn(self):
        return self._isbn

    def titulo(self):
        return self._titulo

    def autor(self):
        return self._autor

    def categoria(self):
        return self._categoria

    def seccion(self):
        return self._seccion

    def estante(self):
        return self._estante

    def ejemplares(self):
        return self._ejemplares

    def disponibles_prestamo(self):
        return self._disponibles

    def prestados(self):
        return self._ejemplares - self._disponibles

    def prestar_uno(self):
        if self._disponibles <= 0:
            raise errores.DatosInvalidosError(
                f"No hay ejemplares disponibles de '{self._titulo}'"
            )
        self._disponibles -= 1
        return True

    def devolver_uno(self):
        if self._disponibles < self._ejemplares:
            self._disponibles += 1
        return True

    def a_diccionario(self):
        return {
            "isbn": self._isbn,
            "titulo": self._titulo,
            "autor": self._autor,
            "categoria": self._categoria,
            "seccion": self._seccion,
            "estante": self._estante,
            "ejemplares": self._ejemplares,
            "disponibles_prestamo": self._disponibles,
        }

    def __str__(self):
        return (
            f"{self._isbn} | {self._titulo} | {self._autor} | disp: {self._disponibles}"
        )


def matriz_disponibilidad(catalogo):
    encabezado = ["Seccion"]
    for numero in range(1, config.estantes + 1):
        encabezado.append(f"E{numero}")
    encabezado.append("Total")

    filas = []
    for seccion in config.secciones:
        fila = [seccion]
        total_seccion = 0
        for numero in range(1, config.estantes + 1):
            libres = 0
            for libro in catalogo.values():
                if libro.seccion() == seccion and libro.estante() == numero:
                    libres += libro.disponibles_prestamo()
            fila.append(libres)
            total_seccion += libres
        fila.append(total_seccion)
        filas.append(fila)

    totales = ["Total"]
    general = 0
    for numero in range(1, config.estantes + 1):
        suma = 0
        for fila in filas:
            suma += fila[numero]
        totales.append(suma)
        general += suma
    totales.append(general)
    filas.append(totales)
    return [encabezado] + filas


def matriz_ubicacion(catalogo):
    encabezado = ["Seccion"]
    for numero in range(1, config.estantes + 1):
        encabezado.append(f"E{numero}")
    encabezado.append("Titulos")

    filas = []
    for seccion in config.secciones:
        fila = [seccion]
        titulos = 0
        for numero in range(1, config.estantes + 1):
            cuenta = 0
            for libro in catalogo.values():
                if libro.seccion() == seccion and libro.estante() == numero:
                    cuenta += 1
            fila.append(cuenta)
            titulos += cuenta
        fila.append(titulos)
        filas.append(fila)
    return [encabezado] + filas


def matriz_categorias(catalogo):
    encabezado = ["Categoria", "Titulos", "Ejemplares", "Disponibles"]
    filas = []
    for categoria in categorias_unicas(catalogo):
        titulos = ejemplares = disponibles = 0
        for libro in catalogo.values():
            if libro.categoria().split("/")[0] == categoria:
                titulos += 1
                ejemplares += libro.ejemplares()
                disponibles += libro.disponibles_prestamo()
        filas.append([categoria, titulos, ejemplares, disponibles])
    return [encabezado] + filas


def categorias_unicas(catalogo):
    unicas = []
    for libro in catalogo.values():
        primera = libro.categoria().split("/")[0]
        if primera not in unicas:
            unicas.append(primera)
    return unicas


def niveles_categoria(categoria):
    partes = categoria.split("/")
    if len(partes) == 1:
        return [partes[0]]
    return [partes[0]] + niveles_categoria("/".join(partes[1:]))


def buscar_por_categoria(catalogo, nombre):
    if len(catalogo) == 0:
        return []
    if pertenece_a_categoria(catalogo[0], nombre):
        return [catalogo[0]] + buscar_por_categoria(catalogo[1:], nombre)
    return buscar_por_categoria(catalogo[1:], nombre)


def pertenece_a_categoria(libro, nombre, niveles=None):
    if niveles is None:
        niveles = niveles_categoria(libro.categoria())
    if len(niveles) == 0:
        return False
    if niveles[0].lower() == str(nombre).strip().lower():
        return True
    return pertenece_a_categoria(libro, nombre, niveles[1:])
