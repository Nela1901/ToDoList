# app.py (ubicado en src/interfaz/app.py)

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject
from src.interfaz.ventana_login import VentanaLogin
from src.interfaz.ventana_principal import VentanaPrincipal

def main():
    app = QApplication(sys.argv)

    while True:
        login = VentanaLogin()
        if login.exec():
            ventana_principal = VentanaPrincipal(login.usuario)
            ventana_principal.show()

            app.exec()  # Espera mientras se cierra ventana principal
        else:
            break  # Usuario cerró login sin autenticarse

if __name__ == "__main__":
    main()
