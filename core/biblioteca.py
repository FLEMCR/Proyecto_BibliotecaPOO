from datetime import date, timedelta

from core import configuracion, errores, libros, prestamos, usuarios, utilidades


class Biblioteca:
    """Controlador principal del sistema que administra el catálogo, los usuarios y los préstamos."""

    def __init__(self):
        self._catalogo = {}
        self._usuarios = {}
        self._prestamos = []
        self.cargar_datos()

    def cargar_datos(self):
        """Carga y sincroniza los libros, usuarios y préstamos desde los archivos JSON."""
        self._catalogo = {}
        for registro in configuracion.leer_archivo(configuracion.ARCHIVO_LIBROS):
            libro = libros.crear_libro(registro)
            self._catalogo[libro.isbn()] = libro

        self._usuarios = {}
        for registro in configuracion.leer_archivo(configuracion.ARCHIVO_USUARIOS):
            usuario = usuarios.crear_usuario(registro)
            self._usuarios[usuario.dni()] = usuario

        self._prestamos = []
        for registro in configuracion.leer_archivo(configuracion.ARCHIVO_PRESTAMOS):
            prestamo = prestamos.crear_prestamo(registro)
            self._prestamos.append(prestamo)

        return self.resumen()

    def todos_los_libros(self):
        """Retorna una lista con todos los objetos Libro registrados en la biblioteca."""
        return list(self._catalogo.values())

    def todos_los_usuarios(self):
        """Retorna una lista con todos los objetos Usuario registrados."""
        return list(self._usuarios.values())

    def todos_los_prestamos(self):
        """Retorna una lista con todos los préstamos registrados."""
        return list(self._prestamos)

    def libro(self, isbn):
        """Busca y retorna un libro específico por su ISBN; lanza error si no existe."""
        isbn_buscado = utilidades.validar_isbn(isbn)
        if isbn_buscado not in self._catalogo:
            raise errores.ErrorDeDatos(
                f"No hay ningun libro con el ISBN {isbn_buscado}"
            )
        return self._catalogo[isbn_buscado]

    def usuario(self, dni):
        """Busca y retorna un usuario específico por su DNI; lanza error si no existe."""
        dni_buscado = utilidades.validar_dni(dni)
        if dni_buscado not in self._usuarios:
            raise errores.ErrorDeDatos(
                f"No hay ningun usuario con el DNI {dni_buscado}"
            )
        return self._usuarios[dni_buscado]

    def datos_de_un_libro(self, isbn):
        """Retorna los datos detallados de un libro específico para su visualización."""
        return self.libro(isbn).datos_para_pantalla()

    def buscar_avanzado(
        self,
        texto="",
        campo="Todo",
        categoria="Todas",
        solo_disponibles=False,
        ordenar_por="Título",
        limite=None,
    ):
        """Filtra, ordena y recorta el catálogo según los filtros de la interfaz."""
        encontrados = []
        for libro in self.todos_los_libros():
            if not self._coincide_con_el_campo(libro, texto, campo):
                continue
            if categoria not in ("", None, "Todas") and libro.categoria() != categoria:
                continue
            if solo_disponibles and not libro.se_puede_prestar():
                continue
            encontrados.append(libro)

        encontrados.sort(key=lambda libro: self._clave_de_orden(libro, ordenar_por))
        if limite is not None:
            encontrados = encontrados[: int(limite)]
        return libros.datos_del_catalogo(encontrados)

    def _coincide_con_el_campo(self, libro, texto, campo):
        """Verifica si un libro coincide con el texto en el campo elegido."""
        buscado = utilidades.normalizar_texto(texto)
        if buscado == "":
            return True

        titulo = utilidades.normalizar_texto(libro.titulo())
        autor = utilidades.normalizar_texto(libro.autor())
        categoria = utilidades.normalizar_texto(libro.categoria())
        isbn = utilidades.normalizar_texto(libro.isbn())

        if campo == "ISBN":
            return buscado in isbn
        if campo == "Título":
            return buscado in titulo
        if campo == "Autor":
            return buscado in autor
        if campo == "Categoría":
            return buscado in categoria
        return (
            buscado in titulo
            or buscado in autor
            or buscado in categoria
            or buscado in isbn
        )

    def _clave_de_orden(self, libro, ordenar_por):
        """Devuelve la clave de orden para un libro según la opción elegida."""
        if ordenar_por == "Autor":
            return (utilidades.normalizar_texto(libro.autor()), libro.isbn())
        if ordenar_por == "Categoría":
            return (
                utilidades.normalizar_texto(libro.categoria()),
                utilidades.normalizar_texto(libro.titulo()),
            )
        if ordenar_por in ("Disponibilidad", "Disponibles para préstamo"):
            return (-libro.disponibles(), utilidades.normalizar_texto(libro.titulo()))
        return (utilidades.normalizar_texto(libro.titulo()), libro.isbn())

    def categorias(self):
        """Retorna las categorías presentes en el catálogo, sin repetir y ordenadas."""
        return sorted({libro.categoria() for libro in self.todos_los_libros()})

    def guardar_libros(self):
        """Escribe todos los libros cargados en libros.json."""
        configuracion.escribir_archivo(
            configuracion.ARCHIVO_LIBROS,
            [libro.a_diccionario() for libro in self.todos_los_libros()],
        )

    def guardar_usuarios(self):
        """Escribe todos los usuarios cargados en usuarios.json."""
        configuracion.escribir_archivo(
            configuracion.ARCHIVO_USUARIOS,
            [usuario.a_diccionario() for usuario in self._usuarios.values()],
        )

    def guardar_prestamos(self):
        """Escribe todos los préstamos cargados en prestamos.json."""
        configuracion.escribir_archivo(
            configuracion.ARCHIVO_PRESTAMOS,
            [prestamo.a_diccionario() for prestamo in self._prestamos],
        )

    def registrar_libro(self, datos):
        """Crea un libro nuevo y lo guarda en el catálogo."""
        if not isinstance(datos, dict):
            raise errores.ErrorDeDatos("Los datos del libro deben ser un diccionario")
        isbn = utilidades.validar_isbn(datos.get("isbn"))
        if isbn in self._catalogo:
            raise errores.ErrorDeDatos(f"Ya existe un libro con el ISBN {isbn}")
        libro = libros.crear_libro(datos)
        self._catalogo[libro.isbn()] = libro
        self.guardar_libros()
        return libro

    def actualizar_libro(self, isbn, datos):
        """Modifica un libro existente y guarda los cambios."""
        libro_actual = self.libro(isbn)
        datos_actualizados = dict(datos)
        datos_actualizados["isbn"] = libro_actual.isbn()
        libro = libros.crear_libro(datos_actualizados)
        self._catalogo[libro.isbn()] = libro
        self.guardar_libros()
        return libro

    def eliminar_libro(self, isbn):
        """Elimina un libro del catálogo si no tiene préstamos activos."""
        libro = self.libro(isbn)
        for prestamo in self._prestamos:
            if prestamo.isbn() == libro.isbn() and prestamo.esta_activo():
                raise errores.ErrorDeDatos(
                    "No se puede eliminar un libro con un prestamo activo"
                )
        del self._catalogo[libro.isbn()]
        self.guardar_libros()
        return libro

    def registrar_usuario(
        self, datos, permitir_administrador=False, fecha_de_alta=None
    ):
        """Registra un usuario nuevo, calcula su vencimiento y lo guarda en el JSON."""
        if not isinstance(datos, dict):
            raise errores.ErrorDeDatos("Los datos del usuario deben ser un diccionario")

        dni = utilidades.validar_dni(datos.get("dni"))
        if dni in self._usuarios:
            raise errores.ErrorDeDatos(f"Ya existe un usuario con el DNI {dni}")

        nombre = str(datos.get("nombre", "")).strip()
        tipo = str(datos.get("tipo", "Estudiante")).strip()
        if tipo == "Administrador" and not permitir_administrador:
            raise errores.ErrorDeDatos(
                "No se puede crear un administrador desde el acceso"
            )

        fecha_de_alta = fecha_de_alta or date.today()
        vencimiento = datos.get("vencimiento_membresia")
        if vencimiento is None:
            vencimiento = utilidades.sumar_meses(
                fecha_de_alta, configuracion.MESES_DE_MEMBRESIA
            )

        usuario = usuarios.crear_usuario(
            {
                "dni": dni,
                "nombre": nombre,
                "tipo": tipo,
                "vencimiento_membresia": str(vencimiento),
                "activo": True,
            }
        )
        self._usuarios[usuario.dni()] = usuario
        self.guardar_usuarios()
        return usuario

    def prestamo_activo_de_usuario(self, dni):
        """Devuelve el préstamo activo del usuario o None si no tiene ninguno."""
        dni_buscado = utilidades.validar_dni(dni)
        for prestamo in self._prestamos:
            if prestamo.dni() == dni_buscado and prestamo.esta_activo():
                return prestamo
        return None

    def prestamos_activos(self):
        """Retorna todos los préstamos que todavía no fueron devueltos."""
        return [prestamo for prestamo in self._prestamos if prestamo.esta_activo()]

    def prestamos_de_usuario(self, dni):
        """Retorna el historial de préstamos de un usuario."""
        dni_buscado = utilidades.validar_dni(dni)
        return [
            prestamo for prestamo in self._prestamos if prestamo.dni() == dni_buscado
        ]

    def prestar(self, isbn, dni):
        """Registra un préstamo si el usuario y el libro cumplen las reglas."""
        usuario = self.usuario(dni)
        if not usuario.esta_activo() or not usuario.tiene_membresia_vigente():
            raise errores.ErrorDeDatos("El usuario no puede recibir prestamos")
        if self.prestamo_activo_de_usuario(usuario.dni()) is not None:
            raise errores.ErrorDeDatos(
                "El usuario ya tiene un libro prestado; debe devolverlo primero"
            )

        libro = self.libro(isbn)
        if not libro.se_puede_prestar():
            raise errores.ErrorDeDatos(
                "No hay ejemplares disponibles para prestar de este libro"
            )

        libro.prestar_ejemplar()
        hoy = date.today()
        prestamo = prestamos.Prestamo(
            libro.isbn(),
            usuario.dni(),
            hoy,
            hoy + timedelta(days=configuracion.DIAS_DE_PRESTAMO),
            identificador=self._siguiente_identificador_de_prestamo(),
        )
        self._prestamos.append(prestamo)
        self.guardar_libros()
        self.guardar_prestamos()
        return prestamo

    def devolver(self, isbn, dni):
        """Registra la devolución de un préstamo activo y repone el ejemplar."""
        libro = self.libro(isbn)
        dni_buscado = utilidades.validar_dni(dni)
        prestamo_activo = None
        for prestamo in self._prestamos:
            if (
                prestamo.isbn() == libro.isbn()
                and prestamo.dni() == dni_buscado
                and prestamo.esta_activo()
            ):
                prestamo_activo = prestamo
                break

        if prestamo_activo is None:
            raise errores.ErrorDeDatos(
                "No hay un prestamo activo de este libro para ese usuario"
            )

        prestamo_activo.marcar_devuelto(date.today())
        libro.devolver_ejemplar()
        self.guardar_libros()
        self.guardar_prestamos()
        return prestamo_activo

    def _siguiente_identificador_de_prestamo(self):
        """Genera el siguiente identificador consecutivo de préstamo."""
        return f"P-{len(self._prestamos) + 1:04d}"

    def resumen(self):
        """Calcula y retorna un diccionario con estadísticas generales del estado de la biblioteca."""
        total_ejemplares = 0
        total_disponibles = 0
        for libro in self.todos_los_libros():
            total_ejemplares = total_ejemplares + libro.ejemplares()
            total_disponibles = total_disponibles + libro.disponibles()
        return {
            "biblioteca": configuracion.NOMBRE_BIBLIOTECA,
            "fecha_de_hoy": str(date.today()),
            "titulos": len(self._catalogo),
            "ejemplares": total_ejemplares,
            "disponibles": total_disponibles,
            "prestados": total_ejemplares - total_disponibles,
            "usuarios": len(self._usuarios),
        }
