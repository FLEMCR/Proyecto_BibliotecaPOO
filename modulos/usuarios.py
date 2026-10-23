from datetime import date

from modulos import configuracion, errores, utilidades


class Usuario:
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
                "El tipo de usuario debe ser "
                + " o ".join(configuracion.TIPOS_DE_USUARIO)
            )
        if vencimiento_membresia is None:
            raise errores.ErrorDeDatos(
                "El usuario "
                + self._nombre
                + " no tiene fecha de vencimiento de membresia"
            )
        self._vencimiento_membresia = utilidades.convertir_fecha(vencimiento_membresia)
        self._activo = bool(activo)

    def dni(self):
        return self._dni

    def nombre(self):
        return self._nombre

    def tipo(self):
        return self._tipo

    def vencimiento_membresia(self):
        return self._vencimiento_membresia

    def esta_activo(self):
        return self._activo

    def puede_administrar(self):
        return False

    def tiene_membresia_vigente(self):
        return date.today() <= self._vencimiento_membresia

    def estado(self):
        if not self.esta_activo():
            return "De baja"
        if not self.tiene_membresia_vigente():
            return "Membresia vencida"
        return "Al dia"

    def datos_de_membresia(self):
        return {
            "dni": self._dni,
            "nombre": self._nombre,
            "tipo": self._tipo,
            "vencimiento_membresia": str(self._vencimiento_membresia),
            "estado": self.estado(),
        }


class Administrador(Usuario):
    def puede_administrar(self):
        return True

    def datos_de_membresia(self):
        datos = super().datos_de_membresia()
        datos["puede_administrar"] = utilidades.si_o_no(self.puede_administrar())
        return datos


def crear_usuario(datos):
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
