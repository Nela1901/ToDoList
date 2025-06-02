import tkinter as tk
from tkinter import messagebox
from src.modelo import database


def refrescar_lista():
    lista.delete(0, tk.END)
    for tarea in database.get_tasks():
        lista.insert(tk.END, f"{tarea[0]} - {tarea[1]}")  # Muestra: ID - Título

def agregar_tarea():
    titulo = entrada_titulo.get()
    descripcion = entrada_descripcion.get()
    if titulo:
        try:
            database.insert_task(titulo, descripcion)
            entrada_titulo.delete(0, tk.END)
            entrada_descripcion.delete(0, tk.END)
            refrescar_lista()
        except:
            messagebox.showerror("Error", "El título ya existe.")
    else:
        messagebox.showwarning("Advertencia", "El título es obligatorio.")

def eliminar_tarea():
    try:
        seleccionada = lista.get(lista.curselection())
        id_tarea = int(seleccionada.split(" - ")[0])
        database.delete_task(id_tarea)
        refrescar_lista()
    except:
        messagebox.showerror("Error", "Selecciona una tarea para eliminar.")

def completar_tarea():
    try:
        seleccionada = lista.get(lista.curselection())
        id_tarea = int(seleccionada.split(" - ")[0])
        database.complete_task(id_tarea)
        refrescar_lista()
    except:
        messagebox.showerror("Error", "Selecciona una tarea para marcar como completada.")


ventana = tk.Tk()
ventana.title("ToDo List")

tk.Label(ventana, text="Título").pack()
entrada_titulo = tk.Entry(ventana, width=40)
entrada_titulo.pack()

tk.Label(ventana, text="Descripción").pack()
entrada_descripcion = tk.Entry(ventana, width=40)
entrada_descripcion.pack()

tk.Button(ventana, text="Agregar tarea", command=agregar_tarea).pack(pady=3)
tk.Button(ventana, text="Eliminar tarea", command=eliminar_tarea).pack(pady=3)
tk.Button(ventana, text="Marcar como completada", command=completar_tarea).pack(pady=3)

lista = tk.Listbox(ventana, width=60)
lista.pack(pady=10)

database.init_db()
refrescar_lista()
ventana.mainloop()
