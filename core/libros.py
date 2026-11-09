import unicodedata

from core import configuracion, errores, utilidades


class Libro:
    """Representa un libro en el sistema con sus datos, reglas de validación y estado de disponibilidad."""

    def __init__(
        self, isbn, titulo, autor, categoria, seccion, estante, ejemplares, disponibles
    ):
        self._isbn = utilidades.validar_isbn(isbn)
        self._titulo = str(titulo).strip()
        self._autor = str(autor).strip()
        self._categoria = str(categoria).strip()
        self._seccion = str(seccion).strip().upper()
        self._estante = int(estante)
        self._ejemplares = int(ejemplares)
        self._disponibles = int(disponibles)
        self.revisar_datos()

    def isbn(self):
        """Retorna el ISBN del libro."""
        return self._isbn

    def titulo(self):
        """Retorna el título del libro."""
        return self._titulo

    def autor(self):
        """Retorna el autor del libro."""
        return self._autor

    def categoria(self):
        """Retorna la categoría del libro."""
        return self._categoria

    def seccion(self):
        """Retorna la sección del libro."""
        return self._seccion

    def estante(self):
        """Retorna el número de estante del libro."""
        return self._estante

    def ejemplares(self):
        """Retorna el total de ejemplares disponibles y prestados."""
        return self._ejemplares

    def disponibles(self):
        """Retorna la cantidad de ejemplares disponibles en estante."""
        return self._disponibles

    def prestados(self):
        """Calcula y retorna la cantidad de ejemplares prestados actualmente."""
        return self._ejemplares - self._disponibles

    def se_puede_prestar(self):
        """Indica si el libro cuenta con suficientes ejemplares para poder ser prestado."""
        return self._disponibles > 1

    def revisar_datos(self):
        """Valida que todos los atributos del libro cumplan con las reglas de negocio del sistema."""
        if self._titulo == "":
            raise errores.ErrorDeDatos("El titulo no puede quedar vacio")
        elif self._autor == "":
            raise errores.ErrorDeDatos("El autor no puede quedar vacio")
        elif self._categoria == "":
            raise errores.ErrorDeDatos("La categoria no puede quedar vacia")
        elif self._seccion not in configuracion.SECCIONES:
            raise errores.ErrorDeDatos(f"La seccion {self._seccion} no existe.")
        elif self._estante < 1 or self._estante > configuracion.CANTIDAD_DE_ESTANTES:
            raise errores.ErrorDeDatos(
                f"El estante debe estar entre 1 y {configuracion.CANTIDAD_DE_ESTANTES}"
            )
        elif self._ejemplares < 1:
            raise errores.ErrorDeDatos("Un libro debe tener por lo menos 1 ejemplar")
        elif self._disponibles < 0:
            raise errores.ErrorDeDatos(
                "La cantidad para realizar prestamos no puede ser menor a 0"
            )
        elif self._disponibles > self._ejemplares:
            raise errores.ErrorDeDatos("No se puede prestar más de lo que se tiene")
        return True

    def a_diccionario(self):
        """Convierte los atributos del libro en un diccionario para su almacenamiento en JSON."""
        return {
            "isbn": self._isbn,
            "titulo": self._titulo,
            "autor": self._autor,
            "categoria": self._categoria,
            "seccion": self._seccion,
            "estante": self._estante,
            "ejemplares": self._ejemplares,
            "disponibles": self._disponibles,
        }

    def datos_para_pantalla(self):
        """Prepara un diccionario extendido con información legible para mostrar en la interfaz."""
        datos = self.a_diccionario()
        datos["seccion_nombre"] = configuracion.SECCIONES[self._seccion]
        datos["prestados"] = self.prestados()
        datos["se_puede_prestar"] = utilidades.si_o_no(self.se_puede_prestar())
        return datos


def _campo_obligatorio(datos, clave):
    """Devuelve un campo del JSON o lanza un error claro si falta o viene vacio."""
    if clave not in datos or datos[clave] is None or str(datos[clave]).strip() == "":
        raise errores.ErrorDeDatos(f"Falta el campo '{clave}' en un libro del catalogo")
    return datos[clave]


def crear_libro(datos):
    """Fábrica que procesa un diccionario de datos para instanciar un objeto Libro."""
    if not isinstance(datos, dict):
        raise errores.ErrorDeDatos("Cada libro del JSON debe ser un diccionario")
    return Libro(
        _campo_obligatorio(datos, "isbn"),
        _campo_obligatorio(datos, "titulo"),
        _campo_obligatorio(datos, "autor"),
        _campo_obligatorio(datos, "categoria"),
        _campo_obligatorio(datos, "seccion"),
        _campo_obligatorio(datos, "estante"),
        _campo_obligatorio(datos, "ejemplares"),
        _campo_obligatorio(datos, "disponibles"),
    )


def normalizar_texto(texto):
    """Pasa un texto a minusculas y le quita tildes para comparar busquedas."""
    sin_tildes = unicodedata.normalize("NFKD", str(texto))
    solo_ascii = sin_tildes.encode("ascii", "ignore").decode("ascii")
    return solo_ascii.strip().lower()


def _texto_del_campo(libro, campo):
    """Devuelve el texto del libro que corresponde al campo elegido en el buscador."""
    campo_normalizado = normalizar_texto(campo)
    if campo_normalizado == "isbn":
        return libro.isbn()
    if campo_normalizado in ("titulo", "título"):
        return libro.titulo()
    if campo_normalizado == "autor":
        return libro.autor()
    if campo_normalizado == "categoria":
        return libro.categoria()
    if campo_normalizado == "seccion":
        return libro.seccion() + " " + configuracion.SECCIONES.get(libro.seccion(), "")
    return " ".join(
        [libro.isbn(), libro.titulo(), libro.autor(), libro.categoria(), libro.seccion()]
    )


def coincide_con_la_busqueda(libro, texto, campo="Todo"):
    """Verifica si el texto aparece en el campo elegido del libro."""
    buscado = normalizar_texto(texto)
    if buscado == "":
        return True
    return buscado in normalizar_texto(_texto_del_campo(libro, campo))


def buscar_por_texto(libros, texto, campo="Todo"):
    """Busca de forma recursiva los libros que coinciden con el texto y el campo.

    Caso base: la lista llega vacia.
    Paso recursivo: se evalua el primer libro y se continua con el resto.
    """
    if len(libros) == 0:
        return []
    primer_libro = libros[0]
    libros_que_faltan = libros[1:]
    if coincide_con_la_busqueda(primer_libro, texto, campo):
        return [primer_libro] + buscar_por_texto(libros_que_faltan, texto, campo)
    return buscar_por_texto(libros_que_faltan, texto, campo)


def filtrar_por_categoria(libros, categoria):
    """Filtra de forma recursiva los libros que pertenecen a una categoria."""
    if len(libros) == 0:
        return []
    primer_libro = libros[0]
    libros_que_faltan = libros[1:]
    if normalizar_texto(categoria) in ("", "todas", "todos"):
        return libros
    if normalizar_texto(primer_libro.categoria()) == normalizar_texto(categoria):
        return [primer_libro] + filtrar_por_categoria(libros_que_faltan, categoria)
    return filtrar_por_categoria(libros_que_faltan, categoria)


def filtrar_solo_disponibles(libros):
    """Filtra de forma recursiva los libros que se pueden prestar."""
    if len(libros) == 0:
        return []
    primer_libro = libros[0]
    libros_que_faltan = libros[1:]
    if primer_libro.se_puede_prestar():
        return [primer_libro] + filtrar_solo_disponibles(libros_que_faltan)
    return filtrar_solo_disponibles(libros_que_faltan)


def datos_del_catalogo(libros):
    """Convierte de forma recursiva una lista de libros en una lista de diccionarios listos para pantalla."""
    if len(libros) == 0:
        return []
    primer_libro = libros[0]
    libros_que_faltan = libros[1:]
    return [primer_libro.datos_para_pantalla()] + datos_del_catalogo(libros_que_faltan)
