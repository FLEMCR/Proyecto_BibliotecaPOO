class ErrorBiblioteca(Exception):
    pass


class ErrorDeDatos(ErrorBiblioteca, ValueError):
    pass
