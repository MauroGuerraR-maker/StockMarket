import pyrebase
import firebase_admin
from firebase_admin import credentials, db, auth as admin_auth

# -------------------- Configuración Pyrebase (para Auth) --------------------
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

# Inicializa Pyrebase para autenticación de usuarios
firebase = pyrebase.initialize_app(firebase_config)
pyre_auth = firebase.auth()

# -------------------- Configuración Firebase Admin (para la DB) --------------------
cred = credentials.Certificate("stockmarket-testbase.json")  # Tu archivo JSON de Admin SDK
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://stockmarket-e92e2-default-rtdb.firebaseio.com/"
})

# -------------------- Funciones --------------------

# Crear usuario (Auth) + perfil en DB
def crear_usuario(email, password):
    try:
        user = pyre_auth.create_user_with_email_and_password(email, password)
        uid = user['localId']
        print(f"Usuario creado con UID: {uid}")
        # Guardar perfil en la base de datos
        db.reference(f'usuarios/{uid}').set({
            "email": email,
            "perfil": {}
        })
        print("Perfil guardado en la base de datos.")
    except Exception as e:
        print(f"Error al crear usuario: {e}")

# Autenticación de usuario
def autenticar_usuario(email, password):
    try:
        user = pyre_auth.sign_in_with_email_and_password(email, password)
        print(f"Usuario autenticado correctamente. ID Token: {user['idToken']}")
        return user
    except Exception as e:
        print(f"Error al autenticar: {e}")
        return None

# Consultar datos de usuario
def obtener_datos_usuario(uid):
    try:
        data = db.reference(f'usuarios/{uid}').get()
        print(f"Datos del usuario: {data}")
        return data
    except Exception as e:
        print(f"Error al obtener datos: {e}")

# Eliminar usuario (Auth + DB)
def eliminar_usuario(uid):
    try:
        # Eliminar de Authentication con Admin SDK
        admin_auth.delete_user(uid)
        print("Usuario eliminado de Authentication.")

        # Eliminar de la base de datos
        db.reference(f'usuarios/{uid}').delete()
        print("Datos del usuario eliminados de la base de datos.")
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")

# -------------------- Ejemplo de uso --------------------
if __name__ == "__main__":
    email = "testuser@example.com"
    password = "Test1234!"

    # Crear un usuario
    crear_usuario(email, password)

    # Autenticar usuario
    user_info = autenticar_usuario(email, password)
    if user_info:
        uid = user_info['localId']
        # Consultar datos
        obtener_datos_usuario(uid)

        # Eliminar usuario
        eliminar_usuario(uid)
