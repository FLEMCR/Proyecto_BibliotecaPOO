from datetime import date

from modulos import configuracion, errores, libros, usuarios, utilidades


class Biblioteca:
    def __init__(self):
        self._catalogo = {}
        self._usuarios = {}
        self.cargar_datos()

    def cargar_datos(self):
        self._catalogo = {}
        for registro in configuracion.leer_archivo(configuracion.ARCHIVO_LIBROS):
            libro = libros.crear_libro(registro)
            self._catalogo[libro.isbn()] = libro

        self._usuarios = {}
        for registro in configuracion.leer_archivo(configuracion.ARCHIVO_USUARIOS):
            usuario = usuarios.crear_usuario(registro)
            self._usuarios[usuario.dni()] = usuario

        return self.resumen()

    def todos_los_libros(self):
        return list(self._catalogo.values())

    def todos_los_usuarios(self):
        return list(self._usuarios.values())

    def libro(self, isbn):
        isbn_buscado = utilidades.validar_isbn(isbn)
        if isbn_buscado not in self._catalogo:
            raise errores.ErrorDeDatos(
                "No hay ningun libro con el ISBN " + isbn_buscado
            )
        return self._catalogo[isbn_buscado]

    def usuario(self, dni):
        dni_buscado = utilidades.validar_dni(dni)
        if dni_buscado not in self._usuarios:
            raise errores.ErrorDeDatos(
                "No hay ningun usuario con el DNI " + dni_buscado
            )
        return self._usuarios[dni_buscado]

    def datos_del_catalogo(self):
        return libros.datos_del_catalogo(self.todos_los_libros())

    def datos_de_un_libro(self, isbn):
        return self.libro(isbn).datos_para_pantalla()

    def buscar(self, texto_buscado):
        encontrados = libros.buscar_por_texto(self.todos_los_libros(), texto_buscado)
        return libros.datos_del_catalogo(encontrados)

    def datos_de_los_usuarios(self):
        return [usuario.datos_de_membresia() for usuario in self.todos_los_usuarios()]

    def datos_de_membresia(self, dni):
        return self.usuario(dni).datos_de_membresia()

    def resumen(self):
        total_ejemplares = 0
        total_en_estante = 0
        for libro in self.todos_los_libros():
            total_ejemplares = total_ejemplares + libro.ejemplares()
            total_en_estante = total_en_estante + libro.en_estante()
        return {
            "biblioteca": configuracion.NOMBRE_BIBLIOTECA,
            "fecha_de_hoy": str(date.today()),
            "titulos": len(self._catalogo),
            "ejemplares": total_ejemplares,
            "en_estante": total_en_estante,
            "prestados": total_ejemplares - total_en_estante,
            "usuarios": len(self._usuarios),
        }
