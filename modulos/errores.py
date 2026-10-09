# Parece que necesitamos colocar los errores como clases para usar "raise".

class DatosInvalidosError(BibliotecaError, ValueError):
