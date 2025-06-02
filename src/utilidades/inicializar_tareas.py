from src.modelo.database import Session
from src.modelo.modelo import Tarea
from datetime import datetime

def inicializar_tareas():
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
