from datetime import date

from . import configuracion, errores, utilidades


class Usuario:
    """Representa a un usuario general del sistema (Estudiante o Docente) con sus datos y validaciones de membresía."""

    def __init__(
        self, dni, nombre, tipo="Estudiante", vencimiento_membresia=None, activo=True
    ):
        self._dni = utilidades.validar_dni(dni)
        self._nombre = str(nombre).strip()
        self._tipo = str(tipo).strip()
        if self._nombre == "":
            raise errores.ErrorDeDatos("El nombre no puede quedar vacio")
        if self._tipo not in configuracion.TIPOS_DE_USUARIO:
            raise errores.ErrorDeDatos(
                f"El tipo de usuario debe ser {' o '.join(configuracion.TIPOS_DE_USUARIO)}"
            )
        if vencimiento_membresia is None:
            raise errores.ErrorDeDatos(
                f"El usuario {self._nombre} no tiene fecha de vencimiento de membresia"
            )
        self._vencimiento_membresia = utilidades.convertir_fecha(vencimiento_membresia)
        self._activo = bool(activo)

    def dni(self):
        """Retorna el DNI validado del usuario."""
        return self._dni

    def nombre(self):
        """Retorna el nombre limpio del usuario."""
        return self._nombre

    def tipo(self):
        """Retorna el tipo de membresía del usuario."""
        return self._tipo

    def vencimiento_membresia(self):
        """Retorna la fecha de vencimiento de la membresía."""
        return self._vencimiento_membresia

    def esta_activo(self):
        """Indica si la cuenta del usuario está activa (True) o de baja (False)."""
        return self._activo

    def puede_administrar(self):
        """Indica si el usuario tiene permisos de administrador (por defecto False)."""
        return False

    def tiene_membresia_vigente(self):
        """Verifica si la fecha actual es menor o igual a la fecha de vencimiento."""
        return date.today() <= self._vencimiento_membresia

    def estado(self):
        """Evalúa y retorna el estado actual de la cuenta (De baja, Vencida o Activa)."""
        if not self.esta_activo():
            return "De baja"
        if not self.tiene_membresia_vigente():
            return "Membresia vencida"
        return "Activo y con membresia vigente"

    def datos_de_membresia(self):
        """Devuelve un diccionario con los datos principales de la membresía para mostrar en pantalla."""
        return {
            "dni": self._dni,
            "nombre": self._nombre,
            "tipo": self._tipo,
            "vencimiento_membresia": str(self._vencimiento_membresia),
            "estado": self.estado(),
        }


class Administrador(Usuario):
    """Subclase que otorga privilegios especiales de administración al usuario."""

    def puede_administrar(self):
        """Habilita los permisos de administración."""
        return True

    def datos_de_membresia(self):
        """Extiende los datos de membresía agregando el indicador de permisos de administrador."""
        datos = super().datos_de_membresia()
        datos["puede_administrar"] = utilidades.si_o_no(self.puede_administrar())
        return datos


def crear_usuario(datos):
    """Fábrica que recibe un diccionario con datos y retorna una instancia de Usuario o Administrador."""
    if not isinstance(datos, dict):
        raise errores.ErrorDeDatos("Cada usuario del JSON debe ser un diccionario")
    dni = datos.get("dni")
    nombre = datos.get("nombre")
    tipo = datos.get("tipo", "Estudiante")
    vencimiento_membresia = datos.get("vencimiento_membresia")
    activo = datos.get("activo", True)
    if str(tipo).strip().lower() == "administrador":
        return Administrador(dni, nombre, tipo, vencimiento_membresia, activo)
    return Usuario(dni, nombre, tipo, vencimiento_membresia, activo)
