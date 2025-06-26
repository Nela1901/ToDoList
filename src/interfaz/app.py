"""
Módulo principal de la aplicación ToDoList.

Este módulo inicia la aplicación y gestiona el ciclo de login y carga de la ventana principal.
"""

import sys
from PySide6.QtWidgets import QApplication # pylint: disable=no-name-in-module
# from PySide6.QtCore import QObject  # noqa: F401 pylint: disable=unused-import
from src.interfaz.ventana_login import VentanaLogin
from src.interfaz.ventana_principal import VentanaPrincipal


def main():
    """
    Punto de entrada principal de la aplicación.

    Muestra la ventana de login y, si el usuario se autentica,
    abre la ventana principal de tareas.
    """
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
