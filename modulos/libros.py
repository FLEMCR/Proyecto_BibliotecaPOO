from modulos import errores, utilidades


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
        activo=True,
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
        self._activo = bool(activo)

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

    def activo(self):
        return self._activo

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
            "activo": self._activo,
        }

    def __str__(self):
        return (
            f"{self._isbn} | {self._titulo} | {self._autor} | disp: {self._disponibles}"
        )
