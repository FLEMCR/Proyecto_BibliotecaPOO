class Usuario:
    def __init__(self, nombre="Invitado", membresia="Invitado"):
        self.id = 0  # Hay que colocar un numero progresivo acorde al numero del usuario, su index
        self.nombre = nombre
        self.membresia = membresia


usuarios = [Usuario("Admin", "Admin")]
