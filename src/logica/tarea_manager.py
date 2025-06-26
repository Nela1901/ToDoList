"""
Módulo para la gestión de tareas en el sistema ToDoList.

Contiene la clase TareaManager, que ofrece métodos para crear, obtener,
actualizar y eliminar tareas. Además, permite relacionar tareas con usuarios,
estados y etiquetas.

Clases:
    TareaManager: Proporciona métodos CRUD para la entidad Tarea.
"""

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.modelo.modelo import Tarea, Estado

class TareaManager:
    """Gestiona las operaciones CRUD para la entidad Tarea."""

    def __init__(self, session):
        """
        Inicializa el administrador de tareas con una sesión de base de datos.

        Args:
            session (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """
        self.session = session

    def crear_tarea(self, titulo, descripcion, fecha_creacion, fecha_vencimiento, **kwargs):
        """
        Crea una nueva tarea con los detalles proporcionados.

        Args:
            titulo (str): Título de la tarea.
            descripcion (str): Descripción detallada de la tarea.
            fecha_creacion (datetime): Fecha y hora de creación de la tarea.
            fecha_vencimiento (datetime): Fecha y hora límite para completar la tarea.
            **kwargs: Otros atributos como id_usuario, id_estado, etc.

        Returns:
            Tarea: Instancia creada de Tarea si se guarda correctamente.
            None: Si ocurre un error de duplicidad o excepción en la base de datos.
        """
        tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_creacion=fecha_creacion,
            fecha_vencimiento=fecha_vencimiento,
            **kwargs
        )
        try:
            self.session.add(tarea)
            self.session.commit()
            return tarea
        except IntegrityError:
            self.session.rollback()
            print(
                "Error: Datos duplicados o inválidos "
                "al crear tarea."
            )
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(
                f"Error inesperado al crear tarea: {e}"
            )
            return None

    def obtener_tareas(self):
        """
        Obtiene todas las tareas almacenadas en la base de datos.

        Returns:
            list[Tarea]: Lista con todas las instancias de Tarea.
        """
        return self.session.query(Tarea).all()


    def actualizar_tarea(self, id_tarea, **kwargs):
        """
        Actualiza los atributos de una tarea dada.

        Args:
            id_tarea (int): ID de la tarea a actualizar.
            **kwargs: Campos y valores a actualizar (
            titulo, descripcion, fecha_vencimiento, id_estado
            ).

        Returns:
            Tarea: Instancia actualizada si la operación fue exitosa.
            None: Si la tarea no se encuentra o ocurre un error.
        """
        tarea = self.obtener_tarea_por_id(id_tarea)
        if not tarea:
            print(
                "Tarea no encontrada para actualizar."
            )
            return None

        for attr, value in kwargs.items():
            setattr(tarea, attr, value)

        try:
            self.session.commit()
            return tarea
        except IntegrityError:
            self.session.rollback()
            print(
                "Error: Datos duplicados o inválidos "
                "al actualizar tarea."
            )
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(
                f"Error inesperado al actualizar tarea: {e}"
            )
            return None

    def eliminar_tarea(self, tarea):
        """Elimina una tarea existente de la base de datos."""
        self.session.delete(tarea)
        self.session.commit()

    def obtener_tarea_por_id(self, id_tarea):
        """
        Obtiene una tarea específica por su ID.

        Args:
            id_tarea (int): Identificador único de la tarea.

        Returns:
            Tarea: Instancia de Tarea si se encuentra, de lo contrario None.
        """
        return self.session.query(Tarea).filter_by(id_tarea=id_tarea).first()

    def obtener_tareas_por_usuario(self, id_usuario: int):
        """Obtiene todas las tareas asociadas a un usuario."""
        return (
            self.session.query(Tarea)
            .options(joinedload(Tarea.etiquetas))
            .filter_by(id_usuario=id_usuario)
            .all()
        )

    def marcar_completado(self, tarea):
        """Marca una tarea como completada actualizando su estado."""
        estado_completado = self.session.query(Estado).filter_by(nombre_estado="Completado").first()
        if not estado_completado:
            estado_completado = Estado(nombre_estado="Completado")
            self.session.add(estado_completado)
            self.session.commit()

        if tarea.id_estado != estado_completado.id_estado:
            tarea.id_estado = estado_completado.id_estado
            self.session.commit()
