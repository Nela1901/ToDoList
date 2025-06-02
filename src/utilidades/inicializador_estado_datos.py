# src/utils/inicializar_estados.py

from src.modelo.database import Session
from src.modelo.modelo import Estado

def inicializar_estados():
    session = Session()

    # Limpia la tabla primero
    session.query(Estado).delete()
    session.commit()

    # Datos iniciales
    estados_iniciales = [
        {"id_estado": 1, "nombre_estado": "En curso", "descripcion": "Actualización de descripción"},
        {"id_estado": 2, "nombre_estado": "Pendiente", "descripcion": "Tarea aún no comenzada"},
        {"id_estado": 3, "nombre_estado": "Completado", "descripcion": "Tarea finalizada"}
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
