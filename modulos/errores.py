# Parece que necesitamos colocar los errores como clases para usar "raise".
class BibliotecaError(Exception):
    pass

class DatosInvalidosError(BibliotecaError, ValueError):
    pass

def errores():
    pass