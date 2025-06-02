# src/logica/estado_manager.py

from src.modelo.modelo import Estado

class EstadoManager:
    def __init__(self, session):
        self.session = session

    def crear_estado(self, nombre_estado, descripcion=None):
        estado = Estado(
            nombre_estado=nombre_estado,
            descripcion=descripcion
        )

        self.session.add(estado)
        self.session.commit()
        return estado

    def obtener_estados(self):
        return self.session.query(Estado).all()

    def obtener_estado_por_id(self, id_estado):
        return self.session.query(Estado).filter_by(id_estado=id_estado).first()

    def actualizar_estado(self, id_estado, nombre_estado=None, descripcion=None):
        estado = self.obtener_estado_por_id(id_estado)
        if estado:
            if nombre_estado:
                estado.nombre_estado = nombre_estado
            if descripcion:
                estado.descripcion = descripcion
            self.session.commit()
        return estado

    def eliminar_estado(self, id_estado):
        estado = self.obtener_estado_por_id(id_estado)
        if estado:
            self.session.delete(estado)
            self.session.commit()
        return estado
