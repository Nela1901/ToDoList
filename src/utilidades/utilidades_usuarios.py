# utilidades/usuarios_utils.py

from src.modelo.database import Session
from src.modelo.modelo import Usuario

def inicializar_usuarios():
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
