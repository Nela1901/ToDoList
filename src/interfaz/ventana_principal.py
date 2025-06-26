import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QApplication, QMenuBar, QMenu, QMessageBox,
    QHBoxLayout, QTableWidget, QTableWidgetItem
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from functools import partial
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from src.interfaz.ventana_crear_cuenta import VentanaCrearCuenta
from src.interfaz.ventana_anadir_tarea import VentanaAnadirTarea
from src.interfaz.estilos import mostrar_mensaje
from src.modelo.database import Session
from src.logica.tarea_manager import TareaManager
from src.interfaz.ventana_editar_tarea import VentanaEditarTarea
from src.interfaz.ventana_cambiar_contrasena import VentanaCambiarContrasena

class VentanaPrincipal(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("ToDoList")
        self.setGeometry(300, 150, 900, 600)

        self.session = Session()
        self.tarea_manager = TareaManager(self.session)

        self._configurar_ui()
        self._crear_menu()
        self.cargar_tareas()

    def _configurar_ui(self):
        contenedor = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel(f"¿Qué tareas más tenemos, {self.usuario.nombre_usuario}?")
        self.label.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 26px;
            font-weight: bold;
            color: #060606;
            padding: 10px;
        """)
        self.label.setAlignment(Qt.AlignCenter)

        self.boton_agregar = QPushButton("➕ Añadir tarea")
        self.boton_agregar.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            background-color: #00c2cb;
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            color: #ffffff;
        """)
        self.boton_agregar.clicked.connect(self.abrir_ventana_añadir_tarea)

        self.tabla_tareas = QTableWidget()
        self.tabla_tareas.setColumnCount(6)
        self.tabla_tareas.setHorizontalHeaderLabels(["✔", "Título", "Descripción", "Vencimiento", "Etiqueta","Acciones"])
        self.tabla_tareas.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            background-color: #ffffff;
            border: 1px solid #bccd7b;
            border-radius: 8px;
            font-size: 14px;
        """)
        self.tabla_tareas.horizontalHeader().setStretchLastSection(True)
        self.tabla_tareas.setColumnWidth(0, 50)
        self.tabla_tareas.setColumnWidth(1, 180)
        self.tabla_tareas.setColumnWidth(2, 200)
        self.tabla_tareas.setColumnWidth(3, 100)
        self.tabla_tareas.setColumnWidth(4, 150)
        self.tabla_tareas.setColumnWidth(5, 120)

        leyenda_iconos = QLabel("✏️ Editar    🗑️ Eliminar    ✔️ Marcar como completada    🕒 Pendiente    ✅ Completada")
        leyenda_iconos.setAlignment(Qt.AlignCenter)
        leyenda_iconos.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 12px;
            color: #555555;
            padding-top: 5px;
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.boton_agregar)
        layout.addWidget(self.tabla_tareas)
        layout.addWidget(leyenda_iconos)

        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)
        self.setStyleSheet("background-color: #f0fdfa;")

    def _crear_menu(self):
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #f0fdfa;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 14px;
                padding: 6px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                margin: 2px;
            }
            QMenuBar::item:selected {
                background-color: #cceeff;
                border-radius: 6px;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #cceeff;
                padding: 6px;
                font-size: 13px;
                font-family: 'Segoe UI';
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 6px;
                color: #333333;
                background-color: transparent;
            }
            QMenu::item:selected {
                background-color: #d0f0f7;
                color: #035c63;
            }
        """)

        menu_hamburguesa = QMenu("☰", self)

        # Acción: Crear cuenta
        accion_crear = QAction("➕ Crear cuenta", self)
        accion_crear.triggered.connect(self.abrir_ventana_crear_cuenta)
        menu_hamburguesa.addAction(accion_crear)

        # Acción: Cambiar contraseña
        accion_cambiar_contrasena = QAction("🔐 Cambiar contraseña", self)
        accion_cambiar_contrasena.triggered.connect(self.abrir_ventana_cambiar_contrasena)
        menu_hamburguesa.addAction(accion_cambiar_contrasena)

        # Acción: Cerrar sesión
        accion_cerrar = QAction("🚪 Cerrar sesión", self)
        accion_cerrar.triggered.connect(self.cerrar_sesion)
        menu_hamburguesa.addAction(accion_cerrar)

        menu_bar.addMenu(menu_hamburguesa)

    def cargar_tareas(self):
        self.tabla_tareas.setRowCount(0)
        tareas = self.tarea_manager.obtener_tareas_por_usuario(self.usuario.id_usuario)

        for fila, tarea in enumerate(tareas):
            self.tabla_tareas.insertRow(fila)

            completado = "✅" if tarea.estado.nombre_estado == "Completado" else "🕒"
            self.tabla_tareas.setItem(fila, 0, QTableWidgetItem(completado))
            self.tabla_tareas.setItem(fila, 1, QTableWidgetItem(tarea.titulo))
            self.tabla_tareas.setItem(fila, 2, QTableWidgetItem(tarea.descripcion))
            self.tabla_tareas.setItem(fila, 3, QTableWidgetItem(tarea.fecha_vencimiento.strftime("%d/%m/%Y")))

            # Mostrar etiquetas
            if tarea.etiquetas:
                etiquetas_texto = ", ".join([etiqueta.nombre_etiqueta for etiqueta in tarea.etiquetas])
            else:
                etiquetas_texto = "—"

            item_etiquetas = QTableWidgetItem(etiquetas_texto)
            item_etiquetas.setToolTip(etiquetas_texto)  # Para texto largo
            self.tabla_tareas.setItem(fila, 4, item_etiquetas)

            contenedor_botones = QWidget()
            contenedor_botones.setStyleSheet("background-color: transparent; border: none;")
            layout_botones = QHBoxLayout(contenedor_botones)
            layout_botones.setContentsMargins(0, 0, 0, 0)

            btn_editar = QPushButton("✏️")
            btn_eliminar = QPushButton("🗑️")
            btn_completar = QPushButton("✔️")

            for btn in [btn_editar, btn_eliminar, btn_completar]:
                btn.setFixedSize(28, 28)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #76a9ed;
                        border-radius: 6px;
                        color: white;
                        font-size: 12px;
                    }
                """)

            btn_editar.clicked.connect(partial(self.editar_tarea, tarea))
            btn_eliminar.clicked.connect(partial(self.eliminar_tarea, tarea))
            btn_completar.clicked.connect(partial(self.marcar_completada, tarea))

            layout_botones.addWidget(btn_editar)
            layout_botones.addWidget(btn_eliminar)
            layout_botones.addWidget(btn_completar)
            self.tabla_tareas.setCellWidget(fila, 5, contenedor_botones)

    def abrir_ventana_añadir_tarea(self):
        ventana = VentanaAnadirTarea(self)
        if ventana.exec():
            self.cargar_tareas()

    def abrir_ventana_crear_cuenta(self):
        ventana = VentanaCrearCuenta()
        ventana.exec()

    def cerrar_sesion(self):
        respuesta = mostrar_mensaje(
            self,
            "Cerrar sesión",
            "¿Estás seguro de que deseas cerrar sesión?",
            tipo="pregunta",
            botones=QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            self.close()

    def editar_tarea(self, tarea=None):
        ventana = VentanaEditarTarea(tarea, self.session, self)  # le pasas self.session
        if ventana.exec():
            self.cargar_tareas()

    def marcar_completada(self, tarea=None):
            if tarea and tarea.estado.nombre_estado != "Completado":
                try:
                    self.tarea_manager.marcar_completado(tarea)
                    mostrar_mensaje(self, "¡Tarea completada!", "La tarea ha sido marcada como completada.", tipo="info")
                    self.cargar_tareas()
                except Exception as e:
                    mostrar_mensaje(self, "Error", f"No se pudo marcar como completada: {e}", tipo="error")
            else:
                mostrar_mensaje(self, "Ya está completada", "La tarea ya estaba marcada como completada.", tipo="info")

    def eliminar_tarea(self, tarea):
        respuesta = mostrar_mensaje(
            self,
            "Eliminar tarea",
            "¿Estás seguro de que deseas eliminar esta tarea?",
            tipo="pregunta",
            botones=QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            try:
                self.tarea_manager.eliminar_tarea(tarea)
                mostrar_mensaje(self, "Tarea eliminada", "La tarea ha sido eliminada correctamente.", tipo="info")
                self.cargar_tareas()
            except Exception as e:
                mostrar_mensaje(self, "Error", f"No se pudo eliminar la tarea: {e}", tipo="error")

    def abrir_ventana_cambiar_contrasena(self):
        ventana = VentanaCambiarContrasena(usuario=self.usuario, parent=self)
        ventana.exec()
