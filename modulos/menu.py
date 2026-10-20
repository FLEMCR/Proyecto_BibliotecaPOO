from modulos import config, errores, utilidades

ACCESO = [
    ("1", "Iniciar sesion con tu DNI"),
    ("2", "Ingresar como invitado"),
    ("0", "Salir"),
]

MIEMBRO = [
    ("1", "Ver catalogo de libros"),
    ("2", "Mis prestamos"),
    ("0", "Cerrar sesion"),
]

PRESTAMOS = [
    ("1", "Pedir un libro"),
    ("2", "Devolver un libro"),
    ("0", "Volver"),
]

INVITADO = [
    ("1", "Ver catalogo de libros"),
    ("0", "Volver"),
]


def mostrar_opciones(titulo_pantalla, opciones):
    print(utilidades.titulo(titulo_pantalla))
    print()
    for numero, texto in opciones:
        print(f"  {numero.rjust(2)} {texto}")
    print()


def leer_opcion(opciones, texto="Opcion: "):
    validos = [numero for numero, _ in opciones]
    while True:
        eleccion = input(texto).strip()
        encontrado = False
        for valido in validos:
            if eleccion == valido:
                encontrado = True
                break
        if encontrado:
            return eleccion
        print("Opcion invalida")


def ejecutar_opcion(accion, biblioteca, pausa=True):
    try:
        accion(biblioteca)
    except errores.DatosInvalidosError as error:
        print(str(error))
    if pausa:
        utilidades.pausa()


def accion_ver_catalogo(biblioteca):
    print(utilidades.titulo("Catalogo de libros"))
    if not biblioteca.catalogo():
        print("No hay libros cargados")
        return
    for libro in biblioteca.catalogo().values():
        print(
            f"  {libro.isbn()} | {libro.titulo()} | {libro.autor()} | {libro.categoria()} | disp: {libro.disponibles_prestamo()}"
        )


def accion_prestar(biblioteca, miembro):
    isbn = input("ISBN del libro: ").strip()
    prestamo = biblioteca.prestar(isbn, miembro.dni())
    print(f"Prestamo {prestamo.codigo()} registrado. Vence el {prestamo.vence()}")


def accion_devolver(biblioteca):
    codigo = input("Codigo del prestamo (ej. P-0001): ").strip()
    multa = biblioteca.devolver(codigo)
    if multa > 0:
        print(f"Devuelto con retraso. Multa: S/ {multa:.2f}")
    else:
        print("Devuelto correctamente")


def submenu_prestamos(biblioteca, miembro):
    while True:
        print(utilidades.titulo(f"Mis prestamos - {miembro.nombre()}"))
        prestamos = biblioteca.prestamos_de(miembro.dni())
        if prestamos:
            for p in prestamos:
                print(
                    f"  {p.codigo()} | {p.libro().titulo()} | vence {p.vence()} | {p.estado()}"
                )
        else:
            print("No tienes prestamos registrados")
        print()
        mostrar_opciones("Opciones de prestamo", PRESTAMOS)
        opcion = leer_opcion(PRESTAMOS)
        if opcion == "1":
            accion_prestar(biblioteca, miembro)
            utilidades.pausa()
        elif opcion == "2":
            accion_devolver(biblioteca)
            utilidades.pausa()
        else:
            return


def menu_miembro(biblioteca, miembro):
    while True:
        mostrar_opciones(f"Menu de {miembro.tipo()} - {miembro.nombre()}", MIEMBRO)
        opcion = leer_opcion(MIEMBRO)
        if opcion == "1":
            ejecutar_opcion(accion_ver_catalogo, biblioteca)
        elif opcion == "2":
            submenu_prestamos(biblioteca, miembro)
        else:
            return


def menu_invitado(biblioteca):
    while True:
        mostrar_opciones("Menu de invitado (solo consulta)", INVITADO)
        opcion = leer_opcion(INVITADO)
        if opcion == "1":
            ejecutar_opcion(accion_ver_catalogo, biblioteca)
        else:
            return


def menu_acceso(biblioteca):
    while True:
        mostrar_opciones("Bienvenido", ACCESO)
        opcion = leer_opcion(ACCESO)
        if opcion == "1":
            dni = input("DNI (8 digitos): ").strip()
            try:
                utilidades.validar_dni(dni)
            except errores.DatosInvalidosError as error:
                print(str(error))
                utilidades.pausa()
                continue
            miembro = biblioteca.miembro(dni)
            if miembro is None:
                print("DNI no registrado")
                utilidades.pausa()
                continue
            print(f"Hola {miembro.nombre()}, eres {miembro.tipo()}")
            utilidades.pausa()
            menu_miembro(biblioteca, miembro)
            return
        elif opcion == "2":
            print("Entrando como invitado (solo consulta)")
            utilidades.pausa()
            menu_invitado(biblioteca)
            return
        else:
            raise SystemExit(0)


def ejecutar(biblioteca):
    print(utilidades.titulo(config.nombre_biblioteca))
    print(config.lema)
    print()
    while True:
        menu_acceso(biblioteca)
        if not utilidades.responder_si_no("¿Quieres cerrar tu sesión? (s/n): "):
            break
    print()
    print(utilidades.titulo(f"Gracias por usar {config.nombre_biblioteca}"))
