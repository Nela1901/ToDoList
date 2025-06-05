"""
Script para inicializar los datos básicos en la base de datos del sistema ToDoList.

Este módulo importa y ejecuta los scripts de inicialización de usuarios,
estados, etiquetas, tareas y recordatorios para poblar la base de datos
con datos predeterminados.

Uso:
    Ejecutar directamente este script para crear tablas (si no existen)
    y llenar la base de datos con datos iniciales.

Ejemplo:
    python src/utilidades/inicializar_todo.py
"""

import src.utilidades.inicializador_usuarios as usuario
import src.utilidades.inicializador_estados as estado
import src.utilidades.inicializador_etiqueta as etiqueta
import src.utilidades.inicializador_tareas as tarea
import src.utilidades.inicializador_recordatorio as recordatorio

def main():
    """
    Ejecuta la inicialización de usuarios, estados, etiquetas, tareas y recordatorios.
    """
    print("Creando las tablas y llenando datos iniciales...")

    usuario.inicializar_usuarios()
    estado.inicializar_estados()
    etiqueta.inicializar_etiquetas()
    tarea.inicializar_tareas()
    recordatorio.inicializar_recordatorios()

    print("¡Base de datos lista y con datos iniciales!")

if __name__ == "__main__":
    main()
