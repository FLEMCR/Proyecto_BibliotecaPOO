from modulos import configuracion, errores


def pausa():
    input("Pulsa ENTER para volver al menu")


def portada(biblioteca):
    resumen = biblioteca.resumen()
    print()
    print(resumen["biblioteca"])
    if configuracion.LEMA != "":
        print(configuracion.LEMA)
    print("Hoy es " + resumen["fecha_de_hoy"])
    print(
        "Hay "
        + str(resumen["titulos"])
        + " titulos, "
        + str(resumen["ejemplares"])
        + " ejemplares y "
        + str(resumen["usuarios"])
        + " usuarios registrados"
    )


def mostrar_catalogo(biblioteca):
    datos = biblioteca.datos_del_catalogo()
    print()
    print("CATALOGO: " + str(len(datos)) + " libros")
    for libro in datos:
        print(libro["isbn"] + " | " + libro["titulo"] + " | " + libro["autor"])
        print(
            "   "
            + libro["categoria"]
            + ", seccion "
            + libro["seccion"]
            + " ("
            + libro["seccion_nombre"]
            + "), estante "
            + str(libro["estante"])
            + ", ejemplares "
            + str(libro["ejemplares"])
            + ", en el estante "
            + str(libro["disponibles"])
            + ", prestados "
            + str(libro["prestados"])
            + ", se puede prestar: "
            + libro["se_puede_prestar"]
        )


def buscar_libro(biblioteca):
    texto = input("Escribe una parte del titulo, del autor o de la categoria: ").strip()
    datos = biblioteca.buscar(texto)
    print()
    print("Con '" + texto + "' salieron " + str(len(datos)) + " libros")
    for libro in datos:
        print(libro["isbn"] + " | " + libro["titulo"] + " | " + libro["autor"])
        print(
            "   "
            + libro["categoria"]
            + ", seccion "
            + libro["seccion"]
            + ", estante "
            + str(libro["estante"])
            + ", se puede prestar: "
            + libro["se_puede_prestar"]
        )


def mostrar_libro(biblioteca):
    isbn = input("Escribe el ISBN del libro: ").strip()
    libro = biblioteca.datos_de_un_libro(isbn)
    print()
    print("Titulo: " + libro["titulo"])
    print("Autor: " + libro["autor"])
    print("ISBN: " + libro["isbn"])
    print("Categoria: " + libro["categoria"])
    print("Seccion: " + libro["seccion"] + " - " + libro["seccion_nombre"])
    print("Estante: " + str(libro["estante"]))
    print("Ejemplares: " + str(libro["ejemplares"]))
    print("En el estante: " + str(libro["disponibles"]))
    print("Prestados: " + str(libro["prestados"]))
    print("Se puede prestar: " + libro["se_puede_prestar"])


def mostrar_membresia(usuario):
    datos = usuario.datos_de_membresia()
    print()
    print("MIEMBRESIA")
    print("Nombre: " + datos["nombre"])
    print("DNI: " + datos["dni"])
    print("Tipo de usuario: " + datos["tipo"])
    print("Vencimiento: " + datos["vencimiento_membresia"])
    print("Estado: " + datos["estado"])
    if "puede_administrar" in datos:
        print("Puede administrar: " + datos["puede_administrar"])


def mostrar_usuarios(biblioteca):
    datos = biblioteca.datos_de_los_usuarios()
    print()
    print("USUARIOS: " + str(len(datos)))
    for usuario in datos:
        print(
            usuario["dni"]
            + " | "
            + usuario["nombre"]
            + " | "
            + usuario["tipo"]
            + " | vence "
            + usuario["vencimiento_membresia"]
            + " | "
            + usuario["estado"]
        )


def entrar(biblioteca):
    dni = input("Escribe tu DNI: ").strip()
    try:
        usuario = biblioteca.usuario(dni)
    except errores.ErrorBiblioteca as error:
        print()
        print("No se pudo entrar: " + str(error))
        return
    if not usuario.esta_activo():
        print()
        print(usuario.nombre() + " no puede entrar, su usuario esta de baja")
        return
    print()
    print("Hola " + usuario.nombre() + ", tu tipo de usuario es " + usuario.tipo())
    menu_de_sesion(biblioteca, usuario)


def menu_de_sesion(biblioteca, usuario):
    while True:
        print()
        print("MENU DE " + usuario.tipo().upper())
        print("1) Ver el catalogo")
        print("2) Buscar un libro")
        print("3) Ver un libro por ISBN")
        print("4) Mi membresia")
        if usuario.puede_administrar():
            print("5) Ver los usuarios")
        print("0) Cerrar sesion")
        opcion = input("Elige una opcion: ").strip()
        if opcion == "0":
            return
        try:
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
            else:
                print("Esa opcion no existe")
        except errores.ErrorBiblioteca as error:
            print("No se pudo: " + str(error))
        pausa()


def menu_de_acceso(biblioteca):
    while True:
        print()
        print("MENU DE ACCESO")
        print("1) Entrar con mi DNI")
        print("0) Salir")
        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            entrar(biblioteca)
        elif opcion == "0":
            print("Hasta luego")
            return
        else:
            print("Esa opcion no existe")
