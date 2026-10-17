import membresias
import utilidades


class Usuario:
    contadores = {tipo: 0 for tipo in membresias.CLASES}

    def __init__(self, nombre, dni, tipo="estudiante", correo=""):
        dni_valido = utilidades.validar_dni(dni)
        membresia = membresias.crear_membresia(tipo)

        Usuario.contadores[tipo] += 1
        numero_contador = Usuario.contadores[tipo]

        self._id_usuario = f"{membresia.prefijo}{numero_contador:04d}"
        self._nombre = nombre
        self._dni = dni_valido
        self._correo = correo.strip()
        self._membresia = membresia
        self._habilitado = True

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def nombre(self):
        return self._nombre

    @property
    def dni(self):
        return self._dni

    @property
    def correo(self):
        return self._correo

    @property
    def membresia(self):
        return self._membresia

    @property
    def tipo(self):
        return self._membresia.tipo

    @property
    def habilitado(self):
        return self._habilitado

    @property
    def activo(self):
        return self._habilitado and self._membresia.vigente()

    def es_admin(self):
        return self._membresia.puede_administrar()

    def membresia_vigente(self):
        return self._membresia.vigente()

    def dias_para_vencer(self):
        return self._membresia.dias_para_vencer()

    def multa(self):
        return self._membresia.multa()

    def puede_renovar(self):
        return self._habilitado

    def puede_pedir_libros(self):
        return self.activo

    def puede_devolver_libros(self):
        return True

    def habilitar(self):
        self._habilitado = True

    def deshabilitar(self):
        self._habilitado = False

    def __str__(self):
        estado = "activo" if self.activo else "inactivo"
        return f"El usuario con id: {self._id_usuario}, con nombre: {self._nombre}, tiene el estado: {estado}"


class Admin(Usuario):
    def __init__(self, nombre, dni, correo=""):
        super().__init__(nombre, dni, tipo="admin", correo=correo)
