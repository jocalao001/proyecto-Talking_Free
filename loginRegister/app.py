from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = '123123123'  # Cambia esto a una clave secreta fuerte

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="usuarios"
)
cursor = db.cursor()

# Ruta de inicio
@app.route('/')
def index():
    return render_template('login.html')

# Ruta de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password_input = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

        # Insertar datos en la base de datos
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password_input))
        db.commit()

        # Redirigir a la página de inicio de sesión
        return redirect(url_for('index'))

    return render_template('registro.html')

# Ruta de inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verificar las credenciales en la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        

        if user and check_password_hash(user[2], password):
            # Iniciar sesión y redirigir a la página principal
            session['user'] = user
            session['logged_in'] = True
            return redirect(url_for('prueba'))

    # Redirigir de nuevo a la página de inicio de sesión en caso de credenciales incorrectas
    return redirect(url_for('index'))

# Ruta de cierre de sesión
@app.route('/logout')
def logout():
    session.pop('user', None)
    session['logged_in'] = False
    return redirect(url_for('index'))

# Ruta de bienvenida
@app.route('/bienvenido', methods=['GET'])
def prueba():
    if 'logged_in' in session and session['logged_in']:
        return render_template('prueba.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port="4002")
