from modulos import config
from modulos import errores
from modulos import utilidades


class Membresia:
    TIPO = "base"
    LIMITE_LIBROS = 0
    DIAS_PRESTAMO = 0
    MULTA_POR_DIA = 0.0
    PUEDE_ADMINISTRAR = False

    def __init__(self):
        pass

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


class Estudiante(Membresia):
    TIPO = "estudiante"
    LIMITE_LIBROS = config.limite_libros["estudiante"]
    DIAS_PRESTAMO = config.dias_prestamo["estudiante"]
    MULTA_POR_DIA = config.multa_por_dia["estudiante"]


class Docente(Membresia):
    TIPO = "docente"
    LIMITE_LIBROS = config.limite_libros["docente"]
    DIAS_PRESTAMO = config.dias_prestamo["docente"]
    MULTA_POR_DIA = config.multa_por_dia["docente"]


class Administrador(Docente):
    TIPO = "administrador"
    PUEDE_ADMINISTRAR = True
    MULTA_POR_DIA = config.multa_por_dia["administrador"]


class Invitado(Membresia):
    TIPO = "invitado"
    LIMITE_LIBROS = config.limite_libros["invitado"]
    DIAS_PRESTAMO = config.dias_prestamo["invitado"]
    MULTA_POR_DIA = config.multa_por_dia["invitado"]


def crear_membresia(tipo):
    clave = str(tipo or "estudiante").strip().lower()
    if clave == "estudiante":
        return Estudiante()
    if clave == "docente":
        return Docente()
    if clave == "administrador":
        return Administrador()
    if clave == "invitado":
        return Invitado()
    raise errores.DatosInvalidosError("Ese tipo de membresia no existe")


class Usuario:
    def __init__(self, nombre, dni, tipo="estudiante"):
        self._nombre = str(nombre or "").strip()
        self._dni = dni
        if tipo != "invitado" and dni:
            self._dni = utilidades.validar_dni(dni)
        self._membresia = crear_membresia(tipo)

    def nombre(self):
        return self._nombre

    def dni(self):
        return self._dni

    def tipo(self):
        return self._membresia.tipo()

    def membresia(self):
        return self._membresia

    def puede_administrar(self):
        return self._membresia.puede_administrar()

    def __str__(self):
        return f"{self._nombre} ({self._dni}) - {self.tipo()}"


def crear_usuario(datos):
    if not isinstance(datos, dict):
        raise errores.DatosInvalidosError("Cada miembro debe ser un diccionario")
    tipo = str(datos.get("tipo", "Estudiante")).strip().lower()
    return Usuario(datos.get("nombre"), datos.get("dni"), tipo)
