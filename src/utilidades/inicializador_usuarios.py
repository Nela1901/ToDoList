"""
Módulo de utilidades para la gestión inicial y limpieza de usuarios en el sistema ToDoList.

Contiene funciones para inicializar usuarios sin duplicados y eliminar usuarios
duplicados basados en el correo electrónico.

Funciones:
    inicializar_usuarios(): Crea o actualiza usuarios predeterminados sin duplicados.
    limpiar_usuarios_duplicados(): Elimina usuarios duplicados dejando uno por correo electrónico.
"""

from src.modelo.database import Session
from src.modelo.modelo import Usuario

def inicializar_usuarios():
    """
    Inicializa la tabla de usuarios con un conjunto predeterminado de usuarios.

    Si un usuario con el mismo correo electrónico ya existe, actualiza su nombre
    y contraseña. Si no existe, crea un nuevo registro.

    La función evita duplicados en base al correo electrónico.

    Después de insertar o actualizar, confirma los cambios y cierra la sesión.
    Imprime un mensaje de éxito al finalizar.
    """
    session = Session()

    usuarios_iniciales = [
        {"nombre_usuario": "Pedro actualizado", "correo_electronico": "nuevo@gmail.com", "contrasena": "xyz"},
        {"nombre_usuario": "Juan", "correo_electronico": "juan@gmail.com", "contrasena": "12345"},
        {"nombre_usuario": "Ana", "correo_electronico": "ana@gmail.com", "contrasena": "pass"}
    ]

    for usuario_data in usuarios_iniciales:
        usuario_existente = session.query(Usuario).filter_by(correo_electronico=usuario_data["correo_electronico"]).first()
        if not usuario_existente:
            nuevo_usuario = Usuario(**usuario_data)
            session.add(nuevo_usuario)
        else:
            usuario_existente.nombre_usuario = usuario_data["nombre_usuario"]
            usuario_existente.contrasena = usuario_data["contrasena"]

    session.commit()
    session.close()
    print("Usuarios inicializados sin duplicados.")

def limpiar_usuarios_duplicados():
    """
    Elimina usuarios duplicados en la tabla `usuario` basándose en el correo electrónico.

    Mantiene solo el primer registro encontrado por correo electrónico y elimina
    los duplicados posteriores.

    Después de la eliminación, confirma los cambios y cierra la sesión.
    Imprime un mensaje de éxito al finalizar.
    """
    session = Session()

    usuarios = session.query(Usuario).order_by(Usuario.id_usuario).all()
    vistos = set()

    for usuario in usuarios:
        if usuario.correo_electronico in vistos:
            session.delete(usuario)
        else:
            vistos.add(usuario.correo_electronico)

    session.commit()
    session.close()
    print("Usuarios duplicados eliminados.")

if __name__ == "__main__":
    print("1. Inicializar usuarios")
    inicializar_usuarios()

    print("\n2. Limpiar duplicados")
    limpiar_usuarios_duplicados()
