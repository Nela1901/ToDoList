from src.modelo.database import Session
from src.modelo.modelo import Etiqueta

def inicializar_etiquetas():
    session = Session()

    # ✅ 1. Eliminar todas las etiquetas existentes para evitar duplicados
    session.query(Etiqueta).delete()

    # ✅ 2. Crear etiquetas iniciales
    etiquetas_iniciales = [
        {"nombre_etiqueta": "Importante"},
        {"nombre_etiqueta": "Urgente"},
        {"nombre_etiqueta": "Casa"},
        {"nombre_etiqueta": "Trabajo"}
    ]

    for data in etiquetas_iniciales:
        etiqueta = Etiqueta(**data)
        session.add(etiqueta)

    session.commit()
    session.close()
    print("✅ Etiquetas inicializadas correctamente.")

if __name__ == "__main__":
    inicializar_etiquetas()
