"""
Módulo para la gestión de los estados de las tareas en el sistema ToDoList.

Contiene la clase EstadoManager, que proporciona métodos para crear, obtener,
actualizar y eliminar estados de las tareas. Los estados permiten identificar
en qué etapa se encuentra una tarea (por ejemplo, Pendiente o Completado).

Clases:
    EstadoManager: Proporciona métodos CRUD para la entidad Estado.
"""
# src/logica/estado_manager.py

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.modelo.modelo import Estado

ESTADOS_VALIDOS = {"Pendiente", "Completado"}

class EstadoManager:
    """Clase para gestionar operaciones CRUD sobre los estados de las tareas.

    Args:
        session (Session): Sesión activa de SQLAlchemy para acceder a la base de datos.
    """

    def __init__(self, session):
        """Inicializa el gestor con una sesión de base de datos.

        Args:
            session (Session): Sesión de base de datos.
        """
        self.session = session

    def crear_estado(self, nombre_estado, descripcion=None):
        """Crea un nuevo estado si el nombre está permitido.

        Args:
            nombre_estado (str): Nombre del estado a crear. Debe ser 'Pendiente' o 'Completado'.
            descripcion (str, optional): Descripción opcional del estado.

        Returns:
            Estado: Objeto Estado creado si tiene éxito.
            None: Si el nombre no es válido o ocurre un error durante la creación.
        """
        if nombre_estado not in ESTADOS_VALIDOS:
            print(f"Error: El estado '{nombre_estado}' no está permitido.")
            return None

        estado = Estado(
            nombre_estado=nombre_estado,
            descripcion=descripcion
        )

        try:
            self.session.add(estado)
            self.session.commit()
            return estado
        except IntegrityError:
            self.session.rollback()
            print("Error: Estado duplicado o datos inválidos al crear.")
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al crear estado: {e}")
            return None

    def obtener_estados(self):
        """Recupera todos los estados existentes en la base de datos.

        Returns:
            list[Estado]: Lista de objetos Estado.
        """
        return self.session.query(Estado).all()

    def obtener_estado_por_id(self, id_estado):
        """Obtiene un estado específico por su ID.

        Args:
            id_estado (int): Identificador único del estado.

        Returns:
            Estado: Objeto Estado si se encuentra, None en caso contrario.
        """
        return self.session.query(Estado).filter_by(id_estado=id_estado).first()

    def actualizar_estado(self, id_estado, nombre_estado=None, descripcion=None):
        """Actualiza los campos nombre y/o descripción de un estado existente.

        Args:
            id_estado (int): ID del estado a actualizar.
            nombre_estado (str, optional): Nuevo nombre del estado, debe estar en los válidos.
            descripcion (str, optional): Nueva descripción del estado.

        Returns:
            Estado: Estado actualizado si la operación fue exitosa.
            None: Si el estado no existe, el nombre no es válido, o ocurre un error.
        """
        estado = self.obtener_estado_por_id(id_estado)
        if not estado:
            print("Estado no encontrado para actualizar.")
            return None
        if nombre_estado and nombre_estado not in ESTADOS_VALIDOS:
            print(f"Error: El estado '{nombre_estado}' no está permitido para actualizar.")
            return None
        if nombre_estado:
            estado.nombre_estado = nombre_estado
        if descripcion:
            estado.descripcion = descripcion
        try:
            self.session.commit()
            return estado
        except IntegrityError:
            self.session.rollback()
            print("Error: Datos duplicados o inválidos al actualizar estado.")
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al actualizar estado: {e}")
            return None

    def eliminar_estado(self, id_estado):
        """Elimina un estado por su ID.

        Args:
            id_estado (int): ID del estado a eliminar.

        Returns:
            Estado: Objeto Estado eliminado si tuvo éxito.
            None: Si el estado no existe o ocurre un error.
        """
        estado = self.obtener_estado_por_id(id_estado)
        if not estado:
            print("Estado no encontrado para eliminar.")
            return None
        try:
            self.session.delete(estado)
            self.session.commit()
            return estado
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al eliminar estado: {e}")
            return None
