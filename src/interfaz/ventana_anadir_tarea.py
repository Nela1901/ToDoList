"""Ventana de diálogo para añadir una nueva tarea con título, descripción, fecha y etiquetas."""
# pylint: disable=no-name-in-module, non-ascii-name
# pylint: disable=duplicate-code
from datetime import datetime

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDateEdit,
    QPushButton, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QDate

from src.logica.tarea_manager import TareaManager
from src.modelo.database import Session
from src.modelo.modelo import Estado, Etiqueta
from src.interfaz.estilos import mostrar_mensaje


class VentanaAnadirTarea(QDialog):
    """Ventana de diálogo para registrar una nueva tarea."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Añadir nueva tarea")
        self.setMinimumSize(400, 350)

        self.session = Session()
        self.tarea_manager = TareaManager(self.session)

        self._configurar_ui()

    def _configurar_ui(self):
        """Configura la interfaz gráfica de la ventana."""
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Título
        label_titulo = QLabel("Título:")
        label_titulo.setStyleSheet("font-weight: bold; color: #333; font-family: 'Segoe UI';")
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Título de la tarea")
        self.titulo_input.setStyleSheet(self._estilo_input())

        # Descripción
        label_descripcion = QLabel("Descripción:")
        label_descripcion.setStyleSheet("font-weight: bold; color: #333; font-family: 'Segoe UI';")
        self.descripcion_input = QLineEdit()
        self.descripcion_input.setPlaceholderText("Descripción")
        self.descripcion_input.setStyleSheet(self._estilo_input())

        # Fecha límite
        label_fecha = QLabel("Fecha límite:")
        label_fecha.setStyleSheet("font-weight: bold; color: #333; font-family: 'Segoe UI';")
        self.fecha_input = QDateEdit()
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setDate(QDate.currentDate())
        self.fecha_input.setStyleSheet(self._estilo_input())

        # Selección de etiquetas
        self.lista_etiquetas = QListWidget()
        self.lista_etiquetas.setSelectionMode(QListWidget.MultiSelection)
        self.lista_etiquetas.setStyleSheet("""
            font-family: 'Segoe UI';
            font-size: 13px;
            background-color: #ffffff;
            border: 1px solid #ccc;
            border-radius: 5px;
        """)

        # Botón guardar
        self.boton_guardar = QPushButton("Guardar tarea")
        self.boton_guardar.setStyleSheet(self._estilo_boton())
        self.boton_guardar.clicked.connect(self.guardar_tarea)

        # Agregar widgets al layout
        layout.addWidget(label_titulo)
        layout.addWidget(self.titulo_input)
        layout.addWidget(label_descripcion)
        layout.addWidget(self.descripcion_input)
        layout.addWidget(label_fecha)
        layout.addWidget(self.fecha_input)
        layout.addWidget(QLabel("Selecciona etiquetas:"))
        layout.addWidget(self.lista_etiquetas)
        layout.addWidget(self.boton_guardar)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #f0fdfa;")
        self.cargar_etiquetas()

    def _estilo_input(self):
        """Devuelve el estilo aplicado a los campos de entrada."""
        return """
            QLineEdit, QDateEdit {
                font-family: 'Segoe UI';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bccd7b;
                border-radius: 8px;
                background-color: #ffffff;
            }
        """

    def _estilo_boton(self):
        """Devuelve el estilo aplicado al botón de guardar."""
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

    def guardar_tarea(self):
        """Guarda la tarea con los datos ingresados y etiquetas seleccionadas."""
        titulo = self.titulo_input.text().strip()
        descripcion = self.descripcion_input.text().strip()
        fecha_vencimiento_qdate = self.fecha_input.date()
        fecha_vencimiento = datetime(
            fecha_vencimiento_qdate.year(),
            fecha_vencimiento_qdate.month(),
            fecha_vencimiento_qdate.day()
        )
        fecha_creacion = datetime.now()

        if not titulo:
            mostrar_mensaje(
                self,
                "Campos incompletos",
                "El título no puede estar vacío.",
                tipo="advertencia"
            )
            return

        if fecha_vencimiento < fecha_creacion:
            mostrar_mensaje(
                self,
                "Fecha inválida",
                "La fecha de vencimiento no puede ser anterior a hoy.",
                tipo="advertencia"
            )
            return

        estado_pendiente = self.session.query(Estado).filter_by(nombre_estado="Pendiente").first()
        if not estado_pendiente:
            mostrar_mensaje(
                self,
                "Error",
                "No se encontró el estado 'Pendiente'.",
                tipo="error"
            )
            return

        # Obtener ID del usuario logueado desde el parent
        id_usuario = self.parent().usuario.id_usuario

        etiquetas_seleccionadas = [
            item.data(Qt.UserRole) for item in self.lista_etiquetas.selectedItems()
        ]

        tarea = self.tarea_manager.crear_tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_creacion=fecha_creacion,
            fecha_vencimiento=fecha_vencimiento,
            id_usuario=id_usuario,
            id_estado=estado_pendiente.id_estado,
            etiquetas=etiquetas_seleccionadas
        )

        if tarea:
            mostrar_mensaje(
                self,
                "Tarea guardada",
                "La tarea se ha guardado correctamente.",
                tipo="info"
            )
            self.accept()
        else:
            mostrar_mensaje(
                self,
                "Error",
                "Ocurrió un error al guardar la tarea.",
                tipo="error"
            )

    def cargar_etiquetas(self):
        """Carga las etiquetas disponibles desde la base de datos."""
        etiquetas = self.session.query(Etiqueta).all()
        for etiqueta in etiquetas:
            item = QListWidgetItem(etiqueta.nombre_etiqueta)
            item.setData(Qt.UserRole, etiqueta)
            self.lista_etiquetas.addItem(item)
