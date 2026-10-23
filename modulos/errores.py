class ErrorBiblioteca(Exception):
    pass


class ErrorDeDatos(ErrorBiblioteca, ValueError):
    pass


class ErrorDeArchivo(ErrorBiblioteca):
    pass
