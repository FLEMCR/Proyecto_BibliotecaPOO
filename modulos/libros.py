from modulos import configuracion, errores, utilidades


class Libro:
    def __init__(
        self, isbn, titulo, autor, categoria, seccion, estante, ejemplares, en_estante
    ):
        self._isbn = utilidades.validar_isbn(isbn)
        self._titulo = str(titulo).strip()
        self._autor = str(autor).strip()
        self._categoria = str(categoria).strip()
        self._seccion = str(seccion).strip().upper()
        self._estante = int(estante)
        self._ejemplares = int(ejemplares)
        self._en_estante = int(en_estante)
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

    def en_estante(self):
        return self._en_estante

    def prestados(self):
        return self._ejemplares - self._en_estante

    def se_puede_prestar(self):
        return self._en_estante > 1

    def revisar_datos(self):
        if self._titulo == "":
            raise errores.ErrorDeDatos("El titulo no puede quedar vacio")
        if self._autor == "":
            raise errores.ErrorDeDatos("El autor no puede quedar vacio")
        if self._categoria == "":
            raise errores.ErrorDeDatos("La categoria no puede quedar vacia")
        if self._seccion not in configuracion.SECCIONES:
            raise errores.ErrorDeDatos(
                "La seccion "
                + self._seccion
                + " no existe. Las secciones son "
                + ", ".join(configuracion.SECCIONES)
            )
        if self._estante < 1 or self._estante > configuracion.CANTIDAD_DE_ESTANTES:
            raise errores.ErrorDeDatos(
                "El estante debe estar entre 1 y "
                + str(configuracion.CANTIDAD_DE_ESTANTES)
            )
        if self._ejemplares < 1:
            raise errores.ErrorDeDatos("Un libro debe tener por lo menos 1 ejemplar")
        if self._en_estante < 0:
            raise errores.ErrorDeDatos(
                "La cantidad en el estante no puede ser negativa"
            )
        if self._en_estante > self._ejemplares:
            raise errores.ErrorDeDatos(
                "No puede haber mas libros en el estante que ejemplares"
            )
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
            "en_estante": self._en_estante,
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
        datos.get("categoria", "General"),
        datos.get("seccion", "A"),
        datos.get("estante", 1),
        datos.get("ejemplares", 1),
        datos.get("en_estante", 1),
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
