from datetime import date

from . import configuracion, errores, utilidades


class Prestamo:
    """Representa un préstamo de un libro a un usuario con sus fechas y estado."""

    def __init__(
        self,
        isbn,
        dni,
        fecha_prestamo,
        fecha_limite,
        fecha_devolucion=None,
        estado="activo",
        identificador=None,
    ):
        self._identificador = str(identificador or "").strip()
        self._isbn = utilidades.validar_isbn(isbn)
        self._dni = utilidades.validar_dni(dni)
        self._fecha_prestamo = utilidades.convertir_fecha(fecha_prestamo)
        self._fecha_limite = utilidades.convertir_fecha(fecha_limite)
        self._estado = str(estado).strip().lower()
        if self._estado not in configuracion.ESTADOS_DE_PRESTAMO:
            raise errores.ErrorDeDatos(
                f"El estado del prestamo debe ser {' o '.join(configuracion.ESTADOS_DE_PRESTAMO)}"
            )
        if fecha_devolucion in (None, ""):
            self._fecha_devolucion = None
        else:
            self._fecha_devolucion = utilidades.convertir_fecha(fecha_devolucion)

    def identificador(self):
        """Retorna el identificador legible del préstamo."""
        return self._identificador

    def isbn(self):
        """Retorna el ISBN del libro prestado."""
        return self._isbn

    def dni(self):
        """Retorna el DNI del usuario que recibió el préstamo."""
        return self._dni

    def fecha_prestamo(self):
        """Retorna la fecha en que se registró el préstamo."""
        return self._fecha_prestamo

    def fecha_limite(self):
        """Retorna la fecha límite para devolver el libro."""
        return self._fecha_limite

    def fecha_devolucion(self):
        """Retorna la fecha de devolución, o None si todavía no se devolvió."""
        return self._fecha_devolucion

    def estado(self):
        """Retorna el estado actual del préstamo."""
        return self._estado

    def esta_activo(self):
        """Indica si el préstamo todavía no fue devuelto."""
        return self._estado == "activo"

    def esta_vencido(self, fecha_hoy=None):
        """Indica si la fecha límite ya pasó, sin aplicar ninguna multa."""
        if not self.esta_activo():
            return False
        fecha_hoy = fecha_hoy or date.today()
        if not hasattr(fecha_hoy, "year"):
            fecha_hoy = utilidades.convertir_fecha(fecha_hoy)
        return fecha_hoy > self._fecha_limite

    def marcar_devuelto(self, fecha=None):
        """Marca el préstamo como devuelto y guarda la fecha de devolución."""
        fecha = fecha or date.today()
        self._fecha_devolucion = utilidades.convertir_fecha(fecha)
        self._estado = "devuelto"
        return self._fecha_devolucion

    def a_diccionario(self):
        """Convierte el préstamo en un diccionario para guardarlo en JSON."""
        return {
            "id": self._identificador,
            "isbn": self._isbn,
            "dni": self._dni,
            "fecha_prestamo": str(self._fecha_prestamo),
            "fecha_limite": str(self._fecha_limite),
            "fecha_devolucion": (
                None if self._fecha_devolucion is None else str(self._fecha_devolucion)
            ),
            "estado": self._estado,
        }

    def datos_para_pantalla(self):
        """Prepara los datos del préstamo para mostrarlos en la interfaz."""
        datos = self.a_diccionario()
        datos["esta_activo"] = self.esta_activo()
        datos["esta_vencido"] = self.esta_vencido()
        return datos


def crear_prestamo(datos):
    """Crea un préstamo a partir de un diccionario leído del JSON."""
    if not isinstance(datos, dict):
        raise errores.ErrorDeDatos("Cada prestamo del JSON debe ser un diccionario")
    return Prestamo(
        datos.get("isbn", ""),
        datos.get("dni", ""),
        datos.get("fecha_prestamo", ""),
        datos.get("fecha_limite", ""),
        datos.get("fecha_devolucion"),
        datos.get("estado", "activo"),
        datos.get("id"),
    )
