# tests/test_recordatorio_manager.py

import unittest
from datetime import datetime, timedelta
from src.logica.recordatorio_manager import RecordatorioManager
from src.modelo.database import Session, Base, engine
from src.logica.usuario_manager import UsuarioManager
from src.logica.estado_manager import EstadoManager
from src.logica.tarea_manager import TareaManager

class TestRecordatorioManager(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.recordatorio_manager = RecordatorioManager(self.session)

        # Crear datos relacionados
        self.usuario_manager = UsuarioManager(self.session)
        self.estado_manager = EstadoManager(self.session)
        self.tarea_manager = TareaManager(self.session)

        self.usuario = self.usuario_manager.crear_usuario("Usuario recordatorio", "recordatorio@correo.com", "123")
        self.estado = self.estado_manager.crear_estado("Pendiente", "Tarea pendiente")
        self.tarea = self.tarea_manager.crear_tarea(
            "Tarea con recordatorio",
            "Descripción",
            datetime.now(),
            datetime.now() + timedelta(days=1),
            self.usuario.id_usuario,
            self.estado.id_estado
        )

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_crear_recordatorio(self):
        recordatorio = self.recordatorio_manager.crear_recordatorio(
            self.tarea.id_tarea,
            datetime.now() + timedelta(hours=2),
            "Notificación"
        )
        self.assertIsNotNone(recordatorio.id_recordatorio)
        self.assertEqual(recordatorio.id_tarea, self.tarea.id_tarea)
        self.assertEqual(recordatorio.tipo, "Notificación")

    def test_obtener_recordatorio(self):
        recordatorio = self.recordatorio_manager.crear_recordatorio(
            self.tarea.id_tarea,
            datetime.now() + timedelta(hours=2),
            "Alarma"
        )
        recordatorio_leido = self.recordatorio_manager.obtener_recordatorio_por_id(recordatorio.id_recordatorio)
        self.assertEqual(recordatorio_leido.tipo, "Alarma")

    def test_actualizar_recordatorio(self):
        recordatorio = self.recordatorio_manager.crear_recordatorio(
            self.tarea.id_tarea,
            datetime.now() + timedelta(hours=2),
            "Tipo A"
        )
        nuevo_tipo = "Tipo B"
        recordatorio_actualizado = self.recordatorio_manager.actualizar_recordatorio(
            recordatorio.id_recordatorio,
            tipo=nuevo_tipo
        )
        self.assertEqual(recordatorio_actualizado.tipo, nuevo_tipo)

    def test_eliminar_recordatorio(self):
        recordatorio = self.recordatorio_manager.crear_recordatorio(
            self.tarea.id_tarea,
            datetime.now() + timedelta(hours=2),
            "Para eliminar"
        )
        eliminado = self.recordatorio_manager.eliminar_recordatorio(recordatorio.id_recordatorio)
        self.assertIsNone(self.recordatorio_manager.obtener_recordatorio_por_id(eliminado.id_recordatorio))

if __name__ == "__main__":
    unittest.main()
