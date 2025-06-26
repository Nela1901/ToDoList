"""Ventana de la aplicación que permite registrar un nuevo usuario."""
# pylint: disable=no-name-in-module, too-few-public-methods, missing-function-docstring
# pylint: disable=duplicate-code
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from src.modelo.database import Session
from src.logica.usuario_manager import UsuarioManager
from src.interfaz.estilos import mostrar_mensaje


class VentanaCrearCuenta(QDialog):
    """Ventana para crear una nueva cuenta de usuario."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crear Cuenta")
        self.setMinimumSize(400, 300)

        self.session = Session()
        self.usuario_manager = UsuarioManager(self.session)

        self._configurar_ui()

    def _configurar_ui(self):
        """Configura los elementos visuales de la ventana."""
        layout = QVBoxLayout()
        layout.setSpacing(12)

        titulo = QLabel("Crear nuevo usuario")
        titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #060606; padding: 10px;")
        layout.addWidget(titulo)

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre de usuario")
        self.input_nombre.setStyleSheet(self._estilo_input())
        layout.addWidget(self.input_nombre)

        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("Correo electrónico")
        self.input_correo.setStyleSheet(self._estilo_input())
        layout.addWidget(self.input_correo)

        self.input_contrasena = QLineEdit()
        self.input_contrasena.setPlaceholderText("Contraseña")
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        self.input_contrasena.setStyleSheet(self._estilo_input())
        layout.addWidget(self.input_contrasena)

        boton_crear = QPushButton("Registrar cuenta")
        boton_crear.setStyleSheet(self._estilo_boton())
        boton_crear.clicked.connect(self.crear_cuenta)
        layout.addWidget(boton_crear)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #f0fdfa;")

    def _estilo_input(self):
        """Devuelve el estilo CSS para los campos de texto."""
        return (
            "QLineEdit {"
            "font-family: 'Segoe UI';"
            "font-size: 14px;"
            "padding: 8px;"
            "border: 1px solid #bccd7b;"
            "border-radius: 8px;"
            "background-color: #ffffff;"
            "}"
        )

    def _estilo_boton(self):
        """Devuelve el estilo CSS para el botón de registro."""
        return (
            "QPushButton {"
            "font-family: 'Segoe UI';"
            "background-color: #00c2cb;"
            "color: white;"
            "padding: 10px;"
            "font-size: 14px;"
            "font-weight: bold;"
            "border: none;"
            "border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #76a9ed;"
            "}"
        )

    def crear_cuenta(self):
        """Crea una nueva cuenta con los datos ingresados en el formulario."""
        nombre = self.input_nombre.text().strip()
        correo = self.input_correo.text().strip()
        contrasena = self.input_contrasena.text().strip()

        if not nombre or not correo or not contrasena:
            mostrar_mensaje(
                self,
                "Campos vacíos",
                "Todos los campos son obligatorios.",
                tipo="advertencia"
            )
            return

        nuevo_usuario = self.usuario_manager.crear_usuario(nombre, correo, contrasena)

        if nuevo_usuario:
            mostrar_mensaje(
                self,
                "Éxito",
                "Cuenta creada correctamente.",
                tipo="info"
            )
            self.accept()
        else:
            mostrar_mensaje(
                self,
                "Error",
                "No se pudo crear el usuario. Puede que ya exista.",
                tipo="error"
            )
