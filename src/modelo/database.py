from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Crea la base de datos SQLite (ruta absoluta)
engine = create_engine('sqlite:///D:/TODOLIST/ToDoList/tasks.db', echo=True)

Base = declarative_base()

# Sesión
Session = sessionmaker(bind=engine)
