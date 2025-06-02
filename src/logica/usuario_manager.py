# src/logica/usuario_manager.py

from src.modelo.modelo import Usuario

class UsuarioManager:
    def __init__(self, session):
        self.session = session

    def crear_usuario(self, nombre_usuario, correo_electronico, contrasena):
        usuario = Usuario(
            nombre_usuario = nombre_usuario,
            correo_electronico = correo_electronico,
            contrasena = contrasena
        )
        self.session.add(usuario)
        self.session.commit()
        return usuario

    def obtener_usuarios(self):
        return self.session.query(Usuario).all()

    def obtener_usuario_por_id(self, id_usuario):
        return self.session.query(Usuario).filter_by(id_usuario=id_usuario).first()

    def actualizar_usuario(self, id_usuario, nombre_usuario=None, correo_electronico=None, contrasena=None):
        usuario = self.obtener_usuario_por_id(id_usuario)
        if usuario:
            if nombre_usuario:
                usuario.nombre_usuario = nombre_usuario
            if correo_electronico:
                usuario.correo_electronico = correo_electronico
            if contrasena:
                usuario.contrasena = contrasena
            self.session.commit()
        return usuario

    def eliminar_usuario(self, id_usuario):
        usuario = self.obtener_usuario_por_id(id_usuario)
        if usuario:
            self.session.delete(usuario)
            self.session.commit()
        return usuario
