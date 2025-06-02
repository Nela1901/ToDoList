# tests/test_usuario_manager.py

import unittest
from src.logica.usuario_manager import UsuarioManager
from src.modelo.database import Session, Base, engine

class TestUsuarioManager(unittest.TestCase):
    def setUp(self):
        # Crear las tablas desde cero antes de cada prueba
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        # Nueva sesión
        self.session = Session()
        self.manager = UsuarioManager(self.session)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_crear_usuario(self):
        usuario = self.manager.crear_usuario("Juan", "juan@gmail.com", "12345")
        self.assertIsNotNone(usuario.id_usuario)
        self.assertEqual(usuario.nombre_usuario, "Juan")
        self.assertEqual(usuario.correo_electronico, "juan@gmail.com")
        self.assertEqual(usuario.contrasena, "12345")

    def test_obtener_usuario(self):
        usuario = self.manager.crear_usuario("Ana", "ana@gmail.com", "pass")
        usuario_leido = self.manager.obtener_usuario_por_id(usuario.id_usuario)
        self.assertEqual(usuario_leido.nombre_usuario, "Ana")
        self.assertEqual(usuario_leido.correo_electronico, "ana@gmail.com")
        self.assertEqual(usuario_leido.contrasena, "pass")

    def test_actualizar_usuario(self):
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
        usuario = self.manager.crear_usuario("Eliminarme", "borrar@gmail.com", "bye")
        eliminado = self.manager.eliminar_usuario(usuario.id_usuario)
        self.assertIsNone(self.manager.obtener_usuario_por_id(eliminado.id_usuario))

if __name__ == "__main__":
    unittest.main()

