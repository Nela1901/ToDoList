"""
Modelo de datos para el sistema de gestión de tareas (ToDoList).

Define las entidades principales del sistema utilizando SQLAlchemy:
- Usuario: Representa a los usuarios del sistema.
- Estado: Representa los estados que pueden tener las tareas (por ejemplo, Pendiente,
Completado).
- Etiqueta: Permite categorizar tareas con etiquetas y colores personalizados.
- Tarea: Contiene información sobre las tareas, su estado y usuario asociado.
- Recordatorio: Almacena recordatorios vinculados a tareas.
- Tabla intermedia tarea_etiqueta: Permite la relación muchos a muchos entre Tareas
y Etiquetas.

Las relaciones están definidas mediante SQLAlchemy ORM, facilitando la gestión de
la base de datos.

Atributos del módulo:
    tarea_etiqueta (Table): Tabla intermedia para la relación muchos a muchos entre
    Tarea y Etiqueta.

Clases:
    Usuario: Representa a un usuario del sistema.
    Estado: Representa un estado posible de las tareas.
    Etiqueta: Representa una etiqueta para las tareas.
    Tarea: Representa una tarea específica.
    Recordatorio: Representa un recordatorio asociado a una tarea.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from src.modelo.declarative_base import Base


# Tabla intermedia para la relación muchos a muchos entre Tarea y Etiqueta
tarea_etiqueta = Table(
    'tarea_etiqueta', Base.metadata,
    Column(
        'id_tarea', Integer, ForeignKey('tarea.id_tarea'), primary_key=True
    ),
    Column(
        'id_etiqueta', Integer, ForeignKey('etiqueta.id_etiqueta'), primary_key=True
    )
)
# pylint: disable=too-few-public-methods
class Usuario(Base):
    """
        Representa a un usuario en el sistema.

        Atributos:
            id_usuario (int): Identificador único del usuario.
            nombre_usuario (str): Nombre del usuario, único y no nulo.
            correo_electronico (str): Correo electrónico del usuario, único y no nulo.
            contrasena (str): Contraseña encriptada del usuario.
            tareas (list[Tarea]): Lista de tareas asociadas al usuario.
        """
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(100), nullable=False, unique=True)
    correo_electronico = Column(String(150), nullable=False, unique=True, index=True)
    contrasena = Column(String(255), nullable=False)

    tareas = relationship("Tarea", back_populates="usuario")
# pylint: disable=too-few-public-methods
class Estado(Base):
    """
        Representa un estado posible que puede tener una tarea (por ejemplo, Pendiente,
        Completado).

        Atributos:
            id_estado (int): Identificador único del estado.
            nombre_estado (str): Nombre del estado.
            descripcion (str): Descripción opcional del estado.
            tareas (list[Tarea]): Lista de tareas que tienen este estado.
        """
    __tablename__ = 'estado'

    id_estado = Column(Integer, primary_key=True, autoincrement=True)
    nombre_estado = Column(String(50), nullable=False)
    descripcion = Column(String(150))

    tareas = relationship("Tarea", back_populates="estado")
# pylint: disable=too-few-public-methods
class Etiqueta(Base):
    """
       Representa una etiqueta para categorizar tareas.

       Atributos:
           id_etiqueta (int): Identificador único de la etiqueta.
           nombre_etiqueta (str): Nombre de la etiqueta.
           color (str): Color asociado a la etiqueta.
           tareas (list[Tarea]): Lista de tareas que tienen esta etiqueta.
       """
    __tablename__ = 'etiqueta'

    id_etiqueta = Column(Integer, primary_key=True, autoincrement=True)
    nombre_etiqueta = Column(String(50), nullable=False)
    color = Column(String(20))

    tareas = relationship(
        "Tarea", secondary=tarea_etiqueta, back_populates="etiquetas"
    )
# pylint: disable=too-few-public-methods
class Tarea(Base):
    """
        Representa una tarea en el sistema.

        Atributos:
            id_tarea (int): Identificador único de la tarea.
            titulo (str): Título de la tarea.
            descripcion (str): Descripción detallada de la tarea.
            fecha_creacion (datetime): Fecha en la que se creó la tarea.
            fecha_vencimiento (datetime): Fecha límite de la tarea.
            id_estado (int): Identificador del estado de la tarea.
            id_usuario (int): Identificador del usuario propietario de la tarea.
            usuario (Usuario): Relación con el usuario propietario.
            estado (Estado): Relación con el estado de la tarea.
            etiquetas (list[Etiqueta]): Lista de etiquetas asociadas a la tarea.
            recordatorios (list[Recordatorio]): Lista de recordatorios de la tarea.
        """
    __tablename__ = 'tarea'

    id_tarea = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime)
    fecha_vencimiento = Column(DateTime)

    id_estado = Column(Integer, ForeignKey('estado.id_estado'), index=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), index=True)

    usuario = relationship("Usuario", back_populates="tareas")
    estado = relationship("Estado", back_populates="tareas")
    etiquetas = relationship(
        "Etiqueta", secondary=tarea_etiqueta, back_populates="tareas"
    )
    recordatorios = relationship("Recordatorio", back_populates="tarea")
# pylint: disable=too-few-public-methods
class Recordatorio(Base):
    """
        Representa un recordatorio asociado a una tarea.

        Atributos:
            id_recordatorio (int): Identificador único del recordatorio.
            id_tarea (int): Identificador de la tarea asociada.
            fecha_hora (datetime): Fecha y hora del recordatorio.
            tipo (str): Tipo de recordatorio (por ejemplo, Email, Notificación).
            tarea (Tarea): Relación con la tarea asociada.
        """
    __tablename__ = 'recordatorio'

    id_recordatorio = Column(Integer, primary_key=True, autoincrement=True)
    id_tarea = Column(Integer, ForeignKey('tarea.id_tarea'))
    fecha_hora = Column(DateTime)
    tipo = Column(String(50))

    tarea = relationship("Tarea", back_populates="recordatorios")
