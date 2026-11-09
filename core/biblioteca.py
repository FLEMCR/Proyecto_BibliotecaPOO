from datetime import date

from core import configuracion, errores, libros, usuarios, utilidades


class Biblioteca:
    """Controlador principal del sistema que administra el catálogo de libros, los usuarios y la lógica de negocio."""

    def __init__(self):
        self._catalogo = {}
        self._usuarios = {}
        self.cargar_datos()

    def cargar_datos(self):
        """Carga y sincroniza los libros y usuarios desde los archivos JSON de almacenamiento."""
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
        """Retorna una lista con todos los objetos Libro registrados en la biblioteca."""
        return list(self._catalogo.values())

    def todos_los_usuarios(self):
        """Retorna una lista con todos los objetos Usuario registrados."""
        return list(self._usuarios.values())

    def libro(self, isbn):
        """Busca y retorna un libro específico por su ISBN; lanza error si no existe."""
        isbn_buscado = utilidades.validar_isbn(isbn)
        if isbn_buscado not in self._catalogo:
            raise errores.ErrorDeDatos(
                f"No hay ningun libro con el ISBN {isbn_buscado}"
            )
        return self._catalogo[isbn_buscado]

    def usuario(self, dni):
        """Busca y retorna un usuario específico por su DNI; lanza error si no existe."""
        dni_buscado = utilidades.validar_dni(dni)
        if dni_buscado not in self._usuarios:
            raise errores.ErrorDeDatos(
                f"No hay ningun usuario con el DNI {dni_buscado}"
            )
        return self._usuarios[dni_buscado]

    def datos_del_catalogo(self):
        """Retorna el catálogo completo formateado para mostrar en pantalla."""
        return libros.datos_del_catalogo(self.todos_los_libros())

    def datos_de_un_libro(self, isbn):
        """Retorna los datos detallados de un libro específico para su visualización."""
        return self.libro(isbn).datos_para_pantalla()

    def buscar(self, texto_buscado):
        """Filtra y retorna libros que coincidan con el texto de búsqueda ingresado."""
        encontrados = libros.buscar_por_texto(self.todos_los_libros(), texto_buscado)
        return libros.datos_del_catalogo(encontrados)

    def datos_de_los_usuarios(self):
        """Retorna una lista con los datos de membresía de todos los usuarios."""
        return [usuario.datos_de_membresia() for usuario in self.todos_los_usuarios()]

    def datos_de_membresia(self, dni):
        """Retorna los datos de membresía de un usuario específico."""
        return self.usuario(dni).datos_de_membresia()

    def resumen(self):
        """Calcula y retorna un diccionario con estadísticas generales del estado de la biblioteca."""
        total_ejemplares = 0
        total_disponibles = 0
        for libro in self.todos_los_libros():
            total_ejemplares = total_ejemplares + libro.ejemplares()
            total_disponibles = total_disponibles + libro.disponibles()
        return {
            "biblioteca": configuracion.NOMBRE_BIBLIOTECA,
            "fecha_de_hoy": str(date.today()),
            "titulos": len(self._catalogo),
            "ejemplares": total_ejemplares,
            "disponibles": total_disponibles,
            "prestados": total_ejemplares - total_disponibles,
            "usuarios": len(self._usuarios),
        }
