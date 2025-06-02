# tests/test_etiqueta_manager.py

import unittest
from src.logica.etiqueta_manager import EtiquetaManager
from src.modelo.database import Session, Base, engine

class TestEtiquetaManager(unittest.TestCase):
    def setUp(self):
        # Crear las tablas desde cero antes de cada prueba
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.manager = EtiquetaManager(self.session)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_crear_etiqueta(self):
        etiqueta = self.manager.crear_etiqueta("Trabajo", "Rojo")
        self.assertIsNotNone(etiqueta.id_etiqueta)
        self.assertEqual(etiqueta.nombre_etiqueta, "Trabajo")
        self.assertEqual(etiqueta.color, "Rojo")

    def test_obtener_etiqueta(self):
        etiqueta = self.manager.crear_etiqueta("Casa", "Azul")
        etiqueta_leida = self.manager.obtener_etiqueta_por_id(etiqueta.id_etiqueta)
        self.assertEqual(etiqueta_leida.nombre_etiqueta, "Casa")
        self.assertEqual(etiqueta_leida.color, "Azul")

    def test_actualizar_etiqueta(self):
        etiqueta = self.manager.crear_etiqueta("Personal", "Verde")
        etiqueta_actualizada = self.manager.actualizar_etiqueta(
            etiqueta.id_etiqueta, nombre_etiqueta="Ocio", color="Amarillo"
        )
        self.assertEqual(etiqueta_actualizada.nombre_etiqueta, "Ocio")
        self.assertEqual(etiqueta_actualizada.color, "Amarillo")

    def test_eliminar_etiqueta(self):
        etiqueta = self.manager.crear_etiqueta("Borrar", "Negro")
        eliminada = self.manager.eliminar_etiqueta(etiqueta.id_etiqueta)
        self.assertIsNone(self.manager.obtener_etiqueta_por_id(eliminada.id_etiqueta))

if __name__ == "__main__":
    unittest.main()
