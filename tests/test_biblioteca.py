"""Pruebas básicas del dominio de la biblioteca."""

import unittest

from core import errores, libros
from core.biblioteca import Biblioteca


class PruebasBiblioteca(unittest.TestCase):
    def setUp(self):
        self.biblioteca = Biblioteca()

    def test_resumen_inicial(self):
        resumen = self.biblioteca.resumen()
        self.assertEqual(resumen["titulos"], 22)
        self.assertEqual(resumen["usuarios"], 13)
        self.assertGreaterEqual(resumen["ejemplares"], resumen["disponibles"])

    def test_buscar_por_isbn(self):
        datos = self.biblioteca.buscar_avanzado("9788437604947", campo="ISBN")
        self.assertEqual(len(datos), 1)
        self.assertEqual(datos[0]["titulo"], "Cien años de soledad")

    def test_buscar_por_titulo_ignora_tildes(self):
        datos = self.biblioteca.buscar_avanzado("anos", campo="titulo")
        titulos = [libro["titulo"] for libro in datos]
        self.assertIn("Cien años de soledad", titulos)

    def test_buscar_por_autor(self):
        datos = self.biblioteca.buscar_avanzado("tolkien", campo="autor")
        self.assertEqual(len(datos), 1)
        self.assertIn("Tolkien", datos[0]["autor"])

    def test_buscar_por_categoria(self):
        datos = self.biblioteca.buscar_avanzado(categoria="Arte")
        self.assertEqual(len(datos), 4)
        self.assertTrue(all(libro["categoria"] == "Arte" for libro in datos))

    def test_solo_disponibles_para_prestar(self):
        datos = self.biblioteca.buscar_avanzado(solo_disponibles=True)
        self.assertTrue(datos)
        self.assertTrue(all(libro["disponibles"] > 1 for libro in datos))

    def test_limite_de_resultados(self):
        datos = self.biblioteca.buscar_avanzado(limite=5)
        self.assertEqual(len(datos), 5)

    def test_busqueda_sin_resultados(self):
        datos = self.biblioteca.buscar_avanzado("xyz", campo="titulo")
        self.assertEqual(datos, [])

    def test_usuario_vencido_no_tiene_membresia_vigente(self):
        usuario = self.biblioteca.usuario("76789012")
        self.assertFalse(usuario.tiene_membresia_vigente())

    def test_usuario_de_baja(self):
        usuario = self.biblioteca.usuario("70778899")
        self.assertFalse(usuario.esta_activo())
        self.assertEqual(usuario.estado(), "De baja")

    def test_regla_del_ejemplar_que_se_queda(self):
        libro = self.biblioteca.libro("9789972433353")
        self.assertEqual(libro.ejemplares(), 1)
        self.assertFalse(libro.se_puede_prestar())

    def test_prestados_se_calcula(self):
        libro = self.biblioteca.libro("9788437604947")
        self.assertEqual(libro.prestados(), libro.ejemplares() - libro.disponibles())

    def test_libro_incompleto_lanza_error(self):
        with self.assertRaises(errores.ErrorDeDatos):
            libros.crear_libro(
                {
                    "isbn": "9780000000001",
                    "titulo": "Sin categoria",
                    "autor": "Alguien",
                    "seccion": "A",
                    "estante": 1,
                    "ejemplares": 1,
                    "disponibles": 1,
                }
            )

    def test_categorias_sin_repetir(self):
        categorias = self.biblioteca.categorias()
        self.assertEqual(categorias, sorted(set(categorias)))
        self.assertIn("Literatura", categorias)


if __name__ == "__main__":
    unittest.main()
