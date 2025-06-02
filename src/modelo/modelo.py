# src/modelo/modelo.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from src.modelo.declarative_base import Base

# Tabla intermedia para la relación muchos a muchos entre Tarea y Etiqueta
tarea_etiqueta = Table(
    'tarea_etiqueta', Base.metadata,
    Column('id_tarea', Integer, ForeignKey('tarea.id_tarea'), primary_key=True),
    Column('id_etiqueta', Integer, ForeignKey('etiqueta.id_etiqueta'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(100), nullable=False)
    correo_electronico = Column(String(150), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)

    tareas = relationship("Tarea", back_populates="usuario")

class Estado(Base):
    __tablename__ = 'estado'

    id_estado = Column(Integer, primary_key=True, autoincrement=True)
    nombre_estado = Column(String(50), nullable=False)
    descripcion = Column(String(150))

    tareas = relationship("Tarea", back_populates="estado")

class Etiqueta(Base):
    __tablename__ = 'etiqueta'

    id_etiqueta = Column(Integer, primary_key=True, autoincrement=True)
    nombre_etiqueta = Column(String(50), nullable=False)
    color = Column(String(20))

    tareas = relationship("Tarea", secondary=tarea_etiqueta, back_populates="etiquetas")

class Tarea(Base):
    __tablename__ = 'tarea'

    id_tarea = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime)
    fecha_vencimiento = Column(DateTime)

    id_estado = Column(Integer, ForeignKey('estado.id_estado'))
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))

    usuario = relationship("Usuario", back_populates="tareas")
    estado = relationship("Estado", back_populates="tareas")
    etiquetas = relationship("Etiqueta", secondary=tarea_etiqueta, back_populates="tareas")
    recordatorios = relationship("Recordatorio", back_populates="tarea")

class Recordatorio(Base):
    __tablename__ = 'recordatorio'

    id_recordatorio = Column(Integer, primary_key=True, autoincrement=True)
    id_tarea = Column(Integer, ForeignKey('tarea.id_tarea'))
    fecha_hora = Column(DateTime)
    tipo = Column(String(50))

    tarea = relationship("Tarea", back_populates="recordatorios")


