from modulos import config, errores, libros, usuarios


class Biblioteca:
    def __init__(self):
        self._catalogo = {}
        self._miembros = {}
        self._sesion = None
        self.cargar_datos()

    def cargar_datos(self):
        try:
            datos = config.cargar_todos()
        except ValueError as error:
            raise errores.ArchivoDatosError(
                f"No se pudieron leer los JSON de la carpeta datos/: {error}"
            )

        self._catalogo = {}
        for registro in datos["libros"]:
            libro = libros.Libro(
                registro.get("isbn"),
                registro.get("titulo"),
                registro.get("autor"),
                registro.get("categoria", "General"),
                registro.get("seccion", "A"),
                registro.get("estante", 1),
                registro.get("ejemplares", 1),
                registro.get("disponibles_prestamo"),
            )
            self._catalogo[libro.isbn()] = libro

        self._miembros = {}
        for registro in datos["miembros"]:
            miembro = usuarios.crear_usuario(registro)
            self._miembros[miembro.dni()] = miembro

        return self.resumen()

    def guardar_datos(self):
        config.guardar_json(
            "libros", [l.a_diccionario() for l in self._catalogo.values()]
        )
        config.guardar_json(
            "miembros", [m.a_diccionario() for m in self._miembros.values()]
        )
        return True

    def catalogo(self):
        return self._catalogo

    def miembros(self):
        return self._miembros

    def libro(self, isbn):
        return self._catalogo.get(isbn)

    def miembro(self, dni):
        return self._miembros.get(dni)

    def iniciar_sesion(self, dni=None, invitado=False):
        if invitado:
            self._sesion = usuarios.Usuario("Invitado", "", "invitado")
        else:
            self._sesion = self.miembro(dni)
        return self._sesion

    def sesion(self):
        return self._sesion

    def cerrar_sesion(self):
        self._sesion = None

    def matrices(self):
        return {
            "disponibilidad": libros.matriz_disponibilidad(self._catalogo),
            "ubicacion": libros.matriz_ubicacion(self._catalogo),
            "categorias": libros.matriz_categorias(self._catalogo),
        }

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
        }

    def __str__(self):
        r = self.resumen()
        return f"{config.nombre_biblioteca}: {r['titulos']} titulos y {r['miembros']} miembros"
