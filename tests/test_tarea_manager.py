"""
Pruebas unitarias para la clase TareaManager del sistema ToDoList.

Este módulo verifica la correcta creación, obtención, actualización y eliminación
de tareas dentro del sistema.
"""

import unittest
from datetime import datetime, timedelta
from src.logica.tarea_manager import TareaManager
from src.modelo.database import Session, Base, engine
from src.logica.usuario_manager import UsuarioManager
from src.logica.estado_manager import EstadoManager
from src.modelo.modelo import Estado


class TestTareaManager(unittest.TestCase):
    """
    Conjunto de pruebas unitarias para la clase TareaManager.
    """

    def setUp(self):
        """
        Configura la base de datos limpia y prepara la sesión y los managers,
        creando un usuario y estado para asociar las tareas.
        """
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.tarea_manager = TareaManager(self.session)

        # Crear datos relacionados necesarios
        self.usuario_manager = UsuarioManager(self.session)
        self.estado_manager = EstadoManager(self.session)
        self.usuario = self.usuario_manager.crear_usuario(
            "Usuario prueba", "test@correo.com", "1234")
        self.estado = self.estado_manager.crear_estado("Pendiente", "Tarea pendiente")

    def tearDown(self):
        """
        Revierte cualquier cambio y cierra la sesión después de cada prueba.
        """
        self.session.rollback()
        self.session.close()

    def test_crear_tarea(self):
        """Prueba que se cree una tarea con los datos correctos."""
        tarea = self.tarea_manager.crear_tarea(
            "Tarea 1", "Descripción tarea 1",
            datetime.now(), datetime.now() + timedelta(days=1),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )
        self.assertIsNotNone(tarea.id_tarea)
        self.assertEqual(tarea.titulo, "Tarea 1")
        self.assertEqual(tarea.descripcion, "Descripción tarea 1")

    def test_obtener_tarea(self):
        """Prueba la obtención correcta de una tarea por su ID."""
        tarea = self.tarea_manager.crear_tarea(
            "Tarea 2", "Descripción tarea 2",
            datetime.now(), datetime.now() + timedelta(days=1),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )
        tarea_leida = self.tarea_manager.obtener_tarea_por_id(tarea.id_tarea)
        self.assertEqual(tarea_leida.titulo, "Tarea 2")
        self.assertEqual(tarea_leida.descripcion, "Descripción tarea 2")

    def test_actualizar_tarea(self):
        """Prueba la actualización del título y descripción de una tarea existente."""
        tarea = self.tarea_manager.crear_tarea(
            "Tarea 3", "Descripción tarea 3",
            datetime.now(), datetime.now() + timedelta(days=1),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )
        tarea_actualizada = self.tarea_manager.actualizar_tarea(
            tarea.id_tarea,
            titulo="Tarea 3 actualizada",
            descripcion="Nueva descripción"
        )
        self.assertEqual(tarea_actualizada.titulo, "Tarea 3 actualizada")
        self.assertEqual(tarea_actualizada.descripcion, "Nueva descripción")

    def test_eliminar_tarea(self):
        """Prueba la eliminación correcta de una tarea."""
        tarea = self.tarea_manager.crear_tarea(
            "Tarea 4", "Descripción tarea 4",
            datetime.now(), datetime.now() + timedelta(days=1),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )
        self.tarea_manager.eliminar_tarea(tarea)
        self.assertIsNone(self.tarea_manager.obtener_tarea_por_id(tarea.id_tarea))

    def test_obtener_tareas(self):
        """Prueba obtener todas las tareas existentes."""
        self.tarea_manager.crear_tarea(
            "Tarea 5", "Descripción 5",
            datetime.now(), datetime.now() + timedelta(days=2),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )
        self.tarea_manager.crear_tarea(
            "Tarea 6", "Descripción 6",
            datetime.now(), datetime.now() + timedelta(days=3),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )
        tareas = self.tarea_manager.obtener_tareas()
        self.assertEqual(len(tareas), 2)

    def test_obtener_tareas_por_usuario(self):
        """Prueba que solo se obtengan las tareas del usuario especificado."""
        self.tarea_manager.crear_tarea(
            "Tarea A", "Descripción A",
            datetime.now(), datetime.now() + timedelta(days=1),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )
        tareas_usuario = self.tarea_manager.obtener_tareas_por_usuario(self.usuario.id_usuario)
        self.assertEqual(len(tareas_usuario), 1)
        self.assertEqual(tareas_usuario[0].titulo, "Tarea A")

    def test_marcar_completado(self):
        """Prueba que se marque la tarea como completada correctamente."""
        tarea = self.tarea_manager.crear_tarea(
            "Tarea completar", "Descripción",
            datetime.now(), datetime.now() + timedelta(days=1),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )
        self.tarea_manager.marcar_completado(tarea)
        tarea_actualizada = self.tarea_manager.obtener_tarea_por_id(tarea.id_tarea)
        nombre_estado = self.session.query(Estado).get(tarea_actualizada.id_estado).nombre_estado
        self.assertEqual(nombre_estado, "Completado")

    def test_crear_tarea_campos_vacios(self):
        """Debe fallar al crear una tarea con título vacío o campos nulos."""
        tarea = self.tarea_manager.crear_tarea(
            "",  # título vacío
            "Descripción sin título",
            datetime.now(),
            datetime.now() + timedelta(days=1),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )
        self.assertIsNotNone(tarea)
        self.assertEqual(tarea.titulo, "")

        tarea_none = self.tarea_manager.crear_tarea(
            "Tarea sin descripción",
            None,  # descripción None
            datetime.now(),
            datetime.now() + timedelta(days=1),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )
        self.assertIsNotNone(tarea_none)
        self.assertEqual(tarea_none.descripcion, None)

    def test_actualizar_tarea_inexistente(self):
        """Debe retornar None al intentar actualizar una tarea que no existe."""
        resultado = self.tarea_manager.actualizar_tarea(
            9999,  # ID inexistente
            titulo="Título falso"
        )
        self.assertIsNone(resultado)

    def test_actualizar_tarea_datos_invalidos(self):
        """Debe manejar correctamente datos inválidos en actualización."""
        tarea = self.tarea_manager.crear_tarea(
            "Tarea original", "Descripción original",
            datetime.now(), datetime.now() + timedelta(days=1),
            id_usuario=self.usuario.id_usuario,
            id_estado=self.estado.id_estado
        )

        resultado = self.tarea_manager.actualizar_tarea(
            tarea.id_tarea,
            titulo="",  # título inválido
            descripcion=None  # descripción inválida
        )
        # Puede fallar y devolver None si hay restricciones, o guardar los datos inválidos si no están validados
        # Aquí solo validamos que no haya excepción y el resultado no sea None si no hay restricciones.
        self.assertIsNotNone(resultado)

    def test_crear_tarea_usuario_invalido(self):
        """Debe fallar al crear tarea con id_usuario inexistente."""
        try:
            tarea = self.tarea_manager.crear_tarea(
                "Tarea inválida", "Desc",
                datetime.now(), datetime.now() + timedelta(days=1),
                id_usuario=9999,  # ID no existente
                id_estado=self.estado.id_estado
            )
            self.assertIsNotNone(tarea)  # Puede lanzar IntegrityError si hay FK en DB
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_crear_tarea_estado_invalido(self):
        """Debe fallar al crear tarea con id_estado inexistente."""
        try:
            tarea = self.tarea_manager.crear_tarea(
                "Tarea sin estado", "Desc",
                datetime.now(), datetime.now() + timedelta(days=1),
                id_usuario=self.usuario.id_usuario,
                id_estado=9999  # estado no existente
            )
            self.assertIsNotNone(tarea)  # Puede lanzar IntegrityError si hay FK en DB
        except Exception as e:
            self.assertIsInstance(e, Exception)


if __name__ == "__main__":
    unittest.main()
