import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # Necesita instalar Pillow
import pyrebase
import firebase_admin
from firebase_admin import credentials, db, auth as admin_auth

# -------------------- Firebase Configuración --------------------
firebase_config = {
    "apiKey": "AIzaSyDWPdr2ADEeZYDfk58TgFLfAr5XfqRY_Xo",
    "authDomain": "stockmarket-e92e2.firebaseapp.com",
    "databaseURL": "https://stockmarket-e92e2-default-rtdb.firebaseio.com/",
    "projectId": "stockmarket-e92e2",
    "storageBucket": "stockmarket-e92e2.appspot.com",
    "messagingSenderId": "156560897736",
    "appId": "1:156560897736:web:7ac36bae494b4b8bc1dc7d",
    "measurementId": "G-2RCVXNKBBZN"
}

firebase = pyrebase.initialize_app(firebase_config)
pyre_auth = firebase.auth()

cred = credentials.Certificate("stockmarket-testbase.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": firebase_config["databaseURL"]
    })

# -------------------- Funciones --------------------
def crear_usuario():
    email = email_var.get()
    password = pass_var.get()
    nombre = nombre_var.get()

    try:
        user = pyre_auth.create_user_with_email_and_password(email, password)
        uid = user['localId']
        db.reference(f'usuarios/{uid}').set({"email": email, "perfil": nombre})
        messagebox.showinfo("Éxito", f"Usuario {nombre} creado.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el usuario:\n{e}")

def autenticar_usuario():
    email = email_var.get()
    password = pass_var.get()
    try:
        user = pyre_auth.sign_in_with_email_and_password(email, password)
        uid = user['localId']
        datos = db.reference(f'usuarios/{uid}').get()
        abrir_interfaz_usuario(uid, datos['perfil'])  # 🔄 Aquí se abre la interfaz personalizada
    except Exception as e:
        messagebox.showerror("Error", f"Credenciales incorrectas:\n{e}")

def actualizar_usuario():
    email = email_var.get()
    password = pass_var.get()
    nuevo_nombre = nombre_var.get()
    try:
        user = pyre_auth.sign_in_with_email_and_password(email, password)
        uid = user['localId']
        db.reference(f'usuarios/{uid}/perfil').set(nuevo_nombre)
        messagebox.showinfo("Actualizado", "Nombre actualizado.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")

def eliminar_usuario():
    email = email_var.get()
    password = pass_var.get()
    try:
        user = pyre_auth.sign_in_with_email_and_password(email, password)
        uid = user['localId']
        admin_auth.delete_user(uid)
        db.reference(f'usuarios/{uid}').delete()
        messagebox.showinfo("Eliminado", f"Usuario {email} eliminado.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

def limpiar_campos():
    email_var.set("")
    pass_var.set("")
    nombre_var.set("")

def abrir_interfaz_usuario(uid, perfil):
    ventana_usuario = tk.Toplevel(root)
    ventana_usuario.title(f"Panel de {perfil}")
    ventana_usuario.geometry("550x650")
    ventana_usuario.configure(bg="#ffffff")

    tk.Label(ventana_usuario, text=f"Bienvenido, {perfil}", font=("Helvetica", 14, "bold"), bg="#ffffff").pack(pady=10)

    productos_frame = tk.Frame(ventana_usuario, bg="#ffffff")
    productos_frame.pack(pady=10)

    # Variables del producto
    nombre_var = tk.StringVar()
    descripcion_var = tk.StringVar()
    cantidad_var = tk.StringVar()
    precio_var = tk.StringVar()

    # Campos de entrada
    tk.Label(productos_frame, text="Nombre del producto:", bg="#ffffff").grid(row=0, column=0, sticky="w")
    tk.Entry(productos_frame, textvariable=nombre_var, width=30).grid(row=0, column=1)

    tk.Label(productos_frame, text="Descripción:", bg="#ffffff").grid(row=1, column=0, sticky="w")
    tk.Entry(productos_frame, textvariable=descripcion_var, width=30).grid(row=1, column=1)

    tk.Label(productos_frame, text="Cantidad:", bg="#ffffff").grid(row=2, column=0, sticky="w")
    tk.Entry(productos_frame, textvariable=cantidad_var, width=30).grid(row=2, column=1)

    tk.Label(productos_frame, text="Precio:", bg="#ffffff").grid(row=3, column=0, sticky="w")
    tk.Entry(productos_frame, textvariable=precio_var, width=30).grid(row=3, column=1)

    # Lista de productos
    lista = tk.Listbox(ventana_usuario, width=70)
    lista.pack(pady=20)

    claves_productos = []

    def cargar_productos():
        lista.delete(0, tk.END)
        nonlocal claves_productos
        claves_productos = []
        ref = db.reference(f'usuarios/{uid}/productos')
        datos = ref.get()
        if datos:
            for clave, info in datos.items():
                texto = f"{info['nombre']} | {info.get('descripcion', '')} | Cantidad: {info.get('cantidad', '')} | Precio: ${info.get('precio', 0)}"
                lista.insert(tk.END, texto)
                claves_productos.append(clave)

    def agregar_producto():
        nombre = nombre_var.get()
        descripcion = descripcion_var.get()
        cantidad = cantidad_var.get()
        precio = precio_var.get()
        if nombre and cantidad.isdigit() and precio.replace('.', '', 1).isdigit():
            ref = db.reference(f'usuarios/{uid}/productos')
            ref.push({
                "nombre": nombre,
                "descripcion": descripcion,
                "cantidad": int(cantidad),
                "precio": float(precio)
            })
            limpiar_campos_producto()
            cargar_productos()
        else:
            messagebox.showwarning("Entrada inválida", "Revisa que cantidad y precio sean números válidos.")

    def eliminar_producto():
        seleccion = lista.curselection()
        if seleccion:
            clave = claves_productos[seleccion[0]]
            db.reference(f'usuarios/{uid}/productos/{clave}').delete()
            cargar_productos()
            limpiar_campos_producto()

    def editar_producto():
        seleccion = lista.curselection()
        if seleccion:
            clave = claves_productos[seleccion[0]]
            nombre = nombre_var.get()
            descripcion = descripcion_var.get()
            cantidad = cantidad_var.get()
            precio = precio_var.get()
            if nombre and cantidad.isdigit() and precio.replace('.', '', 1).isdigit():
                db.reference(f'usuarios/{uid}/productos/{clave}').update({
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "cantidad": int(cantidad),
                    "precio": float(precio)
                })
                cargar_productos()
                limpiar_campos_producto()
            else:
                messagebox.showwarning("Error", "Verifica que los datos sean correctos.")

    def rellenar_campos_para_edicion(event):
        seleccion = lista.curselection()
        if seleccion:
            clave = claves_productos[seleccion[0]]
            datos = db.reference(f'usuarios/{uid}/productos/{clave}').get()
            nombre_var.set(datos.get("nombre", ""))
            descripcion_var.set(datos.get("descripcion", ""))
            cantidad_var.set(str(datos.get("cantidad", "")))
            precio_var.set(str(datos.get("precio", "")))

    def limpiar_campos_producto():
        nombre_var.set("")
        descripcion_var.set("")
        cantidad_var.set("")
        precio_var.set("")
        lista.selection_clear(0, tk.END)

    lista.bind("<<ListboxSelect>>", rellenar_campos_para_edicion)

    # Botones
    acciones = tk.Frame(ventana_usuario, bg="#ffffff")
    acciones.pack()

    tk.Button(acciones, text="Agregar Producto", command=agregar_producto,
              bg=ACCENT_COLOR, fg="white", width=20).grid(row=0, column=0, padx=10, pady=5)

    tk.Button(acciones, text="Eliminar Seleccionado", command=eliminar_producto,
              bg="red", fg="white", width=20).grid(row=0, column=1, padx=10, pady=5)

    tk.Button(acciones, text="Editar Producto", command=editar_producto,
              bg="#FFA500", fg="white", width=20).grid(row=1, column=0, padx=10, pady=5)

    tk.Button(acciones, text="Limpiar Campos", command=limpiar_campos_producto,
              bg="#808080", fg="white", width=20).grid(row=1, column=1, padx=10, pady=5)

    cargar_productos()


# -------------------- Interfaz --------------------
root = tk.Tk()
root.title("Gestión de Usuarios")
root.geometry("500x600")
root.configure(bg="#f2f4f8")

# Colores corporativos
PRIMARY_COLOR = "#002B5C"
ACCENT_COLOR = "#4A90E2"
TEXT_COLOR = "#ffffff"

# Encabezado con logo
header = tk.Frame(root, bg=PRIMARY_COLOR)
header.pack(fill="x")

try:
    img = Image.open("Logo_StockMarket.png")  # Asegúrate de tener un logo
    img = img.resize((50, 50))
    logo = ImageTk.PhotoImage(img)
    tk.Label(header, image=logo, bg=PRIMARY_COLOR).pack(side="left", padx=10)
except:
    pass  # Si no hay logo, continúa sin error

tk.Label(header, text="Panel de Gestión de Usuarios", bg=PRIMARY_COLOR, fg=TEXT_COLOR,
         font=("Helvetica", 16, "bold")).pack(pady=10, padx=10)

# Variables de entrada
email_var = tk.StringVar()
pass_var = tk.StringVar()
nombre_var = tk.StringVar()

# Formulario
form = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
form.pack(pady=20)

tk.Label(form, text="Email:", bg="#ffffff").grid(row=0, column=0, sticky="w")
tk.Entry(form, textvariable=email_var, width=30).grid(row=0, column=1, pady=5)

tk.Label(form, text="Contraseña:", bg="#ffffff").grid(row=1, column=0, sticky="w")
tk.Entry(form, textvariable=pass_var, show="*", width=30).grid(row=1, column=1, pady=5)

tk.Label(form, text="Nombre/Perfil:", bg="#ffffff").grid(row=2, column=0, sticky="w")
tk.Entry(form, textvariable=nombre_var, width=30).grid(row=2, column=1, pady=5)

# Botones de acción
botones = tk.Frame(root, bg="#f2f4f8")
botones.pack(pady=10)

def boton_estilo(t, cmd):
    return tk.Button(botones, text=t, command=cmd,
                     bg=ACCENT_COLOR, fg="white", width=20, font=("Montserrat", 10, "bold"))

boton_estilo("Crear Usuario", crear_usuario).grid(row=0, column=0, padx=5, pady=5)
boton_estilo("Autenticar Usuario", autenticar_usuario).grid(row=0, column=1, padx=5, pady=5)
boton_estilo("Actualizar Perfil", actualizar_usuario).grid(row=1, column=0, padx=5, pady=5)
boton_estilo("Eliminar Usuario", eliminar_usuario).grid(row=1, column=1, padx=5, pady=5)
boton_estilo("Limpiar Campos", limpiar_campos).grid(row=2, column=0, columnspan=2, pady=5)

root.mainloop()


