"""
Módulo para inicializar la tabla de etiquetas en la base de datos del sistema ToDoList.

Este módulo define una función que elimina los registros existentes en la tabla
`etiqueta` y la llena con un conjunto de etiquetas predeterminadas. Estas etiquetas
permiten categorizar las tareas desde el inicio.

Funciones:
    inicializar_etiquetas(): Elimina los registros existentes en la tabla `etiqueta` y
                             los reemplaza con etiquetas iniciales predefinidas.
"""

from src.modelo.database import Session
from src.modelo.modelo import Etiqueta


def inicializar_etiquetas():
    """
    Inicializa la tabla de etiquetas con datos básicos.

    Realiza los siguientes pasos:
    1. Borra todas las etiquetas existentes para evitar duplicados.
    2. Inserta un conjunto de etiquetas iniciales:
       - Personal
       - Urgente
       - Casa
       - Universidad
    3. Confirma la transacción y cierra la sesión.

    Imprime un mensaje de éxito al finalizar.

    Raises:
        SQLAlchemyError: Si ocurre un error durante las operaciones en la base de datos.
    """
    session = Session()

    # 1. Eliminar todas las etiquetas existentes para evitar duplicados
    session.query(Etiqueta).delete()

    # 2. Crear etiquetas iniciales
    etiquetas_iniciales = [
        {"nombre_etiqueta": "Personal"},
        {"nombre_etiqueta": "Urgente"},
        {"nombre_etiqueta": "Casa"},
        {"nombre_etiqueta": "Universidad"}
    ]

    for data in etiquetas_iniciales:
        etiqueta = Etiqueta(**data)
        session.add(etiqueta)

    session.commit()
    session.close()
    print("Etiquetas inicializadas correctamente.")


if __name__ == "__main__":
    inicializar_etiquetas()
