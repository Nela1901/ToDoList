"""
Módulo para inicializar la tabla de tareas en la base de datos del sistema ToDoList.

Contiene una función que elimina las tareas existentes y crea tareas iniciales
con datos de ejemplo para facilitar pruebas y desarrollo.

Funciones:
    inicializar_tareas(): Borra registros existentes e inserta tareas predeterminadas.
"""
from datetime import datetime
from src.modelo.database import Session
from src.modelo.modelo import Tarea


def inicializar_tareas():
    """
    Inicializa la tabla `tarea` con registros predeterminados.

    Pasos realizados:
        1. Elimina todos los registros existentes para evitar duplicados.
        2. Inserta tareas con atributos como título, descripción, fechas,
           estado y usuario asociado.
        3. Confirma los cambios y cierra la sesión de la base de datos.
        4. Imprime un mensaje de confirmación.

    Raises:
        SQLAlchemyError: Si ocurre un error en la operación con la base de datos.
    """
    session = Session()

    # Eliminar todos los registros existentes
    session.query(Tarea).delete()
    session.commit()

    # Insertar tareas iniciales
    tareas_iniciales = [
        {
            "titulo": "Tarea de ejemplo",
            "descripcion": "Descripción de ejemplo",
            "fecha_creacion": datetime(2025, 6, 1, 0, 0, 0),
            "fecha_vencimiento": datetime(2025, 6, 2, 0, 0, 0),
            "id_estado": 1,
            "id_usuario": 1
        },
        {
            "titulo": "Otra tarea",
            "descripcion": "Otra descripción",
            "fecha_creacion": datetime(2025, 6, 1, 0, 0, 0),
            "fecha_vencimiento": datetime(2025, 6, 2, 0, 0, 0),
            "id_estado": 2,
            "id_usuario": 2
        }
    ]

    for tarea_data in tareas_iniciales:
        tarea = Tarea(**tarea_data)
        session.add(tarea)

    session.commit()
    print("Tabla tarea inicializada correctamente.")
    session.close()

if __name__ == "__main__":
    inicializar_tareas()
