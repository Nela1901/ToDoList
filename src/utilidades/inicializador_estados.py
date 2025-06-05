"""
Módulo para inicializar la tabla de estados en la base de datos del sistema ToDoList.

Este módulo contiene una función que borra los registros existentes de la tabla
`estado` y la llena con datos iniciales predeterminados. Esto asegura que siempre
existan los estados básicos requeridos por el sistema (como "Pendiente" y "Completado").

Funciones:
    inicializar_estados(): Borra los datos existentes en la tabla `estado` y la llena
                           con datos iniciales predefinidos.
"""

from src.modelo.database import Session
from src.modelo.modelo import Estado


def inicializar_estados():
    """
    Inicializa la tabla de estados con datos básicos.

    Este procedimiento realiza los siguientes pasos:
    1. Borra todos los registros existentes en la tabla `estado`.
    2. Inserta un conjunto de estados iniciales:
       - Pendiente
       - Completado
    3. Confirma la transacción y cierra la sesión.

    Imprime un mensaje de éxito al finalizar.

    Raises:
        SQLAlchemyError: Si ocurre un error al interactuar con la base de datos.
    """
    session = Session()

    # Limpia la tabla primero
    session.query(Estado).delete()
    session.commit()

    # Datos iniciales
    estados_iniciales = [
        {"id_estado": 1, "nombre_estado": "Pendiente", "descripcion": "Tarea aún no comenzada"},
        {"id_estado": 2, "nombre_estado": "Completado", "descripcion": "Tarea finalizada"}
    ]

    # Inserta los datos iniciales
    for estado_data in estados_iniciales:
        estado = Estado(**estado_data)
        session.add(estado)
    session.commit()
    print("Datos iniciales insertados correctamente.")

    session.close()


if __name__ == "__main__":
    inicializar_estados()
