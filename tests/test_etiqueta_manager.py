"""
Pruebas unitarias para la clase EtiquetaManager del sistema ToDoList.

Este módulo verifica la correcta creación, obtención, actualización y eliminación
de etiquetas, así como la recuperación de las etiquetas iniciales.
"""

import unittest
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
        test_crear_etiqueta: Verifica la creación correcta de una etiqueta.
        test_obtener_etiqueta: Verifica la obtención correcta de una etiqueta por ID.
        test_obtener_etiquetas_iniciales: Verifica que las etiquetas iniciales estén presentes.
        test_actualizar_etiqueta: Verifica la actualización correcta de una etiqueta.
        test_eliminar_etiqueta: Verifica la eliminación correcta de una etiqueta.
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
        """
        Prueba que se cree una etiqueta con nombre y color correctos.
        """
        etiqueta = self.manager.crear_etiqueta("Trabajo", "Rojo")
        self.assertIsNotNone(etiqueta.id_etiqueta)
        self.assertEqual(etiqueta.nombre_etiqueta, "Trabajo")
        self.assertEqual(etiqueta.color, "Rojo")

    def test_obtener_etiqueta(self):
        """
        Prueba la obtención correcta de una etiqueta por su ID.
        """
        etiqueta = self.manager.crear_etiqueta("Casa", "Azul")
        etiqueta_leida = self.manager.obtener_etiqueta_por_id(etiqueta.id_etiqueta)
        self.assertEqual(etiqueta_leida.nombre_etiqueta, "Casa")
        self.assertEqual(etiqueta_leida.color, "Azul")

    def test_obtener_etiquetas_iniciales(self):
        """
        Verifica que todas las etiquetas iniciales están presentes en la base de datos.
        """
        etiquetas = self.manager.obtener_etiquetas()
        nombres = [e.nombre_etiqueta for e in etiquetas]
        for etiq in ETIQUETAS_INICIALES:
            self.assertIn(etiq["nombre_etiqueta"], nombres)

    def test_actualizar_etiqueta(self):
        """
        Prueba la actualización del nombre y color de una etiqueta existente.
        """
        etiqueta = self.manager.crear_etiqueta("Personal", "Verde")
        etiqueta_actualizada = self.manager.actualizar_etiqueta(
            etiqueta.id_etiqueta, nombre_etiqueta="Ocio", color="Amarillo"
        )
        self.assertEqual(etiqueta_actualizada.nombre_etiqueta, "Ocio")
        self.assertEqual(etiqueta_actualizada.color, "Amarillo")

    def test_eliminar_etiqueta(self):
        """
        Prueba la eliminación correcta de una etiqueta.
        """
        etiqueta = self.manager.crear_etiqueta("Borrar", "Negro")
        eliminada = self.manager.eliminar_etiqueta(etiqueta.id_etiqueta)
        self.assertIsNone(self.manager.obtener_etiqueta_por_id(eliminada.id_etiqueta))

if __name__ == "__main__":
    unittest.main()
