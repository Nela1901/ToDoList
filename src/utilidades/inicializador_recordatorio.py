"""
Módulo para inicializar la tabla de recordatorios en la base de datos del sistema ToDoList.

Define una función que limpia los datos existentes en la tabla `recordatorio` y agrega
un conjunto inicial de recordatorios con fechas y tareas asociadas.

Funciones:
    inicializar_recordatorios(): Borra los registros actuales y crea recordatorios iniciales.
"""

from src.modelo.database import Session
from src.modelo.modelo import Recordatorio
from datetime import datetime

def inicializar_recordatorios():
    """
    Inicializa la tabla de recordatorios con datos predeterminados.

    Pasos realizados:
    1. Elimina todos los recordatorios existentes para evitar duplicados.
    2. Inserta recordatorios con fecha, hora y tarea asociada.
    3. Confirma la transacción y cierra la sesión.
    4. Imprime un mensaje de éxito.

    Raises:
        SQLAlchemyError: Si ocurre un error durante las operaciones en la base de datos.
    """
    session = Session()

    # Opcionalmente, elimina duplicados antes:
    session.query(Recordatorio).delete()

    recordatorios_iniciales = [
        {
            "fecha_hora": datetime(2025, 6, 1, 8, 0, 0),
            "id_tarea": 1
        },
        {
            "fecha_hora": datetime(2025, 6, 2, 9, 0, 0),
            "id_tarea": 2
        }
    ]

    for data in recordatorios_iniciales:
        recordatorio = Recordatorio(**data)
        session.add(recordatorio)

    session.commit()
    session.close()
    print("Recordatorios inicializados correctamente")

if __name__ == "__main__":
    inicializar_recordatorios()
