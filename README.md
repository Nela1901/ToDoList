# Proyecto de fin de curso ToDoList - Sistema de escritorio

Este proyecto es un sistema de escritorio para la gestión de tareas (ToDoList) desarrollada con **Python** y **SQLAlchemy**. 
Permite a los usuarios registrar, editar, eliminar y marcar tareas como completadas. 
También gestiona usuarios, etiquetas y recordatorios.

**Características principales:**
- Creación, edición y eliminación de tareas.
- Gestión de usuarios y etiquetas para personalizar las tareas.
- Recordatorios asociados a tareas para mejorar la productividad.
- Base de datos local ('tasks.db') para almacenar la información de forma segura.

Este proyecto refleja las buenas prácticas de programación y busca ser una herramienta intuitiva 
y útil para el manejo eficiente de actividades.

## Requisitos

- Python 3.10 o superior.
- Entorno virtual (recomendado).
- Paquetes necesarios:
  - SQLAlchemy
  - sqlite3 (base de datos incluida en Python)
  - Otros paquetes especificados en `requirements.txt`.

## Instalación

Clonar el repositorio:
[https://github.com/Nela1901/ToDoList]

## Estructura del Proyecto
ToDoList/
│
├── src/
│ ├── logica
│ │ ├── init.py
│ │ ├── estado_manager.py
│ │ ├── etiqueta_manager.py
│ │ ├── recordatorio_manager.py
│ │ ├── tarea_manager.py
│ │ ├── usuario_manager.py
│ │ └── modelo/ # Modelos y configuración de base de datos
│ │ ├── init.py
│ │ ├── database.py
│ │ ├── declarative_base.py
│ │ └── modelo.py
│ │
│ ├── utilidades/ # Scripts de inicialización y utilidades
│ │ ├── init.py
│ │ ├── inicializador_estado_datos.py
│ │ ├── inicializador_etiqueta.py
│ │ ├── inicializador_recordatorio.py
│ │ ├── inicializar_tareas.py
│ │ └── utilidades_usuarios.py
│ │
│ ├── vista/ # Código para la interfaz gráfica
│ │ ├── init.py
│ │ ├── componentes.py
│ │ ├── ventana_agregar.py
│ │ └── ventana_principal.py
│
├── tests/ # Pruebas unitarias
│ ├── init.py
│ ├── test_estado_manager.py
│ ├── test_etiqueta_manager.py
│ ├── test_recordatorio_manager.py
│ ├── test_tarea_manager.py
│ └── test_usuario_manager.py
│
├── .gitignore # Archivos y carpetas a ignorar por Git
├── app.py # Entrada principal de la aplicación
├── gui.py # Código de GUI (si aplica)
├── main.py # Archivo principal del proyecto
├── requirements.txt # Requisitos del proyecto
├── tasks.db # Base de datos SQLite
└── README.md # Este archivo

## Integrantes del Proyecto

| N° | Nombre completo                           |
|----|-------------------------------------------|
| 1  | Espinoza Tiza Yago Imanol                |
| 2  | Flores Torres Jhanpool                   |
| 3  | Guerra Lozano Keen                       |
| 4  | Inciso Aguilar Elizabeth Antonela        |
| 5  | Uscuvilca Ramos Abraham Luis             |
