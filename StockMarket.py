import firebase_admin
from firebase_admin import credentials, db

# Configura el acceso a Firebase
#cred = credentials.Certificate("testpoo-59c96.json")  # Cambia por el nombre del archivo JSON
cred = credentials.Certificate("stockmarket-testbase.json")  # Cambia por el nombre del archivo JSON
firebase_admin.initialize_app(cred, {
    #"databaseURL": "https://testpoo-59c96-default-rtdb.firebaseio.com"  # Cambia con tu URL de la base de datos
    "databaseURL": "https://stockmarket-e92e2-default-rtdb.firebaseio.com/"  # Cambia con tu URL de la base de datos
})
#Capturar datos de entrevista: nombre, edad, ingenieria, hobbie, numero fav.
#Tupla
ref5 = db.reference("Usuarios/Usuario 4") 
ref5.set({
    "Nombre": "Cristian David Renginfo Gomez",
    "Edad":"22",
    "Programa de ingenieria": "Ingenieria Civil",
    "Hobbie": "Tomar",
    "NumeroFavorito":"69"
})

x=("Julian", 18,"Ingenieria Agricola", "Dibujar", 24)
ref3 = db.reference("Usuarios/Usuario 2") 
ref3.set({
    "Nombre": x[0],
    "Edad": x[1],
    "Programa de Ingenieria": x[2],
    "Hobbie": x[3],
    "NumeroFavorito": x[4]
})

#Conjuntos de datos
ref2 = db.reference("Usuarios/Usuario 1") 
ref2.set({
    "Nombre": "Mauro Antonio Guerra Rodriguez",
    "Edad":"17",
    "Programa de ingenieria": "Ingenieria Civil",
    "Hobbie": "Origami",
    "NumeroFavorito":"7"
})
# Referencia al nodo en la base de datos
ref = db.reference("nodo1")  # Cambia "nodo_principal" por tu ruta

# Escribe datos en tiempo real
ref.set({
    "mensaje": "Hola desde Python",
    "activo": True
})

# Escucha cambios en tiempo real
def escuchar_eventos(event):
    print(f"Cambio detectado: {event.data}")

ref.listen(escuchar_eventos)