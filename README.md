# Proyecto de fin de curso ToDoList - Sistema de escritorio

Este proyecto es un sistema de escritorio para la gestión de tareas (ToDoList) desarrollada con **Python** y **SQLAlchemy**. 
Permite a los usuarios registrar, editar, eliminar y marcar tareas como completadas. 
También gestiona usuarios, etiquetas y recordatorios.

**Características principales:**
- Creación, edición y eliminación de tareas.
- Gestión de usuarios y etiquetas para personalizar las tareas.
- Recordatorios asociados a tareas para mejorar la productividad.
- Base de datos local (`tasks.db`) para almacenar la información de forma segura.

Este proyecto refleja las buenas prácticas de programación y busca ser una herramienta intuitiva 
y útil para el manejo eficiente de actividades.

##Estructura del proyecto
```
ToDoList/
├── src/
│ ├── logica/
│ │ ├── estado_manager.py
│ │ ├── etiqueta_manager.py
│ │ ├── recordatorio_manager.py
│ │ ├── tarea_manager.py
│ │ ├── usuario_manager.py
│ │ ├── modelo/
│ │ │ ├── database.py
│ │ │ ├── declarative_base.py
│ │ │ ├── modelo.py
│ │ └── init.py
│ ├── utilidades/
│ │ ├── inicializador_estado_datos.py
│ │ ├── inicializador_etiqueta.py
│ │ ├── inicializador_recordatorio.py
│ │ ├── inicializar_tareas.py
│ │ ├── utilidades_usuarios.py
│ │ └── init.py
│ ├── vista/
│ │ ├── componentes.py
│ │ ├── ventana_agregar.py
│ │ ├── ventana_principal.py
│ │ └── init.py
│ └── tests/
│ ├── test_estado_manager.py
│ ├── test_etiqueta_manager.py
│ ├── test_recordatorio_manager.py
│ ├── test_tarea_manager.py
│ ├── test_usuario_manager.py
│ └── init.py
├── app.py
├── gui.py
├── main.py
├── requirements.txt
├── .gitignore
└── tasks.db
```
## Requisitos

- Python 3.10 o superior.
- Entorno virtual (recomendado).
- DB Browser para SQLite
- Paquetes necesarios:
  - SQLAlchemy
  - Otros paquetes especificados en `requirements.txt`.

## Instalación

- Clonar el repositorio:
  git clone [https://github.com/Nela1901/ToDoList]
  cd ToDoList
- Crear y activar un entorno virtual
- Instalar deprendencias pip install -r requerements.txt

## Ejemplo de uso
- Agregar tareas
  ```
  from src.logica.tarea_manager import TareaManager
  gestor_tareas = TareaManager()
  gestor_tareas.crear_tarea("Hacer compras", "Comprar leche y pan", "2025-06-10")
  ```
## Ramas
   Actualmente el repositorio usa como rama principal a main. Posteriormente se empleará ramas para la parte de las interfaces y luego fusionarlas mediante pull requests.
   
## Integrantes del Proyecto

| N° | Nombre completo                           |
|----|-------------------------------------------|
| 1  | Espinoza Tiza Yago Imanol                |
| 2  | Flores Torres Jhanpool                   |
| 3  | Guerra Lozano Keen                       |
| 4  | Inciso Aguilar Elizabeth Antonela        |
| 5  | Uscuvilca Ramos Abraham Luis             |
