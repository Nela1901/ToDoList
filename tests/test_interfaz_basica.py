import unittest
from PySide6.QtWidgets import QApplication

from src.interfaz.ventana_anadir_tarea import VentanaAnadirTarea
from src.interfaz.ventana_cambiar_contrasena import VentanaCambiarContrasena
from src.interfaz.ventana_crear_cuenta import VentanaCrearCuenta
from src.interfaz.ventana_editar_tarea import VentanaEditarTarea
from src.interfaz.ventana_login import VentanaLogin
from src.interfaz.ventana_principal import VentanaPrincipal

app = QApplication([])  # Necesario para testear interfaces gráficas

class TestInterfazBasica(unittest.TestCase):

    def test_ventana_anadir_tarea(self):
        ventana = VentanaAnadirTarea("UsuarioPrueba")
        self.assertIsNotNone(ventana)

    def test_ventana_cambiar_contrasena(self):
        ventana = VentanaCambiarContrasena("UsuarioPrueba")
        self.assertIsNotNone(ventana)

    def test_ventana_crear_cuenta(self):
        ventana = VentanaCrearCuenta()
        self.assertIsNotNone(ventana)

    def test_ventana_editar_tarea(self):
        ventana = VentanaEditarTarea(1, "UsuarioPrueba")  # Usa un ID válido de prueba si es necesario
        self.assertIsNotNone(ventana)

    def test_ventana_login(self):
        ventana = VentanaLogin()
        self.assertIsNotNone(ventana)

    def test_ventana_principal(self):
        ventana = VentanaPrincipal("UsuarioPrueba")
        self.assertIsNotNone(ventana)

if __name__ == '__main__':
    unittest.main()
