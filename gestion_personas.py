import requests
import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

# Función para crear la base de datos y la tabla personas
def crear_base_de_datos():
    conexion = sqlite3.connect('datos_personales.db')
    cursor = conexion.cursor()
    cursor.execute('DROP TABLE IF EXISTS personas')
    cursor.execute('''
        CREATE TABLE personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            email TEXT,
            pais TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para guardar personas en la base de datos
def guardar_persona(nombre, apellido, email, pais):
    conexion = sqlite3.connect('datos_personales.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO personas (nombre, apellido, email, pais) VALUES (?, ?, ?, ?)
    ''', (nombre, apellido, email, pais))
    conexion.commit()
    conexion.close()

# Función para buscar personas en la base de datos
def obtener_personas():
    conexion = sqlite3.connect('datos_personales.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM personas')
    personas = cursor.fetchall()
    conexion.close()
    return personas

# Función para consultar datos de la API de Random User
def consultar_persona_global():
    url = "https://randomuser.me/api/"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            user = data['results'][0]
            nombre = user['name']['first']
            apellido = user['name']['last']
            email = user['email']
            pais = user['location']['country']
            return (nombre, apellido, email, pais)
        else:
            return None
    except Exception as e:
        print(f"Error al acceder a la API: {e}")
        return None

# Función para mostrar los datos consultados y permitir guardar
def consultar_y_mostrar_datos():
    global datos_persona
    datos_persona = consultar_persona_global()
    if datos_persona:
        nombre, apellido, email, pais = datos_persona
        info = f"Nombre: {nombre} {apellido}\nEmail: {email}\nPaís: {pais}"
        messagebox.showinfo("Datos Consultados", info)
        boton_guardar.config(state=tk.NORMAL)  # Habilitar el botón de guardar
    else:
        messagebox.showerror("Error", "No se pudo obtener datos de la persona.")

# Función para guardar los datos consultados
def guardar_datos():
    global datos_persona
    if datos_persona:
        nombre, apellido, email, pais = datos_persona
        guardar_persona(nombre, apellido, email, pais)
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        boton_guardar.config(state=tk.DISABLED)  # Deshabilitar el botón de guardar

# Función para mostrar los datos guardados
def mostrar_datos_guardados():
    personas = obtener_personas()
    if personas:
        info = ""
        for persona in personas:
            info += f"ID: {persona[0]}\nNombre: {persona[1]} {persona[2]}\nEmail: {persona[3]}\nPaís: {persona[4]}\n\n"
        messagebox.showinfo("Personas Guardadas", info)
    else:
        messagebox.showerror("Error", "No hay personas guardadas en la base de datos.")

# Función para la interfaz gráfica de usuario
def gui():
    global boton_guardar

    root = tk.Tk()
    root.title("Gestión de Personas Globales")
    root.geometry("400x300")

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 12), padding=10)

    ttk.Label(root, text="Gestión de Personas Globales", font=("Helvetica", 16)).pack(pady=10)

    ttk.Button(root, text="Consultar Persona Global", command=consultar_y_mostrar_datos).pack(fill=tk.X, padx=20, pady=10)
    boton_guardar = ttk.Button(root, text="Guardar Datos", command=guardar_datos, state=tk.DISABLED)
    boton_guardar.pack(fill=tk.X, padx=20, pady=10)
    ttk.Button(root, text="Mostrar Personas Guardadas", command=mostrar_datos_guardados).pack(fill=tk.X, padx=20, pady=10)
    ttk.Button(root, text="Salir", command=root.destroy).pack(fill=tk.X, padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    crear_base_de_datos()
    gui()
