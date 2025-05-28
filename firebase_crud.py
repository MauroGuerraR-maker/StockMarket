import pyrebase

# Configuración de tu proyecto Firebase
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

# Inicializar conexión
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
# --------------------------
#Funciones Basicas
#crear_usuario("Usuario 1", {"Nombre": "Mauro Antonio Guerra", "Hobby": "Origami"})
#crear_usuario("Usuario 6", {"Nombre": "Cristian David Rengifo Gomez","Hobby": "Dibujar","NumeroFavorito": 69,"Programa de ingeniería": "Ingeniería Civil"})
#actualizar_usuario("Usuario 1", {"Ciudad": "Bogotá"})
#
#
#
#
# --------------------------
# Funciones CRUD
# --------------------------

# Crear un nuevo usuario
def crear_usuario(id_usuario, datos):
    db.child("Usuarios").child(id_usuario).set(datos)
    print(f" Usuario '{id_usuario}' creado.")

# Leer datos de un usuario específico
def leer_usuario(id_usuario):
    usuario = db.child("Usuarios").child(id_usuario).get()
    if usuario.val():
        print(f" Datos de '{id_usuario}': {usuario.val()}")
    else:
        print(f" Usuario '{id_usuario}' no encontrado.")

# Leer todos los usuarios
def leer_todos_usuarios():
    usuarios = db.child("Usuarios").get()
    print(" Usuarios registrados:")
    for user in usuarios.each():
        print(f"{user.key()}: {user.val()}")

# Actualizar un usuario
def actualizar_usuario(id_usuario, datos_actualizados):
    db.child("Usuarios").child(id_usuario).update(datos_actualizados)
    print(f" Usuario '{id_usuario}' actualizado.")

# Eliminar un usuario
def eliminar_usuario(id_usuario):
    db.child("Usuarios").child(id_usuario).remove()
    print(f" Usuario '{id_usuario}' eliminado.")

# --------------------------
# Pruebas
# --------------------------
if __name__ == "__main__":
    # Crear un usuario nuevo
    crear_usuario("Usuario 5", {
        "nombre": "Laura Gómez",
        "email": "lauragomez@example.com",
        "activo": True
    })

    # Leer un usuario
    leer_usuario("Usuario 5")

    # Leer todos los usuarios
    leer_todos_usuarios()

    # Actualizar un usuario
    actualizar_usuario("Usuario 5", {"activo": False})

    # Eliminar un usuario
    eliminar_usuario("Usuario 5")

    # Leer todos los usuarios nuevamente
    leer_todos_usuarios()

