# src/logica/recordatorio_manager.py

from src.modelo.modelo import Recordatorio

class RecordatorioManager:
    def __init__(self, session):
        self.session = session

    def crear_recordatorio(self, id_tarea, fecha_hora, tipo):
        recordatorio = Recordatorio(
            id_tarea=id_tarea,
            fecha_hora=fecha_hora,
            tipo=tipo
        )
        self.session.add(recordatorio)
        self.session.commit()
        return recordatorio

    def obtener_recordatorios(self):
        return self.session.query(Recordatorio).all()

    def obtener_recordatorio_por_id(self, id_recordatorio):
        return self.session.query(Recordatorio).filter_by(id_recordatorio=id_recordatorio).first()

    def actualizar_recordatorio(self, id_recordatorio, fecha_hora=None, tipo=None):
        recordatorio = self.obtener_recordatorio_por_id(id_recordatorio)
        if recordatorio:
            if fecha_hora:
                recordatorio.fecha_hora = fecha_hora
            if tipo:
                recordatorio.tipo = tipo
            self.session.commit()
        return recordatorio

    def eliminar_recordatorio(self, id_recordatorio):
        recordatorio = self.obtener_recordatorio_por_id(id_recordatorio)
        if recordatorio:
            self.session.delete(recordatorio)
            self.session.commit()
        return recordatorio
