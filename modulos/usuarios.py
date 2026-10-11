import utilidades

membresias = ["admin", "invitado", "estudiante", "docente"]
# No se si usar diccionarios o una clase para las membresias y colocar los datos por defecto de cada uno


class Usuario:
    CONTADOR = 100

    def __init__(self, nombre, dni, tipo="estudiante", correo=""):
        Usuario.CONTADOR += 1
        self._id = Usuario.CONTADOR
        self._nombre = nombre
        self._dni = utilidades.validar_dni(dni)
        self._correo = correo.strip()
        self._membresia = membresias
        self._activo = True
        self._multa = 0.0

    def obtener_nombre(self):
        return self._nombre

    def obtener_dni(self):
        return self._dni

    def obtener_membresia(self):
        return self._membresia

    def obtener_multa(self):
        return round(self._multa, 2)


usuarios = [Usuario("Admin", "Admin")]
