from src.interfaz.ventana_anadir_tarea import VentanaAnadirTarea
from src.interfaz.ventana_editar_tarea import VentanaEditarTarea
from src.interfaz.ventana_principal import VentanaPrincipal

# Mocks simples para simular un usuario y una tarea

class UsuarioFalso:
    def __init__(self):
        self.nombre_usuario = "UsuarioPrueba"

class TareaFalsa:
    def __init__(self):
        self.titulo = "Tarea de prueba"
        self.descripcion = "Descripción de prueba"
        self.fecha_vencimiento = None
        self.etiquetas = []

# Test: creación de ventana para añadir tarea
def test_ventana_anadir_tarea():
    usuario = UsuarioFalso()
    ventana = VentanaAnadirTarea(usuario)
    assert ventana is not None
    #es decir que se haya creado correctamente
    #una instancia de la ventana.
    #None indica error

# Test: creación de ventana para editar tarea
def test_ventana_editar_tarea():
    tarea = TareaFalsa()
    usuario = UsuarioFalso()
    ventana = VentanaEditarTarea(tarea, usuario)
    assert ventana is not None

# Test: creación de ventana principal
def test_ventana_principal():
    usuario = UsuarioFalso()
    ventana = VentanaPrincipal(usuario)
    assert ventana is not None
