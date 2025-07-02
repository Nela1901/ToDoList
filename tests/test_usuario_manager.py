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

    def test_crear_usuario_duplicado(self):
        """
        Prueba que no se puede crear un usuario con nombre o correo duplicado.
        """
        self.manager.crear_usuario("Duplicado", "correo@gmail.com", "123")
        duplicado = self.manager.crear_usuario("Duplicado", "correo@gmail.com", "otro")
        self.assertIsNone(duplicado)

    def test_obtener_usuarios_lista(self):
        """
        Prueba que se devuelva la lista correcta de usuarios.
        """
        self.assertEqual(self.manager.obtener_usuarios(), [])  # Lista vacía al inicio
        self.manager.crear_usuario("A", "a@a.com", "a")
        self.manager.crear_usuario("B", "b@b.com", "b")
        usuarios = self.manager.obtener_usuarios()
        self.assertEqual(len(usuarios), 2)

    def test_obtener_usuario_por_id_inexistente(self):
        """
        Prueba la obtención de un usuario con ID que no existe.
        """
        usuario = self.manager.obtener_usuario_por_id(999)
        self.assertIsNone(usuario)

    def test_actualizar_usuario_inexistente(self):
        """
        Prueba que no se actualiza un usuario si no existe.
        """
        resultado = self.manager.actualizar_usuario(999, nombre_usuario="nuevo")
        self.assertIsNone(resultado)

    def test_eliminar_usuario_inexistente(self):
        """
        Prueba que no se puede eliminar un usuario que no existe.
        """
        resultado = self.manager.eliminar_usuario(999)
        self.assertIsNone(resultado)

    def test_obtener_por_nombre_existente(self):
        """
        Prueba obtener un usuario por nombre existente.
        """
        self.manager.crear_usuario("Buscado", "buscado@gmail.com", "clave")
        usuario = self.manager.obtener_por_nombre("Buscado")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre_usuario, "Buscado")

    def test_obtener_por_nombre_inexistente(self):
        """
        Prueba buscar un usuario por nombre que no existe.
        """
        usuario = self.manager.obtener_por_nombre("NoExiste")
        self.assertIsNone(usuario)

    def test_actualizar_usuario_con_datos_duplicados(self):
        """
        Prueba que no se puede actualizar un usuario con un nombre o correo ya existentes.
        """
        usuario1 = self.manager.crear_usuario("Usuario1", "user1@gmail.com", "pass1")
        usuario2 = self.manager.crear_usuario("Usuario2", "user2@gmail.com", "pass2")
        resultado = self.manager.actualizar_usuario(
            usuario2.id_usuario,
            nombre_usuario="Usuario1",  # nombre ya existente
            correo_electronico="user1@gmail.com"  # correo ya existente
        )
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()
