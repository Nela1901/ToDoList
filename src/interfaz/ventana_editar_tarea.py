# src/interfaz/ventana_editar_tarea.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton
)

from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from src.modelo.modelo import Etiqueta  # asegúrate de tenerlo para consultar las etiquetas

from PySide6.QtCore import QDate
from datetime import datetime
from src.logica.tarea_manager import TareaManager
from src.modelo.database import Session
from src.interfaz.estilos import mostrar_mensaje

class VentanaEditarTarea(QDialog):
    def __init__(self, tarea, session, parent=None):  # añadimos session como parámetro
        super().__init__(parent)
        self.setWindowTitle("Editar tarea")
        self.setMinimumSize(400, 350)

        self.session = session  # usar la sesión que viene del padre
        self.tarea_manager = TareaManager(self.session)
        self.tarea = tarea

        self._configurar_ui()

    def _configurar_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Título
        label_titulo = QLabel("Título:")
        label_titulo.setStyleSheet("font-weight: bold; color: #333; font-family: 'Segoe UI';")
        self.titulo_input = QLineEdit(self.tarea.titulo)
        self.titulo_input.setStyleSheet(self._estilo_input())

        # Descripción
        label_descripcion = QLabel("Descripción:")
        label_descripcion.setStyleSheet("font-weight: bold; color: #333; font-family: 'Segoe UI';")
        self.descripcion_input = QLineEdit(self.tarea.descripcion)
        self.descripcion_input.setStyleSheet(self._estilo_input())

        # Fecha límite
        label_fecha = QLabel("Fecha límite:")
        label_fecha.setStyleSheet("font-weight: bold; color: #333; font-family: 'Segoe UI';")
        self.fecha_input = QDateEdit()
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setDate(QDate(self.tarea.fecha_vencimiento.year, self.tarea.fecha_vencimiento.month, self.tarea.fecha_vencimiento.day))
        self.fecha_input.setStyleSheet(self._estilo_input())

        # Lista de etiquetas
        label_etiquetas = QLabel("Etiquetas:")
        label_etiquetas.setStyleSheet("font-weight: bold; color: #333; font-family: 'Segoe UI';")
        self.etiquetas_lista = QListWidget()
        self.etiquetas_lista.setSelectionMode(QListWidget.MultiSelection)
        self.etiquetas_lista.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #bccd7b;
                border-radius: 8px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QListWidget::item:selected {
                background-color: #00c2cb;
                color: white;
                font-weight: bold;
            }
        """)

        # Obtener etiquetas disponibles
        todas_las_etiquetas = self.session.query(Etiqueta).all()
        etiquetas_asignadas = {et.id_etiqueta for et in self.tarea.etiquetas}

        for etiqueta in todas_las_etiquetas:
            item = QListWidgetItem(etiqueta.nombre_etiqueta)
            item.setData(Qt.UserRole, etiqueta)
            if etiqueta.id_etiqueta in etiquetas_asignadas:
                item.setSelected(True)
            self.etiquetas_lista.addItem(item)

        layout.addWidget(label_etiquetas)
        layout.addWidget(self.etiquetas_lista)

        # Botón guardar cambios
        self.boton_guardar = QPushButton("Guardar cambios")
        self.boton_guardar.setStyleSheet(self._estilo_boton())
        self.boton_guardar.clicked.connect(self.guardar_cambios)

        layout.addWidget(label_titulo)
        layout.addWidget(self.titulo_input)
        layout.addWidget(label_descripcion)
        layout.addWidget(self.descripcion_input)
        layout.addWidget(label_fecha)
        layout.addWidget(self.fecha_input)
        layout.addWidget(self.boton_guardar)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #f0fdfa;")

    def _estilo_input(self):
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

    def guardar_cambios(self):
        nuevo_titulo = self.titulo_input.text().strip()
        nueva_descripcion = self.descripcion_input.text().strip()
        nueva_fecha_qdate = self.fecha_input.date()
        nueva_fecha = datetime(nueva_fecha_qdate.year(), nueva_fecha_qdate.month(), nueva_fecha_qdate.day())

        if not nuevo_titulo:
            mostrar_mensaje(self, "Campos incompletos", "El título no puede estar vacío.", tipo="advertencia")
            return

        if nueva_fecha < datetime.now():
            mostrar_mensaje(self, "Fecha inválida", "La fecha de vencimiento no puede ser anterior a hoy.", tipo="advertencia")
            return

        # Obtener etiquetas seleccionadas
        etiquetas_seleccionadas = []
        for i in range(self.etiquetas_lista.count()):
            item = self.etiquetas_lista.item(i)
            if item.isSelected():
                etiqueta = item.data(Qt.UserRole)
                etiquetas_seleccionadas.append(etiqueta)

        # Actualizar tarea
        tarea_actualizada = self.tarea_manager.actualizar_tarea(
            id_tarea=self.tarea.id_tarea,
            titulo=nuevo_titulo,
            descripcion=nueva_descripcion,
            fecha_vencimiento=nueva_fecha,
            etiquetas=etiquetas_seleccionadas
        )

        if tarea_actualizada:
            mostrar_mensaje(self, "Tarea actualizada", "La tarea se ha actualizado correctamente.", tipo="info")
            self.accept()
        else:
            mostrar_mensaje(self, "Error", "Ocurrió un error al actualizar la tarea.", tipo="error")
