# src/logica/etiqueta_manager.py

from src.modelo.modelo import Etiqueta

class EtiquetaManager:
    def __init__(self, session):
        self.session = session

    def crear_etiqueta(self, nombre_etiqueta, color):
        etiqueta = Etiqueta(
            nombre_etiqueta=nombre_etiqueta,
            color=color
        )
        self.session.add(etiqueta)
        self.session.commit()
        return etiqueta

    def obtener_etiquetas(self):
        return self.session.query(Etiqueta).all()

    def obtener_etiqueta_por_id(self, id_etiqueta):
        return self.session.query(Etiqueta).filter_by(id_etiqueta=id_etiqueta).first()

    def actualizar_etiqueta(self, id_etiqueta, nombre_etiqueta=None, color=None):
        etiqueta = self.obtener_etiqueta_por_id(id_etiqueta)
        if etiqueta:
            if nombre_etiqueta:
                etiqueta.nombre_etiqueta = nombre_etiqueta
            if color:
                etiqueta.color = color
            self.session.commit()
        return etiqueta

    def eliminar_etiqueta(self, id_etiqueta):
        etiqueta = self.obtener_etiqueta_por_id(id_etiqueta)
        if etiqueta:
            self.session.delete(etiqueta)
            self.session.commit()
        return etiqueta
