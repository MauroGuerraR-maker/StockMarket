from flask import Flask, render_template, request, redirect, session, url_for, flash
import pyrebase
import firebase_admin
from firebase_admin import credentials, db, auth as admin_auth
import os

app = Flask(__name__)
app.secret_key = '123456'  # Cambia esta clave en producción

# -------------------- CONFIGURACIÓN FIREBASE --------------------
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

# Inicializamos Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
pyre_auth = firebase.auth()

# Inicializamos Admin SDK para la base de datos
cred = credentials.Certificate("stockmarket-testbase.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": firebase_config["databaseURL"]
    })

# -------------------- RUTAS FLASK --------------------
@app.route('/')
def home():
    """ Página de inicio """
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = pyre_auth.sign_in_with_email_and_password(email, password)
            uid = user['localId']
            datos = db.reference(f'usuarios/{uid}').get()
            session['user'] = {'uid': uid, 'perfil': datos.get('perfil', 'Usuario')}
            print(f"✅ User logged in: {email}, UID: {uid}")  # <-- Añadir
            return redirect(url_for("inventario"))
        except Exception as e:
            print(f"❌ Login error: {e}")  # <-- Añadir para diagnosticar
            flash("Correo o contraseña incorrectos.")
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    """ Página de registro """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        perfil = request.form.get("perfil")
        try:
            user = pyre_auth.create_user_with_email_and_password(email, password)
            uid = user['localId']
            db.reference(f'usuarios/{uid}').set({
                "email": email,
                "perfil": perfil
            })
            flash("Usuario registrado correctamente. Ahora inicia sesión.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error al crear usuario: {str(e)}", "error")
    return render_template("register.html")

@app.route('/inventario')
def inventario():
    """ Página de inventario """
    if 'user' not in session:
        return redirect(url_for("login"))
    uid = session['user']['uid']
    perfil = session['user']['perfil']
    productos = db.reference(f'usuarios/{uid}/productos').get() or {}
    print(f"✅ Inventario cargado para UID: {uid}")
    return render_template("inventario.html", perfil=perfil, productos=productos)

@app.route('/agregar_producto', methods=["POST"])
def agregar_producto():
    """ Agrega producto al inventario """
    if 'user' not in session:
        return redirect(url_for("login"))
    uid = session['user']['uid']

    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    cantidad = request.form.get('cantidad')
    precio = request.form.get('precio')

    if nombre and cantidad.isdigit() and precio.replace('.', '', 1).isdigit():
        db.reference(f'usuarios/{uid}/productos').push({
            "nombre": nombre,
            "descripcion": descripcion,
            "cantidad": int(cantidad),
            "precio": float(precio)
        })
    else:
        flash("Por favor ingresa datos válidos para el producto.", "error")

    return redirect(url_for("inventario"))

@app.route('/eliminar_producto/<producto_id>', methods=["POST"])
def eliminar_producto(producto_id):
    """ Elimina producto del inventario """
    if 'user' not in session:
        return redirect(url_for("login"))
    uid = session['user']['uid']
    db.reference(f'usuarios/{uid}/productos/{producto_id}').delete()
    flash("Producto eliminado correctamente.", "success")
    return redirect(url_for("inventario"))

@app.route('/editar_producto/<producto_id>', methods=["GET", "POST"])
def editar_producto(producto_id):
    """Edita un producto existente."""
    if 'user' not in session:
        return redirect(url_for("login"))
    uid = session['user']['uid']
    producto_ref = db.reference(f'usuarios/{uid}/productos/{producto_id}')
    producto = producto_ref.get()

    if request.method == "POST":
        # Recoger datos del formulario
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        cantidad = request.form.get('cantidad')
        precio = request.form.get('precio')

        if nombre and cantidad.isdigit() and precio.replace('.', '', 1).isdigit():
            producto_ref.update({
                "nombre": nombre,
                "descripcion": descripcion,
                "cantidad": int(cantidad),
                "precio": float(precio)
            })
            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for("inventario"))
        else:
            flash("Por favor ingresa datos válidos para actualizar el producto.", "error")

    return render_template("editar_producto.html", producto=producto, producto_id=producto_id)


@app.route('/logout')
def logout():
    """ Cierra la sesión """
    session.clear()
    return redirect(url_for("home"))

# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run(debug=True)
