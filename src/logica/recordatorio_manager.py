"""
Módulo para la gestión de recordatorios en el sistema ToDoList.

Contiene la clase RecordatorioManager, que ofrece métodos para crear, obtener,
actualizar y eliminar recordatorios. Los recordatorios permiten notificar a los
usuarios sobre sus tareas y fechas importantes.

Clases:
    RecordatorioManager: Proporciona métodos CRUD para la entidad Recordatorio.
"""

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.modelo.modelo import Recordatorio

class RecordatorioManager:
    """Gestiona las operaciones CRUD para la entidad Recordatorio."""

    def __init__(self, session):
        """
        Inicializa el administrador de recordatorios con una sesión de base de datos.

        Args:
            session (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """
        self.session = session

    def crear_recordatorio(self, id_tarea, fecha_hora, tipo):
        """
        Crea un nuevo recordatorio asociado a una tarea.

        Args:
            id_tarea (int): ID de la tarea asociada al recordatorio.
            fecha_hora (datetime): Fecha y hora del recordatorio.
            tipo (str): Tipo de recordatorio.

        Returns:
            Recordatorio: Instancia creada de Recordatorio si se guarda correctamente.
            None: Si ocurre un error de duplicidad o excepción en la base de datos.
        """
        recordatorio = Recordatorio(
            id_tarea=id_tarea,
            fecha_hora=fecha_hora,
            tipo=tipo
        )
        try:
            self.session.add(recordatorio)
            self.session.commit()
            return recordatorio
        except IntegrityError:
            self.session.rollback()
            print("Error: Datos duplicados o inválidos al crear recordatorio.")
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al crear recordatorio: {e}")
            return None

    def obtener_recordatorios(self):
        """
        Obtiene todos los recordatorios almacenados en la base de datos.

        Returns:
            list[Recordatorio]: Lista con todas las instancias de Recordatorio.
        """
        return self.session.query(Recordatorio).all()

    def obtener_recordatorio_por_id(self, id_recordatorio):
        """
        Obtiene un recordatorio específico por su ID.

        Args:
            id_recordatorio (int): Identificador único del recordatorio.

        Returns:
            Recordatorio: Instancia de Recordatorio si se encuentra, de lo contrario None.
        """
        return self.session.query(Recordatorio).filter_by(id_recordatorio=id_recordatorio).first()

    def actualizar_recordatorio(self, id_recordatorio, fecha_hora=None, tipo=None):
        """
        Actualiza los atributos de un recordatorio dado.

        Args:
            id_recordatorio (int): ID del recordatorio a actualizar.
            fecha_hora (datetime, optional): Nueva fecha y hora del recordatorio.
            tipo (str, optional): Nuevo tipo de recordatorio.

        Returns:
            Recordatorio: Instancia actualizada si la operación fue exitosa.
            None: Si el recordatorio no se encuentra o ocurre un error.
        """
        recordatorio = self.obtener_recordatorio_por_id(id_recordatorio)
        if not recordatorio:
            print("Recordatorio no encontrado para actualizar.")
            return None
        if fecha_hora:
            recordatorio.fecha_hora = fecha_hora
        if tipo:
            recordatorio.tipo = tipo
        try:
            self.session.commit()
            return recordatorio
        except IntegrityError:
            self.session.rollback()
            print("Error: Datos duplicados o inválidos al actualizar recordatorio.")
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al actualizar recordatorio: {e}")
            return None

    def eliminar_recordatorio(self, id_recordatorio):
        """
        Elimina un recordatorio por su ID.

        Args:
            id_recordatorio (int): ID del recordatorio a eliminar.

        Returns:
            Recordatorio: Instancia eliminada si la operación fue exitosa.
            None: Si el recordatorio no existe o ocurre un error.
        """
        recordatorio = self.obtener_recordatorio_por_id(id_recordatorio)
        if not recordatorio:
            print("Recordatorio no encontrado para eliminar.")
            return None
        try:
            self.session.delete(recordatorio)
            self.session.commit()
            return recordatorio
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al eliminar recordatorio: {e}")
            return None
