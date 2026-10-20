from datetime import date, timedelta

from modulos import config, errores


class Prestamo:
    def __init__(self, codigo, libro, usuario, fecha=None, dias=None):
        self._codigo = codigo
        self._libro = libro
        self._usuario = usuario
        self._fecha = fecha or date.today()
        self._dias = int(dias) if dias else usuario.membresia().dias_prestamo()
        self._vence = self._fecha + timedelta(days=self._dias)
        self._devuelto = False
        self._multa = 0.0

    def codigo(self):
        return self._codigo

    def isbn(self):
        return self._libro.isbn()

    def dni(self):
        return self._usuario.dni()

    def vence(self):
        return self._vence

    def devuelto(self):
        return self._devuelto

    def multa(self):
        return self._multa

    def libro(self):
        return self._libro

    def usuario(self):
        return self._usuario

    def estado(self):
        if self._devuelto:
            return "Devuelto"
        return "Activo"

    def devolver(self, hoy=None):
        self._devuelto = True
        hoy = hoy or date.today()
        if hoy > self._vence:
            dias_retraso = (hoy - self._vence).days
            self._multa = round(
                dias_retraso * self._usuario.membresia().multa_por_dia(), 2
            )
        return self._multa

    def a_diccionario(self):
        return {
            "codigo": self._codigo,
            "isbn": self.isbn(),
            "dni": self.dni(),
            "fecha": str(self._fecha),
            "vence": str(self._vence),
            "devuelto": self._devuelto,
            "multa": self._multa,
        }


class GestorPrestamos:
    def __init__(self, catalogo, miembros):
        self._catalogo = catalogo
        self._miembros = miembros
        self._prestamos = []
        self._contador = 0

    def prestar(self, isbn, dni, hoy=None):
        libro = self._catalogo.get(isbn)
        if libro is None:
            raise errores.DatosInvalidosError(f"El ISBN {isbn} no esta en el catalogo")
        usuario = self._miembros.get(dni)
        if usuario is None:
            raise errores.DatosInvalidosError(f"El DNI {dni} no esta registrado")
        libro.prestar_uno()
        self._contador += 1
        prestamo = Prestamo(
            f"P-{self._contador:04d}", libro, usuario, hoy or date.today()
        )
        self._prestamos.append(prestamo)
        return prestamo

    def devolver(self, codigo, hoy=None):
        for prestamo in self._prestamos:
            if prestamo.codigo() == codigo and not prestamo.devuelto():
                multa = prestamo.devolver(hoy)
                prestamo.libro().devolver_uno()
                return multa
        raise errores.DatosInvalidosError(
            f"No se encontro el prestamo {codigo} o ya fue devuelto"
        )

    def prestamos(self):
        return list(self._prestamos)

    def historial_de(self, dni):
        return [p for p in self._prestamos if p.dni() == dni]

    def activos_de(self, dni):
        return [p for p in self._prestamos if p.dni() == dni and not p.devuelto()]

    def a_lista(self):
        return [p.a_diccionario() for p in self._prestamos]
