membresias = ["admin", "invitado", "estudiante", "docente"]
# No se si usar diccionarios o una clase para las membresias y colocar los datos por defecto de cada uno


class Usuario:
    def __init__(self, nombre="Invitado", membresia="Invitado"):
        self.id = 0  # Hay que colocar un numero progresivo acorde al numero del usuario, su index
        self.nombre = nombre
        self.membresia = membresia


usuarios = [Usuario("Admin", "Admin")]
