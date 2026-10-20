class BibliotecaError(Exception):
    pass


class DatosInvalidosError(BibliotecaError, ValueError):
    pass
