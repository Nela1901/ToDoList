"""
Módulo de estilos y utilidades para mensajes emergentes (QMessageBox) personalizados.
"""

from PySide6.QtWidgets import QMessageBox  # pylint: disable=no-name-in-module

def mostrar_mensaje(parent, titulo, texto, tipo="info", botones=QMessageBox.Ok):
    """
    Muestra un cuadro de mensaje con estilo pastel personalizado.

    Parámetros:
        parent (QWidget): Componente padre del mensaje.
        titulo (str): Título de la ventana del mensaje.
        texto (str): Texto que se mostrará dentro del mensaje.
        tipo (str): Tipo de mensaje: 'info', 'advertencia', 'error', 'pregunta'.
        botones (QMessageBox.StandardButtons): Botones que se mostrarán.

    Retorna:
        int: Código del botón presionado.
    """
    msg = QMessageBox(parent)
    msg.setWindowTitle(titulo)
    msg.setText(texto)
    msg.setStandardButtons(botones)

    # Íconos según el tipo
    if tipo == "info":
        msg.setIcon(QMessageBox.Information)
    elif tipo == "advertencia":
        msg.setIcon(QMessageBox.Warning)
    elif tipo == "error":
        msg.setIcon(QMessageBox.Critical)
    elif tipo == "pregunta":
        msg.setIcon(QMessageBox.Question)

    # Estilo pastel moderno
    # es un metodo que permite aplicar
    #  estilos visuales
    #  (como colores, bordes, fuentes) a
    #  los componentes de la interfaz en PySide6
    #  usando código similar a CSS (hojas de estilo).

    # setStyleSheet:Le pasa una cadena con estilos
    # en formato CSS para modificar su apariencia.

    # msg: es un objeto como
    # QMessageBox, QLabel, QPushButton
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #F4FBFF;
            font-family: 'Segoe UI';
            font-size: 14px;
        }
        QLabel {
            color: #333;
        }
        QPushButton {
            background-color: #76a9ed;
            color: white;
            padding: 6px 12px;
            border-radius: 8px;
            font-weight: bold;
            min-width: 80px;
        }
        QPushButton:hover {
            background-color: #00c2cb;
        }
    """)
    return msg.exec()
