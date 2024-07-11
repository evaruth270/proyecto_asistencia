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
            apellido_paterno TEXT,
            apellido_materno TEXT,
            dni TEXT,
            lugar_procedencia TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para guardar personas en la base de datos
def guardar_persona(nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia):
    conexion = sqlite3.connect('datos_personales.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO personas (nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia) VALUES (?, ?, ?, ?, ?)
    ''', (nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia))
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

# Función para consultar datos de la API de apis.net.pe
def consultar_persona_por_dni(dni):
    url = f"https://api.apis.net.pe/v1/dni?numero={dni}"
    headers = {
        'Authorization': 'Bearer TU_TOKEN_DE_ACCESO'  # Reemplaza 'TU_TOKEN_DE_ACCESO' con tu token real
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'nombre' in data and 'apellidoPaterno' in data and 'apellidoMaterno' in data:
                nombre = data['nombre']
                apellido_paterno = data['apellidoPaterno']
                apellido_materno = data['apellidoMaterno']
                lugar_procedencia = data.get('departamento', 'No disponible')  # Si la API proporciona esta información
                return (nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia)
            else:
                messagebox.showerror("Error", "Datos incompletos recibidos de la API.")
                return None
        else:
            messagebox.showerror("Error", f"Error en la consulta. Código de estado: {response.status_code}")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al acceder a la API: {e}")
        return None

# Función para mostrar los datos consultados y permitir guardar
def consultar_y_mostrar_datos():
    dni = simpledialog.askstring("Buscar Persona", "Ingrese el DNI:")
    if not dni or len(dni) != 8 or not dni.isdigit():
        messagebox.showerror("Error", "Ingrese un DNI válido de 8 dígitos.")
        return

    global datos_persona
    datos_persona = consultar_persona_por_dni(dni)
    if datos_persona:
        nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia = datos_persona
        info = f"Nombre Completo: {nombre} {apellido_paterno} {apellido_materno}\nDNI: {dni}\nLugar de Procedencia: {lugar_procedencia}"
        messagebox.showinfo("Datos Consultados", info)
        boton_guardar.config(state=tk.NORMAL)  # Habilitar el botón de guardar
    else:
        messagebox.showerror("Error", "No se pudo obtener datos de la persona.")

# Función para guardar los datos consultados
def guardar_datos():
    global datos_persona
    if datos_persona:
        nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia = datos_persona
        guardar_persona(nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia)
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        boton_guardar.config(state=tk.DISABLED)  # Deshabilitar el botón de guardar

# Función para mostrar los datos guardados
def mostrar_datos_guardados():
    personas = obtener_personas()
    if personas:
        info = ""
        for persona in personas:
            info += f"ID: {persona[0]}\nNombre: {persona[1]} {persona[2]} {persona[3]}\nDNI: {persona[4]}\nLugar de Procedencia: {persona[5]}\n\n"
        messagebox.showinfo("Personas Guardadas", info)
    else:
        messagebox.showerror("Error", "No hay personas guardadas en la base de datos.")

# Función para la interfaz gráfica de usuario
def gui():
    global boton_guardar

    root = tk.Tk()
    root.title("Gestión de Personas Globales")
    root.geometry("500x400")

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 12), padding=10)

    ttk.Label(root, text="Gestión de Personas Globales", font=("Helvetica", 16)).pack(pady=10)

    ttk.Button(root, text="Consultar Persona por DNI", command=consultar_y_mostrar_datos).pack(fill=tk.X, padx=20, pady=10)
    boton_guardar = ttk.Button(root, text="Guardar Datos", command=guardar_datos, state=tk.DISABLED)
    boton_guardar.pack(fill=tk.X, padx=20, pady=10)
    ttk.Button(root, text="Mostrar Personas Guardadas", command=mostrar_datos_guardados).pack(fill=tk.X, padx=20, pady=10)
    ttk.Button(root, text="Salir", command=root.destroy).pack(fill=tk.X, padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    crear_base_de_datos()
    gui()
