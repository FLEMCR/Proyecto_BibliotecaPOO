from modulos import configuracion, errores, utilidades


class Libro:
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

    def disponibles(self):
        return self._disponibles

    def prestados(self):
        return "Aun por hacer".upper()

    def se_puede_prestar(self):
        return self._disponibles > 1

    def revisar_datos(self):
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
        datos = self.a_diccionario()
        datos["seccion_nombre"] = configuracion.SECCIONES[self._seccion]
        datos["prestados"] = self.prestados()
        datos["se_puede_prestar"] = utilidades.si_o_no(self.se_puede_prestar())
        return datos


def crear_libro(datos):
    if not isinstance(datos, dict):
        raise errores.ErrorDeDatos("Cada libro del JSON debe ser un diccionario")
    return Libro(
        datos.get("isbn", ""),
        datos.get("titulo", ""),
        datos.get("autor", ""),
        datos.get("categoria"),
        datos.get("seccion"),
        datos.get("estante"),
        datos.get("ejemplares"),
        datos.get("disponibles"),
    )


def coincide_con_la_busqueda(libro, texto):
    buscado = str(texto).strip().lower()
    if buscado == "":
        return False
    esta_en_el_titulo = buscado in libro.titulo().lower()
    esta_en_el_autor = buscado in libro.autor().lower()
    esta_en_la_categoria = buscado in libro.categoria().lower()
    return esta_en_el_titulo or esta_en_el_autor or esta_en_la_categoria


def buscar_por_texto(libros, texto):
    if len(libros) == 0:
        return []
    primer_libro = libros[0]
    libros_que_faltan = libros[1:]
    if coincide_con_la_busqueda(primer_libro, texto):
        return [primer_libro] + buscar_por_texto(libros_que_faltan, texto)
    return buscar_por_texto(libros_que_faltan, texto)


def datos_del_catalogo(libros):
    if len(libros) == 0:
        return []
    primer_libro = libros[0]
    libros_que_faltan = libros[1:]
    return [primer_libro.datos_para_pantalla()] + datos_del_catalogo(libros_que_faltan)
