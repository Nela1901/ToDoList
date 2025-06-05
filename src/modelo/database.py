"""
Módulo para la configuración de la base de datos y la creación de tablas.

Este módulo configura la conexión a la base de datos SQLite, crea las tablas
definidas en el modelo y permite inicializar datos básicos cuando se ejecuta
directamente.

Attributes:
    engine (Engine): Motor de conexión a la base de datos SQLite.
    Session (sessionmaker): Fábrica de sesiones para interactuar con la base de datos.

Ejecución directa:
    Si se ejecuta este archivo directamente, se inicializan las tablas y
    se cargan datos iniciales mediante los módulos de inicialización.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.modelo import modelo  # noqa: F401
from src.modelo.declarative_base import Base  # Aquí importas el único Base

# Crea la base de datos SQLite (ruta absoluta o relativa)
engine = create_engine('sqlite:///D:/TODOLIST/ToDoList/tasks.db', echo=True)

# Sesión
Session = sessionmaker(bind=engine)

# Crea todas las tablas definidas en el modelo
Base.metadata.create_all(engine)

if __name__ == "__main__":
    """
    Si se ejecuta directamente, inicializa las tablas con datos predefinidos.
    """

    import src.utilidades.inicializador_usuarios as usuario
    import src.utilidades.inicializador_estados as estado
    import src.utilidades.inicializador_etiqueta as etiqueta
    import src.utilidades.inicializador_tareas as tarea
    import src.utilidades.inicializador_recordatorio as recordatorio

    print("Creando las tablas y llenando datos iniciales...")

    usuario.inicializar_usuarios()
    estado.inicializar_estados()
    etiqueta.inicializar_etiquetas()
    tarea.inicializar_tareas()
    recordatorio.inicializar_recordatorios()

    print("¡Base de datos lista y con datos iniciales!")
