from datetime import date

from modulos import config, errores, libros, utilidades


def portada():
    print(utilidades.titulo(config.nombre_biblioteca))
    print((config.lema).center(60))
    print(f" Fecha de hoy: {date.today()}")
    utilidades.pausa()


def mostrar_opciones(opciones):
    for codigo, texto, _ in opciones:
        print(f"{codigo}) {texto}")


def leer_opcion(opciones):
    validos = [c for c, _, _ in opciones]
    while True:
        entrada = input("Elige una opcion: ").strip()
        if entrada in validos:
            return entrada
        print(f"Opcion no valida. Intenta con: {', '.join(validos)}")


def accion_catalogo(biblioteca):
    print(utilidades.titulo("Catalogo disponible"))
    for isbn, libro in biblioteca.catalogo().items():
        print(f"{isbn} | {libro.titulo()} | {libro.autor()}")
        print(
            f"   Categoria: {libro.categoria()} | Seccion {libro.seccion()}, estante {libro.estante()}"
        )
        print(
            f"   Ejemplares: {libro.ejemplares()} | Disponibles: {libro.disponibles_prestamo()}"
        )


def accion_buscar_categoria(biblioteca):
    print(utilidades.titulo("Busqueda recursiva por categoria"))
    nombre = input("Categoria (por ejemplo Literatura o Narrativa): ").strip()
    encontradas = libros.buscar_por_categoria(
        list(biblioteca.catalogo().values()), nombre
    )
    if encontradas:
        print(f"Se encontraron {len(encontradas)} titulos en '{nombre}':")
        for libro in encontradas:
            print(
                f"  - {libro.titulo()} ({' > '.join(libros.niveles_categoria(libro.categoria()))})"
            )
    else:
        print(f"No hay titulos en la categoria '{nombre}'.")


def accion_mi_membresia(biblioteca):
    miembro = biblioteca.sesion()
    print(utilidades.titulo("Mi membresia"))
    print(f"Miembro: {miembro.nombre()} ({miembro.dni()})")
    print(f"Tipo: {miembro.tipo().capitalize()}")
    print(f"Estado: {miembro.estado()}")
    print(f"Vence: {miembro.vencimiento()}")
    print(f"Limite de libros: {miembro.membresia().limite_libros()}")
    print(f"Dias de prestamo: {miembro.membresia().dias_prestamo()}")
    print(f"Multa por dia de retraso: S/{miembro.membresia().multa_por_dia():.2f}")
    print(f"Puede administrar: {'si' if miembro.puede_administrar() else 'no'}")
    print(f"{miembro.membresia().describir()}")


def accion_estado(biblioteca):
    r = biblioteca.resumen()
    print(utilidades.titulo("Estado de la biblioteca"))
    print(f"Fecha del sistema: {date.today()}")
    print(f"Titulos: {r['titulos']} | Ejemplares: {r['ejemplares']}")
    print(f"Disponibles: {r['disponibles']} | Prestados: {r['prestados']}")
    print(f"Miembros: {r['miembros']}")


def accion_miembros(biblioteca):
    print(utilidades.titulo("Miembros registrados"))
    print(f"{'DNI':<10}{'Nombre':<22}{'Tipo':<14}{'Vence':<12}{'Estado':<10}")
    print("-" * 68)
    for dni, miembro in biblioteca.miembros().items():
        print(
            f"{dni:<10}{miembro.nombre()[:20]:<22}{miembro.tipo().capitalize():<14}"
            f"{str(miembro.vencimiento()):<12}{miembro.estado():<10}"
        )


def imprimir_matriz(matriz):
    columnas = max(len(fila) for fila in matriz)
    anchos = [0] * columnas
    for fila in matriz:
        for indice, celda in enumerate(fila):
            anchos[indice] = max(anchos[indice], len(str(celda)))
    for fila in matriz:
        celdas = [str(celda).ljust(anchos[indice]) for indice, celda in enumerate(fila)]
        print("  ".join(celdas).rstrip())


def accion_matriz_disponibilidad(biblioteca):
    print(utilidades.titulo("Matriz de disponibilidad"))
    imprimir_matriz(biblioteca.matrices()["disponibilidad"])
    print(
        "Filas = secciones, columnas = estantes. La ultima fila y columna son totales."
    )


def accion_matriz_ubicacion(biblioteca):
    print(utilidades.titulo("Matriz de ubicacion"))
    imprimir_matriz(biblioteca.matrices()["ubicacion"])
    print("Cuanta coleccion guarda cada estante de cada seccion.")


def accion_matriz_categorias(biblioteca):
    print(utilidades.titulo("Matriz de categorias"))
    imprimir_matriz(biblioteca.matrices()["categorias"])
    print("Se agrupa por el primer nivel de la categoria (antes de la /).")


def accion_guardar(biblioteca):
    if not utilidades.responder_si_no(
        "Se sobreescribiran los JSON de la carpeta datos/. Continuar (s/n): "
    ):
        print("No se guardo nada.")
        return
    biblioteca.guardar_datos()
    print("Cambios guardados en la carpeta datos/.")


def menu_admin(biblioteca):
    while True:
        print(utilidades.titulo("Menu de administracion"))
        mostrar_opciones(ADMIN)
        opcion = leer_opcion(ADMIN)
        if opcion == "0":
            print("Sesion cerrada.")
            return None
        if opcion == "3":
            while True:
                print(utilidades.titulo("Matrices y busqueda recursiva"))
                mostrar_opciones(MATRICES)
                eleccion = leer_opcion(MATRICES)
                if eleccion == "0":
                    break
                for codigo, texto, accion in MATRICES:
                    if codigo == eleccion:
                        accion(biblioteca)
                utilidades.pausa()
            continue
        for codigo, texto, accion in ADMIN:
            if codigo == opcion:
                accion(biblioteca)
        utilidades.pausa()


def menu_invitado(biblioteca):
    while True:
        print(utilidades.titulo("Menu de invitado"))
        mostrar_opciones(INVITADO)
        opcion = leer_opcion(INVITADO)
        if opcion == "0":
            print("Gracias por visitar la biblioteca.")
            return None
        for codigo, texto, accion in INVITADO:
            if codigo == opcion:
                accion(biblioteca)
        utilidades.pausa()


def menu_miembro(biblioteca, miembro):
    while True:
        print(utilidades.titulo(f"Menu de {miembro.nombre()}"))
        mostrar_opciones(MIEMBRO)
        opcion = leer_opcion(MIEMBRO)
        if opcion == "0":
            print("Sesion cerrada. Hasta pronto.")
            return None
        for codigo, texto, accion in MIEMBRO:
            if codigo == opcion:
                accion(biblioteca)
        utilidades.pausa()


def menu_principal(biblioteca):
    while True:
        print(utilidades.titulo(config.nombre_biblioteca))
        mostrar_opciones(ACCESO)
        opcion = leer_opcion(ACCESO)
        if opcion == "0":
            print("Saliendo del sistema...")
            return
        if opcion == "1":
            try:
                dni = utilidades.validar_dni(input("DNI del miembro: "))
            except errores.DatosInvalidosError as error:
                print(error)
                continue
            miembro = biblioteca.iniciar_sesion(dni)
            if miembro is None:
                print(f"No hay ningun miembro registrado con el DNI {dni}.")
                continue
            if not miembro.activo():
                print(
                    f"{miembro.nombre()} esta dado de baja. Consulta con administracion."
                )
                continue
            print(f"Bienvenido, {miembro.nombre()} ({miembro.tipo()}).")
            if miembro.puede_administrar():
                menu_admin(biblioteca)
            else:
                menu_miembro(biblioteca, miembro)
            biblioteca.cerrar_sesion()
            continue
        biblioteca.iniciar_sesion(invitado=True)
        print("Ingresaste como invitado: solo puedes consultar el catalogo.")
        menu_invitado(biblioteca)
        biblioteca.cerrar_sesion()


ACCESO = [
    ("1", "Iniciar sesion (DNI)", None),
    ("2", "Ingresar como invitado", None),
    ("0", "Salir", None),
]

MIEMBRO = [
    ("1", "Consultar catalogo", accion_catalogo),
    ("2", "Buscar por categoria (recursiva)", accion_buscar_categoria),
    ("3", "Mi membresia", accion_mi_membresia),
    ("0", "Cerrar sesion", None),
]

INVITADO = [
    ("1", "Consultar catalogo", accion_catalogo),
    ("2", "Buscar por categoria (recursiva)", accion_buscar_categoria),
    ("0", "Salir", None),
]

ADMIN = [
    ("1", "Estado de la biblioteca", accion_estado),
    ("2", "Miembros", accion_miembros),
    ("3", "Matrices y busqueda recursiva", None),
    ("4", "Guardar cambios en los JSON", accion_guardar),
    ("0", "Cerrar sesion", None),
]

MATRICES = [
    ("1", "Disponibilidad por seccion y estante", accion_matriz_disponibilidad),
    ("2", "Titulos por seccion y estante", accion_matriz_ubicacion),
    ("3", "Categorias principales", accion_matriz_categorias),
    ("4", "Busqueda recursiva por categoria", accion_buscar_categoria),
    ("0", "Volver al menu de administracion", None),
]
