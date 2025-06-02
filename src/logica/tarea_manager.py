# src/logica/tarea_manager.py

from src.modelo.modelo import Tarea

class TareaManager:
    def __init__(self, session):
        self.session = session

    def crear_tarea(self, titulo, descripcion, fecha_creacion, fecha_vencimiento, id_usuario, id_estado):
        tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_creacion=fecha_creacion,
            fecha_vencimiento=fecha_vencimiento,
            id_usuario=id_usuario,
            id_estado=id_estado
        )
        self.session.add(tarea)
        self.session.commit()
        return tarea

    def obtener_tareas(self):
        return self.session.query(Tarea).all()

    def obtener_tarea_por_id(self, id_tarea):
        return self.session.query(Tarea).filter_by(id_tarea=id_tarea).first()

    def actualizar_tarea(self, id_tarea, titulo=None, descripcion=None, fecha_vencimiento=None, id_estado=None):
        tarea = self.obtener_tarea_por_id(id_tarea)
        if tarea:
            if titulo:
                tarea.titulo = titulo
            if descripcion:
                tarea.descripcion = descripcion
            if fecha_vencimiento:
                tarea.fecha_vencimiento = fecha_vencimiento
            if id_estado:
                tarea.id_estado = id_estado
            self.session.commit()
        return tarea

    def eliminar_tarea(self, id_tarea):
        tarea = self.obtener_tarea_por_id(id_tarea)
        if tarea:
            self.session.delete(tarea)
            self.session.commit()
        return tarea
