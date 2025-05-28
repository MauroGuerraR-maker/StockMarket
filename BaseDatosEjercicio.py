import firebase_admin
from firebase_admin import credentials, db

# Configura el acceso a Firebase
#cred = credentials.Certificate("testpoo-59c96.json")  # Cambia por el nombre del archivo JSON
cred = credentials.Certificate("stockmarket-testbase.json")  # Cambia por el nombre del archivo JSON
firebase_admin.initialize_app(cred, {
    #"databaseURL": "https://testpoo-59c96-default-rtdb.firebaseio.com"  # Cambia con tu URL de la base de datos
    "databaseURL": "https://stockmarket-e92e2-default-rtdb.firebaseio.com/"  # Cambia con tu URL de la base de datos
})

