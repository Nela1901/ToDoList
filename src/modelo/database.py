"""
Módulo para la configuración de la base de datos y la creación de tablas.

Este módulo configura la conexión a la base de datos SQLite, crea las tablas
definidas en el modelo

Attributes:
    engine (Engine): Motor de conexión a la base de datos SQLite.
    Session (sessionmaker): Fábrica de sesiones para interactuar con la base de datos.

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.modelo.declarative_base import Base
from src.modelo import modelo  # pylint: disable=unused-import

# Crea la base de datos SQLite (ruta absoluta o relativa)
engine = create_engine('sqlite:///D:/TODOLIST/ToDoList/tasks.db', echo=True)

# Sesión
Session = sessionmaker(bind=engine)

# Crea todas las tablas definidas en el modelo
Base.metadata.create_all(engine)
