"""
Pruebas unitarias para la clase EtiquetaManager del sistema ToDoList.

Este módulo verifica la correcta creación, obtención, actualización y eliminación
de etiquetas, así como la recuperación de las etiquetas iniciales. También valida
el manejo de errores esperados (como duplicados) e inesperados (errores de base de datos).
"""

import unittest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.logica.etiqueta_manager import EtiquetaManager
from src.modelo.database import Session, Base, engine

ETIQUETAS_INICIALES = [
    {"nombre_etiqueta": "Personal", "color": "Verde"},
    {"nombre_etiqueta": "Urgente", "color": "Rojo"},
    {"nombre_etiqueta": "Casa", "color": "Azul"},
    {"nombre_etiqueta": "Universidad", "color": "Amarillo"},
]

class TestEtiquetaManager(unittest.TestCase):
    """
    Conjunto de pruebas unitarias para la clase EtiquetaManager.

    Métodos:
        setUp: Inicializa la base de datos y crea etiquetas iniciales.
        tearDown: Revierte y cierra la sesión tras cada prueba.
    """

    def setUp(self):
        """
        Configura la base de datos limpia y prepara la sesión y el manager,
        insertando las etiquetas iniciales para cada prueba.
        """
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.manager = EtiquetaManager(self.session)
        for etiq in ETIQUETAS_INICIALES:
            self.manager.crear_etiqueta(etiq["nombre_etiqueta"], etiq["color"])

    def tearDown(self):
        """
        Revierte cualquier cambio y cierra la sesión después de cada prueba.
        """
        self.session.rollback()
        self.session.close()

    def test_crear_etiqueta(self):
        """Prueba que se cree una etiqueta con nombre y color correctos."""
        etiqueta = self.manager.crear_etiqueta("Trabajo", "Rojo")
        self.assertIsNotNone(etiqueta.id_etiqueta)
        self.assertEqual(etiqueta.nombre_etiqueta, "Trabajo")
        self.assertEqual(etiqueta.color, "Rojo")

    def test_obtener_etiqueta(self):
        """Prueba la obtención correcta de una etiqueta por su ID."""
        etiqueta = self.manager.crear_etiqueta("TrabajoExtra", "Azul")
        etiqueta_leida = self.manager.obtener_etiqueta_por_id(etiqueta.id_etiqueta)
        self.assertEqual(etiqueta_leida.nombre_etiqueta, "TrabajoExtra")
        self.assertEqual(etiqueta_leida.color, "Azul")

    def test_obtener_etiquetas_iniciales(self):
        """Verifica que todas las etiquetas iniciales están presentes en la base de datos."""
        etiquetas = self.manager.obtener_etiquetas()
        nombres = [e.nombre_etiqueta for e in etiquetas]
        for etiq in ETIQUETAS_INICIALES:
            self.assertIn(etiq["nombre_etiqueta"], nombres)

    def test_actualizar_etiqueta(self):
        """Prueba la actualización del nombre y color de una etiqueta existente."""
        etiqueta = self.manager.crear_etiqueta("Temporal", "Verde")
        etiqueta_actualizada = self.manager.actualizar_etiqueta(
            etiqueta.id_etiqueta, nombre_etiqueta="Ocio", color="Amarillo"
        )
        self.assertEqual(etiqueta_actualizada.nombre_etiqueta, "Ocio")
        self.assertEqual(etiqueta_actualizada.color, "Amarillo")

    def test_eliminar_etiqueta(self):
        """Prueba la eliminación correcta de una etiqueta."""
        etiqueta = self.manager.crear_etiqueta("Borrar", "Negro")
        eliminada = self.manager.eliminar_etiqueta(etiqueta.id_etiqueta)
        self.assertIsNone(self.manager.obtener_etiqueta_por_id(eliminada.id_etiqueta))

    def test_actualizar_etiqueta_inexistente(self):
        """Prueba la actualización de una etiqueta que no existe."""
        etiqueta = self.manager.actualizar_etiqueta(9999, nombre_etiqueta="No existe", color="Transparente")
        self.assertIsNone(etiqueta)

    def test_eliminar_etiqueta_inexistente(self):
        """Prueba la eliminación de una etiqueta que no existe."""
        etiqueta = self.manager.eliminar_etiqueta(9999)
        self.assertIsNone(etiqueta)

    def test_crear_etiqueta_duplicada(self):
        """Prueba que no se permita crear una etiqueta con el mismo nombre."""
        self.manager.crear_etiqueta("Duplicada", "Rosa")
        resultado = self.manager.crear_etiqueta("Duplicada", "Rosa")
        self.assertIsNone(resultado)

    def test_error_inesperado_al_crear(self):
        """Prueba que se maneje correctamente un error inesperado al crear una etiqueta."""
        with patch.object(self.session, 'add', side_effect=SQLAlchemyError("Error simulado")):
            resultado = self.manager.crear_etiqueta("Error", "Gris")
            self.assertIsNone(resultado)

    def test_error_inesperado_al_actualizar(self):
        """Prueba que se maneje correctamente un error inesperado al actualizar una etiqueta."""
        etiqueta = self.manager.crear_etiqueta("Actualizar", "Cyan")
        with patch.object(self.session, 'commit', side_effect=SQLAlchemyError("Fallo commit")):
            resultado = self.manager.actualizar_etiqueta(etiqueta.id_etiqueta, "Nuevo", "Negro")
            self.assertIsNone(resultado)

    def test_error_inesperado_al_eliminar(self):
        """Prueba que se maneje correctamente un error inesperado al eliminar una etiqueta."""
        etiqueta = self.manager.crear_etiqueta("Eliminar", "Blanco")
        with patch.object(self.session, 'commit', side_effect=SQLAlchemyError("Fallo al eliminar")):
            resultado = self.manager.eliminar_etiqueta(etiqueta.id_etiqueta)
            self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()
