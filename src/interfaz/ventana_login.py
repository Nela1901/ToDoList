import sys
import os
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QVBoxLayout
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

from src.modelo.database import Session
from src.logica.usuario_manager import UsuarioManager
from src.interfaz.estilos import mostrar_mensaje  # ← Sigue igual

class VentanaLogin(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión - ToDoList")
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #EAF6F6;")

        self.session = Session()
        self.usuario_manager = UsuarioManager(self.session)

        self.usuario = None  # Atributo para guardar usuario si el login tiene éxito

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # LOGO
        ruta_logo = os.path.join(os.path.dirname(__file__), "img", "logo.png")
        logo = QLabel()
        pixmap = QPixmap(ruta_logo)
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaledToWidth(100, Qt.SmoothTransformation))
            logo.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo)

        # TÍTULO
        self.label_titulo = QLabel("¡Bienvenido a ToDoList!")
        self.label_titulo.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.label_titulo.setStyleSheet("color: #060606; padding: 10px;")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_titulo)

        # USUARIO
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Nombre de usuario")
        self.input_usuario.setStyleSheet("""
            background-color: #ffffff;
            padding: 8px;
            border-radius: 8px;
            font-size: 14px;
            border: 1px solid #bccd7b;
        """)
        layout.addWidget(self.input_usuario)

        # CONTRASEÑA
        self.input_contrasena = QLineEdit()
        self.input_contrasena.setPlaceholderText("Contraseña")
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        self.input_contrasena.setStyleSheet("""
            background-color: #ffffff;
            padding: 8px;
            border-radius: 8px;
            font-size: 14px;
            border: 1px solid #bccd7b;
        """)
        layout.addWidget(self.input_contrasena)

        # BOTÓN
        self.boton_login = QPushButton("Iniciar sesión")
        self.boton_login.setStyleSheet("""
            background-color: #00c2cb;
            color: #ffffff;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
        """)
        self.boton_login.clicked.connect(self.iniciar_sesion)
        layout.addWidget(self.boton_login)

        layout.setSpacing(12)
        layout.setContentsMargins(40, 20, 40, 20)
        self.setLayout(layout)

    def iniciar_sesion(self):
        nombre_usuario = self.input_usuario.text().strip()
        contrasena = self.input_contrasena.text().strip()

        if not nombre_usuario or not contrasena:
            mostrar_mensaje(self, "Campos vacíos", "Por favor, completa todos los campos.", tipo="advertencia")
            return

        usuario = self.usuario_manager.obtener_por_nombre(nombre_usuario)

        if usuario and usuario.contrasena == contrasena:
            mostrar_mensaje(self, "Acceso permitido", f"¡Bienvenido {nombre_usuario}!", tipo="info")
            self.usuario = usuario
            self.accept()  # ← importante para que app.py sepa que el login fue exitoso
        else:
            mostrar_mensaje(self, "Error de inicio de sesión", "Usuario o contraseña incorrectos.", tipo="error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = VentanaLogin()
    if login.exec() == QDialog.Accepted:
        print(f"Usuario logueado: {login.usuario.nombre_usuario}")
    sys.exit(app.exec())
