class BibliotecaError(Exception):
    pass


class DatosInvalidosError(BibliotecaError, ValueError):
    pass


class ArchivoDatosError(BibliotecaError):
    pass
