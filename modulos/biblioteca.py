from modulos import config, errores, libros, prestamos, usuarios, utilidades


class Biblioteca:
    def __init__(self):
        self._catalogo = {}
        self._miembros = {}
        self._gestor = prestamos.GestorPrestamos(self._catalogo, self._miembros)
        self._cargado = False

    def cargar_datos(self):
        datos = config.cargar_todos()
        for registro in datos.get("libros", []):
            try:
                libro = libros.Libro(
                    isbn=registro.get("isbn"),
                    titulo=registro.get("titulo"),
                    autor=registro.get("autor"),
                    categoria=registro.get("categoria", "General"),
                    seccion=registro.get("seccion", "A"),
                    estante=registro.get("estante", 1),
                    ejemplares=registro.get("ejemplares", 1),
                    disponibles_prestamo=registro.get("disponibles_prestamo"),
                    activo=registro.get("activo", True),
                )
                self._catalogo[libro.isbn()] = libro
            except errores.DatosInvalidosError as error:
                print(str(error))
        for registro in datos.get("miembros", []):
            try:
                miembro = usuarios.crear_usuario(registro)
                if self._miembros.get(miembro.dni()) is not None:
                    continue
                self._miembros[miembro.dni()] = miembro
            except errores.DatosInvalidosError as error:
                print(str(error))
        self._gestor = prestamos.GestorPrestamos(self._catalogo, self._miembros)
        self._cargado = True
        return {"libros": len(self._catalogo), "miembros": len(self._miembros)}

    def catalogo(self):
        return self._catalogo

    def miembros(self):
        return self._miembros

    def gestor(self):
        return self._gestor

    def libro(self, isbn):
        return self._catalogo.get(isbn)

    def miembro(self, dni):
        return self._miembros.get(dni)

    def prestar(self, isbn, dni):
        return self._gestor.prestar(isbn, dni)

    def devolver(self, codigo):
        return self._gestor.devolver(codigo)

    def prestamos_de(self, dni):
        return self._gestor.historial_de(dni)

    def prestamos_activos(self, dni=None):
        if dni:
            return self._gestor.activos_de(dni)
        return [p for p in self._gestor.prestamos() if not p.devuelto()]

    def resumen(self):
        disponibles = sum(l.disponibles_prestamo() for l in self._catalogo.values())
        prestados = sum(
            l.ejemplares() - l.disponibles_prestamo() for l in self._catalogo.values()
        )
        return {
            "titulos": len(self._catalogo),
            "ejemplares": sum(l.ejemplares() for l in self._catalogo.values()),
            "disponibles": disponibles,
            "prestados": prestados,
            "miembros": len(self._miembros),
            "prestamos": len(self._gestor.prestamos()),
        }

    def __str__(self):
        r = self.resumen()
        return f"{config.nombre_biblioteca}: {r['titulos']} titulos, {r['miembros']} miembros, {r['prestamos']} prestamos"
