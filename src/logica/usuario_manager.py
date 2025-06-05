"""
Módulo para la gestión de usuarios en el sistema ToDoList.

Contiene la clase UsuarioManager, que ofrece métodos para crear, obtener,
actualizar y eliminar usuarios. Permite gestionar los datos de los usuarios
que acceden al sistema.

Clases:
    UsuarioManager: Proporciona métodos CRUD para la entidad Usuario.
"""
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.modelo.modelo import Usuario


class UsuarioManager:
    """Gestiona las operaciones CRUD para la entidad Usuario."""

    def __init__(self, session):
        """
        Inicializa el administrador de usuarios con una sesión de base de datos.

        Args:
            session (Session): Sesión activa de SQLAlchemy para interactuar con la base de datos.
        """
        self.session = session

    def crear_usuario(self, nombre_usuario, correo_electronico, contrasena):
        """
        Crea un nuevo usuario con la información proporcionada.

        Args:
            nombre_usuario (str): Nombre de usuario.
            correo_electronico (str): Correo electrónico del usuario.
            contrasena (str): Contraseña del usuario.

        Returns:
            Usuario: Instancia creada de Usuario si se guarda correctamente.
            None: Si ocurre un error de duplicidad o excepción en la base de datos.
        """
        usuario = Usuario(
            nombre_usuario=nombre_usuario,
            correo_electronico=correo_electronico,
            contrasena=contrasena
        )
        try:
            self.session.add(usuario)
            self.session.commit()
            return usuario
        except IntegrityError:
            self.session.rollback()
            print("Error: Usuario con ese nombre o correo ya existe.")
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado: {e}")
            return None

    def obtener_usuarios(self):
        """
        Obtiene todos los usuarios almacenados en la base de datos.

        Returns:
            list[Usuario]: Lista con todas las instancias de Usuario.
        """
        return self.session.query(Usuario).all()

    def obtener_usuario_por_id(self, id_usuario):
        """
        Obtiene un usuario específico por su ID.

        Args:
            id_usuario (int): Identificador único del usuario.

        Returns:
            Usuario: Instancia de Usuario si se encuentra, de lo contrario None.
        """
        return self.session.query(Usuario).filter_by(id_usuario=id_usuario).first()

    def actualizar_usuario(
            self, id_usuario, nombre_usuario=None,
            correo_electronico=None, contrasena=None
    ):
        """
        Actualiza los datos de un usuario dado.

        Args:
            id_usuario (int): ID del usuario a actualizar.
            nombre_usuario (str, optional): Nuevo nombre de usuario.
            correo_electronico (str, optional): Nuevo correo electrónico.
            contrasena (str, optional): Nueva contraseña.

        Returns:
            Usuario: Instancia actualizada si la operación fue exitosa.
            None: Si el usuario no se encuentra o ocurre un error.
        """
        usuario = self.obtener_usuario_por_id(id_usuario)
        if not usuario:
            print("Usuario no encontrado.")
            return None
        if nombre_usuario:
            usuario.nombre_usuario = nombre_usuario
        if correo_electronico:
            usuario.correo_electronico = correo_electronico
        if contrasena:
            usuario.contrasena = contrasena
        try:
            self.session.commit()
            return usuario
        except IntegrityError:
            self.session.rollback()
            print("Error: Datos duplicados o inválidos al actualizar.")
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al actualizar: {e}")
            return None

    def eliminar_usuario(self, id_usuario):
        """
        Elimina un usuario por su ID.

        Args:
            id_usuario (int): ID del usuario a eliminar.

        Returns:
            Usuario: Instancia eliminada si la operación fue exitosa.
            None: Si el usuario no existe o ocurre un error.
        """
        usuario = self.obtener_usuario_por_id(id_usuario)
        if not usuario:
            print("Usuario no encontrado para eliminar.")
            return None
        try:
            self.session.delete(usuario)
            self.session.commit()
            return usuario
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inesperado al eliminar: {e}")
            return None
