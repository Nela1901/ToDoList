# tests/test_tarea_manager.py

import unittest
from datetime import datetime, timedelta
from src.logica.tarea_manager import TareaManager
from src.modelo.database import Session, Base, engine
from src.logica.usuario_manager import UsuarioManager
from src.logica.estado_manager import EstadoManager

class TestTareaManager(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.tarea_manager = TareaManager(self.session)

        # Crear datos relacionados
        self.usuario_manager = UsuarioManager(self.session)
        self.estado_manager = EstadoManager(self.session)
        self.usuario = self.usuario_manager.crear_usuario("Usuario prueba", "test@correo.com", "1234")
        self.estado = self.estado_manager.crear_estado("Pendiente", "Tarea pendiente")

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_crear_tarea(self):
        tarea = self.tarea_manager.crear_tarea(
            "Tarea 1", "Descripción tarea 1",
            datetime.now(), datetime.now() + timedelta(days=1),
            self.usuario.id_usuario, self.estado.id_estado
        )
        self.assertIsNotNone(tarea.id_tarea)
        self.assertEqual(tarea.titulo, "Tarea 1")
        self.assertEqual(tarea.descripcion, "Descripción tarea 1")

    def test_obtener_tarea(self):
        tarea = self.tarea_manager.crear_tarea(
            "Tarea 2", "Descripción tarea 2",
            datetime.now(), datetime.now() + timedelta(days=1),
            self.usuario.id_usuario, self.estado.id_estado
        )
        tarea_leida = self.tarea_manager.obtener_tarea_por_id(tarea.id_tarea)
        self.assertEqual(tarea_leida.titulo, "Tarea 2")
        self.assertEqual(tarea_leida.descripcion, "Descripción tarea 2")

    def test_actualizar_tarea(self):
        tarea = self.tarea_manager.crear_tarea(
            "Tarea 3", "Descripción tarea 3",
            datetime.now(), datetime.now() + timedelta(days=1),
            self.usuario.id_usuario, self.estado.id_estado
        )
        tarea_actualizada = self.tarea_manager.actualizar_tarea(
            tarea.id_tarea,
            titulo="Tarea 3 actualizada",
            descripcion="Nueva descripción"
        )
        self.assertEqual(tarea_actualizada.titulo, "Tarea 3 actualizada")
        self.assertEqual(tarea_actualizada.descripcion, "Nueva descripción")

    def test_eliminar_tarea(self):
        tarea = self.tarea_manager.crear_tarea(
            "Tarea 4", "Descripción tarea 4",
            datetime.now(), datetime.now() + timedelta(days=1),
            self.usuario.id_usuario, self.estado.id_estado
        )
        eliminada = self.tarea_manager.eliminar_tarea(tarea.id_tarea)
        self.assertIsNone(self.tarea_manager.obtener_tarea_por_id(eliminada.id_tarea))

if __name__ == "__main__":
    unittest.main()
