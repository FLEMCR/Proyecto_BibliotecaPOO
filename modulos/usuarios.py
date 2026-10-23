from datetime import date

from modulos import config, errores, utilidades


class Membresia:
    TIPO = "base"
    LIMITE_LIBROS = 0
    DIAS_PRESTAMO = 0
    MULTA_POR_DIA = 0.0
    PUEDE_ADMINISTRAR = False

    def __init__(self, vencimiento=None):
        if vencimiento is None:
            self._vence = date.today()
        else:
            self._vence = utilidades.convertir_fecha(vencimiento)
        self._cancelada = False

    def tipo(self):
        return self.TIPO

    def limite_libros(self):
        return self.LIMITE_LIBROS

    def dias_prestamo(self):
        return self.DIAS_PRESTAMO

    def multa_por_dia(self):
        return self.MULTA_POR_DIA

    def puede_administrar(self):
        return self.PUEDE_ADMINISTRAR

    def vencimiento(self):
        return self._vence

    def vigente(self):
        if self._cancelada:
            return False
        return date.today() <= self._vence

    def renovar(self):
        if self.vigente():
            self._vence = utilidades.sumar_dias(self._vence, 365)
        else:
            self._vence = utilidades.sumar_dias(date.today(), 365)
        self._cancelada = False
        return self._vence

    def cancelar(self):
        self._cancelada = True
        return True

    def estado(self):
        if self._cancelada:
            return "Cancelada"
        if self.vigente():
            return "Vigente"
        return "Vencida"

    def describir(self):
        return f"{self.TIPO.capitalize()}: {self.LIMITE_LIBROS} libros por {self.DIAS_PRESTAMO} dias"

    def __str__(self):
        return self.describir()


class Estudiante(Membresia):
    TIPO = "estudiante"
    LIMITE_LIBROS = config.limite_libros["estudiante"]
    DIAS_PRESTAMO = config.dias_prestamo["estudiante"]
    MULTA_POR_DIA = config.multa_por_dia


class Docente(Membresia):
    TIPO = "docente"
    LIMITE_LIBROS = config.limite_libros["docente"]
    DIAS_PRESTAMO = config.dias_prestamo["docente"]
    MULTA_POR_DIA = config.multa_por_dia


class Administrador(Docente):
    TIPO = "administrador"
    PUEDE_ADMINISTRAR = True
    MULTA_POR_DIA = config.multa_por_dia


class Invitado(Membresia):
    TIPO = "invitado"
    LIMITE_LIBROS = config.limite_libros["invitado"]
    DIAS_PRESTAMO = config.dias_prestamo["invitado"]
    MULTA_POR_DIA = config.multa_por_dia

    def describir(self):
        return "Invitado: solo puede consultar el catalogo"


def crear_membresia(tipo, vencimiento=None):
    clave = str(tipo or "estudiante").strip().lower()
    if clave == "estudiante":
        return Estudiante(vencimiento)
    if clave == "docente":
        return Docente(vencimiento)
    if clave in ("administrador", "admin"):
        return Administrador(vencimiento)
    if clave == "invitado":
        return Invitado(vencimiento)
    raise errores.DatosInvalidosError("Ese tipo de membresia no existe")


class Usuario:
    def __init__(self, nombre, dni, tipo="estudiante", vencimiento=None, activo=True):
        self._nombre = str(nombre or "").strip()
        self._dni = dni
        if tipo != "invitado" and dni:
            self._dni = utilidades.validar_dni(dni)
        self._membresia = crear_membresia(tipo, vencimiento)
        self._activo = bool(activo)

    def nombre(self):
        return self._nombre

    def dni(self):
        return self._dni

    def tipo(self):
        return self._membresia.tipo()

    def membresia(self):
        return self._membresia

    def activo(self):
        return self._activo

    def puede_administrar(self):
        return self._membresia.puede_administrar()

    def vencimiento(self):
        return self._membresia.vencimiento()

    def estado(self):
        if not self._activo:
            return "De baja"
        return self._membresia.estado()

    def dar_de_baja(self):
        self._activo = False
        return True

    def reactivar(self):
        self._activo = True
        return True

    def renovar_membresia(self):
        return self._membresia.renovar()

    def cancelar_membresia(self):
        return self._membresia.cancelar()

    def a_diccionario(self):
        return {
            "dni": self._dni,
            "nombre": self._nombre,
            "tipo": self._membresia.TIPO.capitalize(),
            "vencimiento_membresia": str(self._membresia.vencimiento()),
            "activo": self._activo,
        }

    def __str__(self):
        return f"{self._nombre} ({self._dni}) - {self.tipo()}"


def crear_usuario(datos):
    if not isinstance(datos, dict):
        raise errores.DatosInvalidosError("Cada miembro debe ser un diccionario")
    tipo = str(datos.get("tipo", "Estudiante")).strip().lower()
    return Usuario(
        datos.get("nombre"),
        datos.get("dni"),
        tipo,
        datos.get("vencimiento_membresia"),
        datos.get("activo", True),
    )
