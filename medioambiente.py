import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Conectar a la base de datos
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ministerio'
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")
        return None

connection = connect_to_database()

# Funciones CRUD
def agregar_objeto():
    cursor = connection.cursor()
    id = entry_id.get()
    nombre = entry_nombre.get()
    habitat = entry_habitat.get()
    estado = entry_estado.get()
    region = entry_region.get()
    query = "INSERT INTO FaunaFlora (ID, NombreCientifico, Habitat, EstadoConservacion, RegionGeografica) VALUES (%s, %s, %s, %s, %s)"
    values = (id, nombre, habitat, estado, region)
    cursor.execute(query, values)
    connection.commit()
    messagebox.showinfo("Éxito", "Objeto agregado exitosamente")
    cursor.close()

def mostrar_lista():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM FaunaFlora")
    registros = cursor.fetchall()
    listbox.delete(0, tk.END)
    for registro in registros:
        listbox.insert(tk.END, registro)
    cursor.close()

def eliminar_objeto():
    cursor = connection.cursor()
    seleccionado = listbox.curselection()
    if seleccionado:
        id = listbox.get(seleccionado)[0]
        query = "DELETE FROM FaunaFlora WHERE ID = %s"
        cursor.execute(query, (id,))
        connection.commit()
        messagebox.showinfo("Éxito", "Objeto eliminado exitosamente")
        mostrar_lista()
    cursor.close()

def actualizar_objeto():
    cursor = connection.cursor()
    id = entry_id.get()
    nombre = entry_nombre.get()
    habitat = entry_habitat.get()
    estado = entry_estado.get()
    region = entry_region.get()
    query = "UPDATE FaunaFlora SET NombreCientifico = %s, Habitat = %s, EstadoConservacion = %s, RegionGeografica = %s WHERE ID = %s"
    values = (nombre, habitat, estado, region, id)
    cursor.execute(query, values)
    connection.commit()
    messagebox.showinfo("Éxito", "Objeto actualizado exitosamente")
    mostrar_lista()
    cursor.close()

def cargar_objeto():
    seleccionado = listbox.curselection()
    if seleccionado:
        id, nombre, habitat, estado, region = listbox.get(seleccionado)
        entry_id.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_habitat.delete(0, tk.END)
        entry_estado.delete(0, tk.END)
        entry_region.delete(0, tk.END)
        entry_id.insert(0, id)
        entry_nombre.insert(0, nombre)
        entry_habitat.insert(0, habitat)
        entry_estado.insert(0, estado)
        entry_region.insert(0, region)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Gestión de Fauna y Flora")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="ID").grid(row=0, column=0)
entry_id = tk.Entry(frame)
entry_id.grid(row=0, column=1)

tk.Label(frame, text="Nombre Científico").grid(row=1, column=0)
entry_nombre = tk.Entry(frame)
entry_nombre.grid(row=1, column=1)

tk.Label(frame, text="Habitat").grid(row=2, column=0)
entry_habitat = tk.Entry(frame)
entry_habitat.grid(row=2, column=1)

tk.Label(frame, text="Estado de Conservación").grid(row=3, column=0)
entry_estado = tk.Entry(frame)
entry_estado.grid(row=3, column=1)

tk.Label(frame, text="Región Geográfica").grid(row=4, column=0)
entry_region = tk.Entry(frame)
entry_region.grid(row=4, column=1)

tk.Button(frame, text="Agregar", command=agregar_objeto).grid(row=5, column=0, pady=5)
tk.Button(frame, text="Mostrar", command=mostrar_lista).grid(row=5, column=1, pady=5)
tk.Button(frame, text="Eliminar", command=eliminar_objeto).grid(row=6, column=0, pady=5)
tk.Button(frame, text="Actualizar", command=actualizar_objeto).grid(row=6, column=1, pady=5)
tk.Button(frame, text="Cargar", command=cargar_objeto).grid(row=7, column=0, pady=5)

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

root.mainloop()

# Cerrar la conexión a la base de datos al salir de la aplicación
if connection.is_connected():
    connection.close()
