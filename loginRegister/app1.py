from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = '123123123'

# Función para establecer la conexión a la base de datos
def establecer_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usuarios"
    )

def insertar_en_base_de_datos(nombre, email, password):
    try:
        # Hash de la contraseña utilizando passlib
        hashed_password = sha256_crypt.hash(password)

        # Consulta SQL para insertar un nuevo usuario
        query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
        values = (nombre, email, hashed_password)

        # Abrir conexión a la base de datos utilizando un contexto
        with establecer_conexion() as db, db.cursor() as cursor:
            # Ejecutar la consulta
            cursor.execute(query, values)

            # Hacer commit para aplicar los cambios en la base de datos
            db.commit()

        print("Usuario insertado correctamente.")

    except mysql.connector.Error as e:
        # En caso de error específico de MySQL, hacer rollback para deshacer cualquier cambio
        print(f"Error al insertar usuario en la base de datos: {str(e)}")


def authenticate_user(email, password):
    """Authenticate a user"""

    try:
        # Supongo que tu modelo de usuario tiene un campo 'email' en lugar de 'username'
        user = User.query.filter_by(email=email).first()
    except OperationalError:
        db.create_all()
        user = User.query.filter_by(email=email).first()

    authenticated = False

    if user:
        authenticated = sha256_crypt.verify(password, user.password)
    else:
        time.sleep(1)
        flash("Authentication Error: User not found in DB", 'error')
        return False

    if authenticated:
        session['logged_in'] = True
        session['email'] = email
        flash("Successfully Authenticated", 'success')
        return True
    else:
        flash("Authentication Failed", 'error')
        return False

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verificar las credenciales en la base de datos
        if authenticate_user(email, password):
            return redirect(url_for('prueba'))

    return render_template('login.html')

@app.route('/registro', methods=['POST', 'GET'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        # Hash de la contraseña utilizando passlib
        hashed_password = sha256_crypt.hash(password)

        # Insertar el nuevo usuario en la base de datos con la contraseña hasheada
        insertar_en_base_de_datos(nombre, email, hashed_password)

        flash('Registro exitoso. Inicia sesión ahora.', 'success')

        # Redirigir al usuario a la página de login después del registro
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/bienvenido', methods=['GET'])
def prueba():
    if 'logged_in' in session and session['logged_in']:
        return render_template('prueba.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=4004)
