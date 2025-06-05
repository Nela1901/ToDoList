"""
Módulo para la gestión de etiquetas de las tareas en el sistema ToDoList.

Contiene la clase EtiquetaManager, que ofrece métodos para crear, obtener,
actualizar y eliminar etiquetas. Las etiquetas permiten categorizar y organizar
las tareas de forma personalizada.

Clases:
    EtiquetaManager: Proporciona métodos CRUD para la entidad Etiqueta.
"""

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.modelo.modelo import Etiqueta

class EtiquetaManager:
    """Maneja las operaciones CRUD para la entidad Etiqueta."""

    def __init__(self, session):
        """
        Inicializa el administrador de etiquetas con una sesión de base de datos.

        Args:
            session (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """
        self.session = session

    def crear_etiqueta(self, nombre_etiqueta, color):
        """
        Crea una nueva etiqueta con un nombre y color dados.

        Args:
            nombre_etiqueta (str): Nombre de la etiqueta.
            color (str): Color asociado a la etiqueta.

        Returns:
            Etiqueta: Instancia creada de Etiqueta si se guarda correctamente.
            None: Si ocurre un error de duplicidad o excepción en la base de datos.
        """
        etiqueta = Etiqueta(
            nombre_etiqueta=nombre_etiqueta,
            color=color
        )
        try:
            self.session.add(etiqueta)
            self.session.commit()
            return etiqueta
        except IntegrityError:
            self.session.rollback()
            print("Error: Etiqueta duplicada o datos inválidos al crear.")
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al crear etiqueta: {e}")
            return None

    def obtener_etiquetas(self):
        """
        Obtiene todas las etiquetas almacenadas en la base de datos.

        Returns:
            list[Etiqueta]: Lista con todas las instancias de Etiqueta.
        """
        return self.session.query(Etiqueta).all()

    def obtener_etiqueta_por_id(self, id_etiqueta):
        """
        Obtiene una etiqueta específica por su ID.

        Args:
            id_etiqueta (int): Identificador único de la etiqueta.

        Returns:
            Etiqueta: Instancia de Etiqueta si se encuentra, de lo contrario None.
        """
        return self.session.query(Etiqueta).filter_by(id_etiqueta=id_etiqueta).first()

    def actualizar_etiqueta(self, id_etiqueta, nombre_etiqueta=None, color=None):
        """
        Actualiza los atributos de una etiqueta dada.

        Args:
            id_etiqueta (int): ID de la etiqueta a actualizar.
            nombre_etiqueta (str, optional): Nuevo nombre para la etiqueta.
            color (str, optional): Nuevo color para la etiqueta.

        Returns:
            Etiqueta: Instancia actualizada si la operación fue exitosa.
            None: Si la etiqueta no se encuentra o ocurre un error.
        """
        etiqueta = self.obtener_etiqueta_por_id(id_etiqueta)
        if not etiqueta:
            print("Etiqueta no encontrada para actualizar.")
            return None
        if nombre_etiqueta:
            etiqueta.nombre_etiqueta = nombre_etiqueta
        if color:
            etiqueta.color = color
        try:
            self.session.commit()
            return etiqueta
        except IntegrityError:
            self.session.rollback()
            print("Error: Datos duplicados o inválidos al actualizar etiqueta.")
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al actualizar etiqueta: {e}")
            return None

    def eliminar_etiqueta(self, id_etiqueta):
        """
        Elimina una etiqueta por su ID.

        Args:
            id_etiqueta (int): ID de la etiqueta a eliminar.

        Returns:
            Etiqueta: Instancia eliminada si la operación fue exitosa.
            None: Si la etiqueta no existe o ocurre un error.
        """
        etiqueta = self.obtener_etiqueta_por_id(id_etiqueta)
        if not etiqueta:
            print("Etiqueta no encontrada para eliminar.")
            return None
        try:
            self.session.delete(etiqueta)
            self.session.commit()
            return etiqueta
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al eliminar etiqueta: {e}")
            return None
