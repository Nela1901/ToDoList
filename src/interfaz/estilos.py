from PySide6.QtWidgets import QMessageBox

def mostrar_mensaje(parent, titulo, texto, tipo="info", botones=QMessageBox.Ok):
    msg = QMessageBox(parent)
    msg.setWindowTitle(titulo)
    msg.setText(texto)
    msg.setStandardButtons(botones)

    # Íconos
    if tipo == "info":
        msg.setIcon(QMessageBox.Information)
    elif tipo == "advertencia":
        msg.setIcon(QMessageBox.Warning)
    elif tipo == "error":
        msg.setIcon(QMessageBox.Critical)
    elif tipo == "pregunta":
        msg.setIcon(QMessageBox.Question)

    # Estilo pastel moderno
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
