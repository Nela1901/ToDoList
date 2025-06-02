from src.modelo.database import Session
from src.modelo.modelo import Recordatorio
from datetime import datetime
def inicializar_recordatorios():
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
