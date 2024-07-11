import requests
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Función para crear la base de datos y la tabla personas
def crear_base_de_datos():
    conexion = sqlite3.connect('datos_personales.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido_paterno TEXT,
            apellido_materno TEXT,
            dni TEXT,
            lugar_procedencia TEXT,
            fecha TEXT,
            hora TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para guardar personas en la base de datos
def guardar_persona(nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia):
    conexion = sqlite3.connect('datos_personales.db')
    cursor = conexion.cursor()
    fecha = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M:%S')
    cursor.execute('''
        INSERT INTO personas (nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia, fecha, hora) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia, fecha, hora))
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
                return None
        else:
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al acceder a la API: {e}")
        return None

# Función para mostrar los datos consultados y permitir guardar
def consultar_y_mostrar_datos():
    dni = dni_entry.get()
    if not dni or len(dni) != 8 or not dni.isdigit():
        messagebox.showerror("Error", "Ingrese un DNI válido de 8 dígitos.")
        return

    global datos_persona
    datos_persona = consultar_persona_por_dni(dni)
    if datos_persona:
        nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia = datos_persona
        info = f"Nombre Completo: {nombre} {apellido_paterno} {apellido_materno}\nDNI: {dni}\nLugar de Procedencia: {lugar_procedencia}"
        datos_consultados_label.config(text=info)
        boton_guardar.config(state=tk.NORMAL)  # Habilitar el botón de guardar
    else:
        datos_consultados_label.config(text="No se pudo obtener datos de la persona. Ingrese los datos manualmente.")
        abrir_formulario_manual(dni)
        boton_guardar.config(state=tk.DISABLED)  # Deshabilitar el botón de guardar

# Función para guardar los datos consultados
def guardar_datos():
    global datos_persona
    if datos_persona:
        nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia = datos_persona
        guardar_persona(nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia)
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        boton_guardar.config(state=tk.DISABLED)  # Deshabilitar el botón de guardar
        actualizar_lista_personas()
        datos_consultados_label.config(text="")

# Función para abrir el formulario manual
def abrir_formulario_manual(dni):
    formulario_window = tk.Toplevel()
    formulario_window.title("Formulario Manual")
    formulario_window.geometry("400x400")

    ttk.Label(formulario_window, text="DNI").pack(pady=5)
    dni_entry_manual = ttk.Entry(formulario_window)
    dni_entry_manual.pack(pady=5)
    dni_entry_manual.insert(0, dni)
    dni_entry_manual.config(state='disabled')

    ttk.Label(formulario_window, text="Apellido Paterno").pack(pady=5)
    apellido_paterno_entry_manual = ttk.Entry(formulario_window)
    apellido_paterno_entry_manual.pack(pady=5)

    ttk.Label(formulario_window, text="Apellido Materno").pack(pady=5)
    apellido_materno_entry_manual = ttk.Entry(formulario_window)
    apellido_materno_entry_manual.pack(pady=5)

    ttk.Label(formulario_window, text="Nombre").pack(pady=5)
    nombre_entry_manual = ttk.Entry(formulario_window)
    nombre_entry_manual.pack(pady=5)

    ttk.Label(formulario_window, text="Lugar de Procedencia").pack(pady=5)
    lugar_procedencia_entry_manual = ttk.Entry(formulario_window)
    lugar_procedencia_entry_manual.pack(pady=5)

    def guardar_datos_manual():
        nombre = nombre_entry_manual.get()
        apellido_paterno = apellido_paterno_entry_manual.get()
        apellido_materno = apellido_materno_entry_manual.get()
        lugar_procedencia = lugar_procedencia_entry_manual.get()

        if not nombre or not apellido_paterno or not apellido_materno:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        guardar_persona(nombre, apellido_paterno, apellido_materno, dni, lugar_procedencia)
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        formulario_window.destroy()
        actualizar_lista_personas()

    ttk.Button(formulario_window, text="Guardar", command=guardar_datos_manual).pack(pady=20)

# Función para actualizar la lista de personas guardadas
def actualizar_lista_personas():
    personas = obtener_personas()
    lista_personas.delete(0, tk.END)
    if personas:
        for persona in personas:
            info = f"ID: {persona[0]} - {persona[1]} {persona[2]} {persona[3]}, DNI: {persona[4]}, {persona[5]}, {persona[6]}, {persona[7]}"
            lista_personas.insert(tk.END, info)
    else:
        lista_personas.insert(tk.END, "No hay personas guardadas.")

# Función para mostrar la pantalla de administrador
def mostrar_pantalla_administrador():
    def cargar_datos():
        messagebox.showinfo("Cargar Datos", "Función de cargar datos no implementada.")

    def generar_reporte(tipo):
        messagebox.showinfo(f"Reporte {tipo}", f"Generar reporte {tipo} no implementado.")

    admin_window = tk.Toplevel()
    admin_window.title("Administrador")
    admin_window.geometry("500x400")

    menubar = tk.Menu(admin_window)
    report_menu = tk.Menu(menubar, tearoff=0)
    report_menu.add_command(label="Reportes Diarios", command=lambda: generar_reporte("diario"))
    report_menu.add_command(label="Reportes Semanales", command=lambda: generar_reporte("semanal"))
    report_menu.add_command(label="Reportes Mensuales", command=lambda: generar_reporte("mensual"))
    menubar.add_cascade(label="Reportes", menu=report_menu)
    menubar.add_command(label="Cargar Datos", command=cargar_datos)
    menubar.add_command(label="Salir", command=admin_window.destroy)
    admin_window.config(menu=menubar)

# Función para validar el login del administrador
def validar_login(usuario, contrasena):
    if usuario == "yorchflrs" and contrasena == "george777":
        mostrar_pantalla_administrador()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Función para mostrar la pantalla de login del administrador
def mostrar_login_administrador():
    login_window = tk.Toplevel()
    login_window.title("Login Administrador")
    login_window.geometry("300x200")

    ttk.Label(login_window, text="Usuario").pack(pady=5)
    usuario_entry = ttk.Entry(login_window)
    usuario_entry.pack(pady=5)

    ttk.Label(login_window, text="Contraseña").pack(pady=5)
    contrasena_entry = ttk.Entry(login_window, show="*")
    contrasena_entry.pack(pady=5)

    ttk.Button(login_window, text="Login", command=lambda: validar_login(usuario_entry.get(), contrasena_entry.get())).pack(pady=20)

# Función para mostrar la pantalla de registro de asistencia
def mostrar_pantalla_registro_asistencia():
    global boton_guardar, dni_entry, datos_consultados_label, lista_personas

    root = tk.Toplevel()
    root.title("Registro de Asistencia")
    root.geometry("600x600")

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 12), padding=10)

    ttk.Label(root, text="Registro de Asistencia", font=("Helvetica", 16)).pack(pady=10)

    frame_dni = ttk.Frame(root)
    frame_dni.pack(pady=5)
    ttk.Label(frame_dni, text="DNI").pack(side=tk.LEFT, padx=5)
    dni_entry = ttk.Entry(frame_dni)
    dni_entry.pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_dni, text="Buscar", command=consultar_y_mostrar_datos).pack(side=tk.LEFT, padx=5)

    datos_consultados_label = ttk.Label(root, text="", font=("Helvetica", 12))
    datos_consultados_label.pack(pady=10)

    boton_guardar = ttk.Button(root, text="Registrar", command=guardar_datos, state=tk.DISABLED)
    boton_guardar.pack(fill=tk.X, padx=20, pady=10)
    ttk.Button(root, text="Mostrar Personas Guardadas", command=actualizar_lista_personas).pack(fill=tk.X, padx=20, pady=10)

    lista_personas = tk.Listbox(root, height=10, font=("Helvetica", 12))
    lista_personas.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
    actualizar_lista_personas()

    ttk.Button(root, text="Salir", command=root.destroy).pack(fill=tk.X, padx=20, pady=10)

# Función para la pantalla inicial
def pantalla_inicial():
    root = tk.Tk()
    root.title("Sistema de Registro de Asistencia")
    root.geometry("400x300")

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 12), padding=10)

    ttk.Label(root, text="Sistema de Registro de Asistencia", font=("Helvetica", 16)).pack(pady=20)

    ttk.Button(root, text="Administrador", command=mostrar_login_administrador).pack(fill=tk.X, padx=20, pady=10)
    ttk.Button(root, text="Registro de Asistencia", command=mostrar_pantalla_registro_asistencia).pack(fill=tk.X, padx=20, pady=10)
    ttk.Button(root, text="Salir", command=root.destroy).pack(fill=tk.X, padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    crear_base_de_datos()
    pantalla_inicial()
