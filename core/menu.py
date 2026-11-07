import time

from proyecto_parcial.core import configuracion, errores, utilidades


def portada(biblioteca):
    """Muestra la pantalla de bienvenida y el resumen inicial de la biblioteca."""
    resumen = biblioteca.resumen()
    print()
    print(resumen["biblioteca"])
    print(configuracion.LEMA)
    print("Hoy es " + resumen["fecha_de_hoy"])
    print()
    print("/" * 20)
    print(
        f"Hay {resumen['titulos']} titulos y {resumen['usuarios']} usuarios registrados"
    )
    print("/" * 20)


def menu_de_acceso(biblioteca):
    """Muestra el menú principal de acceso al sistema mediante DNI."""
    while True:
        print()
        print("MENU DE ACCESO")
        print("1) Acceder con DNI")
        print("0) Salir")
        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            entrar(biblioteca)
        elif opcion == "0":
            print("Cerrando el programa...")
            time.sleep(0.5)
            return
        else:
            print("Opción invalida. Preube de nuevo")


def entrar(biblioteca):
    """Valida el DNI y el estado del usuario para permitirle el ingreso al sistema."""
    dni = input("Escribe tu DNI: ").strip()
    try:
        usuario = biblioteca.usuario(dni)
    except errores.ErrorBiblioteca as error:
        print()
        print("No se pudo entrar: " + str(error))
        return
    if not usuario.esta_activo():
        print()
        print(f"{usuario.nombre()} no puede entrar, su usuario esta de baja")
        return
    print()
    print(f"Hola {usuario.nombre()}, tu tipo de membresia es {usuario.tipo()}")
    menu_de_sesion(biblioteca, usuario)


def menu_de_sesion(biblioteca, usuario):
    """Muestra las opciones disponibles dentro de la sesión según el tipo de usuario."""
    while True:
        print()
        print(f"MENU DE {usuario.tipo().upper()}")
        print()
        print("1) Ver el catalogo")
        print("2) Buscar un libro")
        print("3) Ver un libro por ISBN")
        print("4) Mi membresia")
        if usuario.puede_administrar():
            print("5) Ver los usuarios")
        print("0) Cerrar sesion")

        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            mostrar_catalogo(biblioteca)
        elif opcion == "2":
            buscar_libro(biblioteca)
        elif opcion == "3":
            mostrar_libro(biblioteca)
        elif opcion == "4":
            mostrar_membresia(usuario)
        elif opcion == "5" and usuario.puede_administrar():
            mostrar_usuarios(biblioteca)
        elif opcion == "0":
            return
        else:
            print("Esa opcion no existe")
        utilidades.pausa()


def mostrar_catalogo(biblioteca):
    """Muestra en pantalla la lista completa de libros disponibles en el catálogo."""
    datos = biblioteca.datos_del_catalogo()
    print()
    print(f"CATALOGO: {len(datos)} libros")
    print()
    for libro in datos:
        print(f"{libro['isbn']} | {libro['titulo']} | {libro['autor']}")
        print(
            f"   {libro['categoria']}, seccion {libro['seccion']}"
            f" ({libro['seccion_nombre']}), estante {libro['estante']},"
            f" ejemplares {libro['ejemplares']}, en el estante {libro['disponibles']},"
            f" prestados {libro['prestados']}, se puede prestar: {libro['se_puede_prestar']}"
        )
        print()


def buscar_libro(biblioteca):
    """Permite buscar libros filtrando por título, autor o categoría."""
    texto = input("Escribe una parte del titulo, del autor o de la categoria: ").strip()
    datos = biblioteca.buscar(texto)
    print()
    print(f"Con '{texto}' salieron {len(datos)} libros")
    for libro in datos:
        print(f"{libro['isbn']} | {libro['titulo']} | {libro['autor']}")
        print(
            f"   {libro['categoria']}, seccion {libro['seccion']},"
            f" estante {libro['estante']},"
            f" se puede prestar: {libro['se_puede_prestar']}"
        )


def mostrar_libro(biblioteca):
    """Muestra la información detallada de un libro consultado por su ISBN."""
    isbn = input("Escribe el ISBN del libro: ").strip()
    libro = biblioteca.datos_de_un_libro(isbn)
    print()
    print(f"Titulo: {libro['titulo']}")
    print(f"Autor: {libro['autor']}")
    print(f"ISBN: {libro['isbn']}")
    print(f"Categoria: {libro['categoria']}")
    print(f"Seccion: {libro['seccion']} {libro['seccion_nombre']}")
    print(f"Estante: {libro['estante']}")
    print(f"Ejemplares: {libro['ejemplares']}")
    print(f"En el estante: {libro['disponibles']}")
    print(f"Prestados: {libro['prestados']}")
    print(f"Se puede prestar: {libro['se_puede_prestar']}")


def mostrar_membresia(usuario):
    """Muestra los datos actuales de la membresía del usuario en sesión."""
    datos = usuario.datos_de_membresia()
    print()
    print("MEMBRESIA")
    print(f"Nombre: {datos['nombre']}")
    print(f"DNI: {datos['dni']}")
    print(f"Tipo de membresia: {datos['tipo']}")
    print(f"Vencimiento: {datos['vencimiento_membresia']}")
    print(f"Estado: {datos['estado']}")
    if "puede_administrar" in datos:
        print()
        print("ERES ADMINISTRADOR")


def mostrar_usuarios(biblioteca):
    """Muestra la lista de todos los usuarios registrados (solo para administradores)."""
    datos = biblioteca.datos_de_los_usuarios()
    print()
    print(f"USUARIOS: {len(datos)}")
    for usuario in datos:
        print(
            f"{usuario['dni']} | {usuario['nombre']} | {usuario['tipo']}"
            f" | vence {usuario['vencimiento_membresia']} | {usuario['estado']}"
        )
