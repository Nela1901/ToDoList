"""
Pruebas unitarias para la clase RecordatorioManager del sistema ToDoList.

Este módulo verifica la correcta creación, obtención, actualización y eliminación
de recordatorios asociados a tareas.
"""

import unittest
from datetime import datetime, timedelta
from src.logica.recordatorio_manager import RecordatorioManager
from src.modelo.database import Session, Base, engine
from src.logica.usuario_manager import UsuarioManager
from src.logica.estado_manager import EstadoManager
from src.logica.tarea_manager import TareaManager

class TestRecordatorioManager(unittest.TestCase):
    """
    Conjunto de pruebas unitarias para la clase RecordatorioManager.

    Métodos:
        setUp: Inicializa la base de datos, sesión y crea datos relacionados.
        tearDown: Revierte y cierra la sesión tras cada prueba.
        test_crear_recordatorio: Verifica la creación correcta de un recordatorio.
        test_obtener_recordatorio: Verifica la obtención correcta de un recordatorio por ID.
        test_actualizar_recordatorio: Verifica la actualización correcta de un recordatorio.
        test_eliminar_recordatorio: Verifica la eliminación correcta de un recordatorio.
    """

    def setUp(self):
        """
        Configura la base de datos limpia y prepara la sesión y los managers,
        creando un usuario, estado y tarea para asociar los recordatorios.
        """
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.recordatorio_manager = RecordatorioManager(self.session)

        # Crear datos relacionados necesarios
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
        """
        Revierte cualquier cambio y cierra la sesión después de cada prueba.
        """
        self.session.rollback()
        self.session.close()

    def test_crear_recordatorio(self):
        """
        Prueba que se cree un recordatorio con los datos correctos.
        """
        recordatorio = self.recordatorio_manager.crear_recordatorio(
            self.tarea.id_tarea,
            datetime.now() + timedelta(hours=2),
            "Notificación"
        )
        self.assertIsNotNone(recordatorio.id_recordatorio)
        self.assertEqual(recordatorio.id_tarea, self.tarea.id_tarea)
        self.assertEqual(recordatorio.tipo, "Notificación")

    def test_obtener_recordatorio(self):
        """
        Prueba la obtención correcta de un recordatorio por su ID.
        """
        recordatorio = self.recordatorio_manager.crear_recordatorio(
            self.tarea.id_tarea,
            datetime.now() + timedelta(hours=2),
            "Alarma"
        )
        recordatorio_leido = self.recordatorio_manager.obtener_recordatorio_por_id(recordatorio.id_recordatorio)
        self.assertEqual(recordatorio_leido.tipo, "Alarma")

    def test_actualizar_recordatorio(self):
        """
        Prueba la actualización del tipo de un recordatorio existente.
        """
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
        """
        Prueba la eliminación correcta de un recordatorio.
        """
        recordatorio = self.recordatorio_manager.crear_recordatorio(
            self.tarea.id_tarea,
            datetime.now() + timedelta(hours=2),
            "Para eliminar"
        )
        eliminado = self.recordatorio_manager.eliminar_recordatorio(recordatorio.id_recordatorio)
        self.assertIsNone(self.recordatorio_manager.obtener_recordatorio_por_id(eliminado.id_recordatorio))

if __name__ == "__main__":
    unittest.main()
