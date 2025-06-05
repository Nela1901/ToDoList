"""
Módulo que define la base declarativa de SQLAlchemy para el proyecto ToDoList.

Contiene la clase Base, que actúa como la base común para todas las entidades
(modelos) del proyecto. Se utiliza para crear todas las tablas en la base de datos
y para establecer las relaciones entre las entidades.

Atributos:
    Base (DeclarativeMeta): Clase base declarativa de SQLAlchemy utilizada
    para definir los modelos de datos.
"""

from sqlalchemy.orm import declarative_base

# Crea la clase base para todas las entidades mapeadas
Base = declarative_base()
