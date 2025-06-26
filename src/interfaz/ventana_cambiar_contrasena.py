from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from src.modelo.database import Session
from src.modelo.modelo import Usuario
from src.interfaz.estilos import mostrar_mensaje


class VentanaCambiarContrasena(QDialog):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cambiar Contraseña")
        self.setMinimumSize(400, 300)
        self.usuario = usuario
        self.session = Session()

        self._configurar_ui()

    def _configurar_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        titulo = QLabel("Actualizar contraseña")
        titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #060606; padding: 10px;")
        layout.addWidget(titulo)

        # Contraseña actual
        self.input_actual = QLineEdit()
        self.input_actual.setPlaceholderText("Contraseña actual")
        self.input_actual.setEchoMode(QLineEdit.Password)
        self.input_actual.setStyleSheet(self._estilo_input())
        layout.addWidget(self.input_actual)

        # Nueva contraseña
        self.input_nueva = QLineEdit()
        self.input_nueva.setPlaceholderText("Nueva contraseña")
        self.input_nueva.setEchoMode(QLineEdit.Password)
        self.input_nueva.setStyleSheet(self._estilo_input())
        layout.addWidget(self.input_nueva)

        # Confirmar nueva
        self.input_confirmar = QLineEdit()
        self.input_confirmar.setPlaceholderText("Confirmar nueva contraseña")
        self.input_confirmar.setEchoMode(QLineEdit.Password)
        self.input_confirmar.setStyleSheet(self._estilo_input())
        layout.addWidget(self.input_confirmar)

        # Botón actualizar
        boton_actualizar = QPushButton("Actualizar contraseña")
        boton_actualizar.setStyleSheet(self._estilo_boton())
        boton_actualizar.clicked.connect(self.actualizar_contrasena)
        layout.addWidget(boton_actualizar)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #f0fdfa;")

    def _estilo_input(self):
        return """
            QLineEdit {
                font-family: 'Segoe UI';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bccd7b;
                border-radius: 8px;
                background-color: #ffffff;
            }
        """

    def _estilo_boton(self):
        return """
            QPushButton {
                font-family: 'Segoe UI';
                background-color: #00c2cb;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #76a9ed;
            }
        """

    def actualizar_contrasena(self):
        actual = self.input_actual.text()
        nueva = self.input_nueva.text()
        confirmar = self.input_confirmar.text()

        if actual != self.usuario.contrasena:
            mostrar_mensaje(self, "Error", "La contraseña actual no es correcta.", tipo="error")
            return
        if not nueva or not confirmar:
            mostrar_mensaje(self, "Campos vacíos", "Todos los campos son obligatorios.", tipo="advertencia")
            return
        if nueva != confirmar:
            mostrar_mensaje(self, "Error", "Las nuevas contraseñas no coinciden.", tipo="error")
            return

        usuario_bd = self.session.query(Usuario).get(self.usuario.id_usuario)
        usuario_bd.contrasena = nueva
        self.session.commit()

        mostrar_mensaje(self, "Éxito", "Contraseña actualizada correctamente.", tipo="info")
        self.accept()
