import pyrebase

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

# Inicializar Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Escribir datos en la base de datos
data = {
    "mensaje": "¡Conexión exitosa a la base de datos!",
    "usuario": "Prueba directa",
    "activo": True
}

db.child("prueba_conexion").set(data)

print("✅ Dato de prueba enviado a Firebase Realtime Database.")
