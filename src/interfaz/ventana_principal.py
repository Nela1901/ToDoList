from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDoList")
        self.setGeometry(100, 100, 800, 600)

        # Ejemplo: etiqueta de bienvenida
        self.etiqueta = QLabel("¡Bienvenido a tu ToDoList!", self)
        self.etiqueta.move(20, 20)

if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()
