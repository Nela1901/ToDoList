"""
Pruebas unitarias para la clase EstadoManager del sistema ToDoList.

Este módulo verifica la correcta creación, obtención, actualización y eliminación
de estados, validando tanto casos válidos como inválidos.
"""

import unittest
from src.logica.estado_manager import EstadoManager
from src.modelo.database import Session, Base, engine

class TestEstadoManager(unittest.TestCase):
    """
    Conjunto de pruebas unitarias para la clase EstadoManager.

    Métodos:
        setUp: Configura la base de datos limpia y prepara la sesión y manager.
        tearDown: Revierte y cierra la sesión tras cada prueba.
        test_crear_estado_valido: Verifica creación exitosa con datos válidos.
        test_crear_estado_invalido: Verifica que no se cree un estado inválido.
        test_obtener_estado: Verifica la obtención correcta de un estado por ID.
        test_actualizar_estado_valido: Verifica la actualización exitosa de un estado.
        test_actualizar_estado_invalido: Verifica que no se permita actualizar con estado inválido.
        test_eliminar_estado: Verifica la eliminación correcta de un estado.
    """

    def setUp(self):
        """
        Configura la base de datos y prepara una sesión y un EstadoManager limpios
        para cada prueba.
        """
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.manager = EstadoManager(self.session)

    def tearDown(self):
        """
        Revierte cualquier cambio y cierra la sesión después de cada prueba.
        """
        self.session.rollback()
        self.session.close()

    def test_crear_estado_valido(self):
        """
        Prueba que se pueda crear un estado válido correctamente.
        """
        estado = self.manager.crear_estado("Pendiente", "Tarea aún no comenzada")
        self.assertIsNotNone(estado)
        self.assertIsNotNone(estado.id_estado)
        self.assertEqual(estado.nombre_estado, "Pendiente")
        self.assertEqual(estado.descripcion, "Tarea aún no comenzada")

    def test_crear_estado_invalido(self):
        """
        Prueba que no se cree un estado con un nombre inválido.
        """
        estado = self.manager.crear_estado("En proceso", "Estado no permitido")
        self.assertIsNone(estado)

    def test_obtener_estado(self):
        """
        Prueba la obtención correcta de un estado por su ID.
        """
        estado = self.manager.crear_estado("Completado", "Tarea finalizada")
        estado_leido = self.manager.obtener_estado_por_id(estado.id_estado)
        self.assertIsNotNone(estado_leido)
        self.assertEqual(estado_leido.nombre_estado, "Completado")
        self.assertEqual(estado_leido.descripcion, "Tarea finalizada")

    def test_actualizar_estado_valido(self):
        """
        Prueba la actualización exitosa de un estado con datos válidos.
        """
        estado = self.manager.crear_estado("Pendiente", "Tarea en espera")
        estado_actualizado = self.manager.actualizar_estado(
            estado.id_estado,
            nombre_estado="Completado",
            descripcion="Tarea ya terminada"
        )
        self.assertIsNotNone(estado_actualizado)
        self.assertEqual(estado_actualizado.nombre_estado, "Completado")
        self.assertEqual(estado_actualizado.descripcion, "Tarea ya terminada")

    def test_actualizar_estado_invalido(self):
        """
        Prueba que no se permita actualizar un estado con un nombre inválido.
        """
        estado = self.manager.crear_estado("Pendiente", "Tarea en espera")
        estado_actualizado = self.manager.actualizar_estado(
            estado.id_estado,
            nombre_estado="En curso",  # Estado inválido
            descripcion="Intento actualización inválida"
        )
        self.assertIsNone(estado_actualizado)

    def test_eliminar_estado(self):
        """
        Prueba la eliminación correcta de un estado existente.
        """
        estado = self.manager.crear_estado("Pendiente", "Temporal")
        eliminado = self.manager.eliminar_estado(estado.id_estado)
        self.assertIsNotNone(eliminado)
        self.assertIsNone(self.manager.obtener_estado_por_id(eliminado.id_estado))

if __name__ == "__main__":
    unittest.main()
