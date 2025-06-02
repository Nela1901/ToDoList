# tests/test_estado_manager.py

import unittest
from src.logica.estado_manager import EstadoManager
from src.modelo.database import Session, Base, engine

class TestEstadoManager(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.manager = EstadoManager(self.session)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_crear_estado(self):
        estado = self.manager.crear_estado("Pendiente", "Tarea aún no comenzada")
        self.assertIsNotNone(estado.id_estado)
        self.assertEqual(estado.nombre_estado, "Pendiente")
        self.assertEqual(estado.descripcion, "Tarea aún no comenzada")

    def test_obtener_estado(self):
        estado = self.manager.crear_estado("Completado", "Tarea finalizada")
        estado_leido = self.manager.obtener_estado_por_id(estado.id_estado)
        self.assertEqual(estado_leido.nombre_estado, "Completado")
        self.assertEqual(estado_leido.descripcion, "Tarea finalizada")

    def test_actualizar_estado(self):
        estado = self.manager.crear_estado("En proceso", "Tarea en ejecución")
        estado_actualizado = self.manager.actualizar_estado(
            estado.id_estado,
            nombre_estado="En curso",
            descripcion="Actualización de descripción"
        )
        self.assertEqual(estado_actualizado.nombre_estado, "En curso")
        self.assertEqual(estado_actualizado.descripcion, "Actualización de descripción")

    def test_eliminar_estado(self):
        estado = self.manager.crear_estado("Temporal", "A eliminar")
        eliminado = self.manager.eliminar_estado(estado.id_estado)
        self.assertIsNone(self.manager.obtener_estado_por_id(eliminado.id_estado))

if __name__ == "__main__":
    unittest.main()




