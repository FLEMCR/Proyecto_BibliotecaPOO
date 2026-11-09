class ErrorBiblioteca(Exception):
    """Clase base para representar cualquier error personalizado dentro del sistema de la biblioteca."""

    pass


class ErrorDeDatos(ErrorBiblioteca, ValueError):
    """Representa errores de validación, formatos incorrectos o datos faltantes al procesar la información."""

    pass


class ErrorDeArchivo(ErrorBiblioteca):
    """Representa problemas al abrir, leer o escribir los archivos del sistema."""

    pass
