"""
Pruebas unitarias para la clase UsuarioManager.

Verifica las operaciones CRUD relacionadas con usuarios en la base de datos.
"""

import unittest
from src.logica.usuario_manager import UsuarioManager
from src.modelo.database import Session, Base, engine

class TestUsuarioManager(unittest.TestCase):
    """
    Pruebas unitarias para UsuarioManager.

    Métodos:
        setUp: Inicializa base de datos y sesión para pruebas.
        tearDown: Revierte cambios y cierra sesión tras cada prueba.
        test_crear_usuario: Verifica creación correcta de un usuario.
        test_obtener_usuario: Verifica obtención correcta de un usuario.
        test_actualizar_usuario: Verifica actualización de datos de usuario.
        test_eliminar_usuario: Verifica eliminación de un usuario.
    """

    def setUp(self):
        """
        Configura una base de datos limpia y crea una sesión nueva antes de cada prueba.
        """
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.manager = UsuarioManager(self.session)

    def tearDown(self):
        """
        Revierte la sesión y la cierra tras cada prueba.
        """
        self.session.rollback()
        self.session.close()

    def test_crear_usuario(self):
        """
        Prueba la creación de un usuario con datos válidos.
        """
        usuario = self.manager.crear_usuario("Juan", "juan@gmail.com", "12345")
        self.assertIsNotNone(usuario.id_usuario)
        self.assertEqual(usuario.nombre_usuario, "Juan")
        self.assertEqual(usuario.correo_electronico, "juan@gmail.com")
        self.assertEqual(usuario.contrasena, "12345")

    def test_obtener_usuario(self):
        """
        Prueba la obtención de un usuario por su ID.
        """
        usuario = self.manager.crear_usuario("Ana", "ana@gmail.com", "pass")
        usuario_leido = self.manager.obtener_usuario_por_id(usuario.id_usuario)
        self.assertEqual(usuario_leido.nombre_usuario, "Ana")
        self.assertEqual(usuario_leido.correo_electronico, "ana@gmail.com")
        self.assertEqual(usuario_leido.contrasena, "pass")

    def test_actualizar_usuario(self):
        """
        Prueba la actualización de los campos de un usuario existente.
        """
        usuario = self.manager.crear_usuario("Pedro", "pedro@gmail.com", "abc")
        usuario_actualizado = self.manager.actualizar_usuario(
            usuario.id_usuario,
            nombre_usuario="Pedro actualizado",
            correo_electronico="nuevo@gmail.com",
            contrasena="xyz"
        )
        self.assertEqual(usuario_actualizado.nombre_usuario, "Pedro actualizado")
        self.assertEqual(usuario_actualizado.correo_electronico, "nuevo@gmail.com")
        self.assertEqual(usuario_actualizado.contrasena, "xyz")

    def test_eliminar_usuario(self):
        """
        Prueba la eliminación de un usuario y la verificación posterior de que ya no existe.
        """
        usuario = self.manager.crear_usuario("Eliminarme", "borrar@gmail.com", "bye")
        eliminado = self.manager.eliminar_usuario(usuario.id_usuario)
        self.assertIsNone(self.manager.obtener_usuario_por_id(eliminado.id_usuario))

if __name__ == "__main__":
    unittest.main()
