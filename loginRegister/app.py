from flask import Flask, render_template, request, redirect, url_for, session, Response
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
# pylint: disable=no-member
# pylint: disable=import-error
import cv2
import mediapipe as mp
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = "123123123"

# Configuración de la base de datos de login y register
db_usuarios = mysql.connector.connect(
    host="localhost", user="root", password="", database="usuarios"
)
cursor_usuarios = db_usuarios.cursor()

# Configuración de la base de datos de la herammienta de notas
db_notas = mysql.connector.connect(
    host="localhost", user="root", password="", database="notas"
)
cursor_notas = db_notas.cursor(dictionary=True)


# Ruta de inicio
@app.route("/")
def index():
    return render_template("loginRegistro.html")

# Ruta de registro
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password_input = generate_password_hash(
            request.form["password"], method="pbkdf2:sha256"
        )

        # Insertar datos en la base de datos
        cursor_usuarios.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password_input),
        )
        db_usuarios.commit()

        # Redirigir a la página de inicio de sesión
        return redirect(url_for("index"))

    return render_template("loginRegistro.html")


# Ruta de inicio de sesión
# Ruta de inicio de sesión
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password_input = request.form["password"]

        # Obtener la contraseña almacenada en la base de datos
        cursor_usuarios.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor_usuarios.fetchone()

        if user:
            print(f"Email ingresado: {email}")
            print(f"Usuario encontrado en la base de datos: {user}")

            # Verificar la contraseña
            if check_password_hash(user[3], password_input):
                # Iniciar sesión y redirigir a la página principal
                session["user"] = user
                session["logged_in"] = True
                return redirect(url_for("prueba"))
            else:
                print("La verificación de contraseña falló.")
        else:
            print(f"No se encontró ningún usuario con el correo electrónico: {email}")

    # Redirigir de nuevo a la página de inicio de sesión en caso de credenciales incorrectas
    return redirect(url_for("index"))


# Ruta de cierre de sesión
@app.route("/logout")
def logout():
    session.pop("user", None)
    session["logged_in"] = False
    return redirect(url_for("index"))


# Ruta despues de aprovado el inicio de sesion
@app.route("/bienvenido", methods=["GET"])
def prueba():
    if "logged_in" in session and session["logged_in"]:
        return render_template("prueba.html")
    else:
        return redirect(url_for("login"))


# Ruta para mostrar notas
@app.route("/notas")
def index2():
    cursor_notas.execute(
        "SELECT id, content, created_at FROM notas ORDER BY created_at DESC"
    )
    notes = cursor_notas.fetchall()
    # Formatear la fecha en cada nota antes de pasarla al template
    for note in notes:
        note["formatted_date"] = note["created_at"].strftime("%d-%m-%Y")

    return render_template("index.html", notes=notes)


# Ruta para agregar una nueva nota
@app.route("/create_note", methods=["POST"])
def create_note():
    content = request.form["note_content"]
    cursor_notas.execute("INSERT INTO notas (content) VALUES (%s)", (content,))
    db_notas.commit()
    return redirect(url_for("index2"))


# Ruta para editar una nota
@app.route("/edit_note/<int:id>")
def edit_note(id):
    cursor_notas.execute("SELECT * FROM notas WHERE id = %s", (id,))
    note = cursor_notas.fetchone()
    return render_template("edit_note.html", note=note)


# Ruta para actualizar una nota editada
@app.route("/update_note/<int:id>", methods=["POST"])
def update_note(id):
    new_content = request.form["new_content"]
    cursor_notas.execute(
        "UPDATE notas SET content = %s WHERE id = %s", (new_content, id)
    )
    db_notas.commit()
    return redirect(url_for("index2"))


# Ruta para eliminar una nota
@app.route("/delete_note/<int:id>")
def delete_note(id):
    cursor_notas.execute("DELETE FROM notas WHERE id = %s", (id,))
    db_notas.commit()
    return redirect(url_for("index2"))


@app.route("/transcription")
def index3():
    return render_template("audio.html")


# Inicializa la detección de manos de Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Inicializa la cámara web
cap = cv2.VideoCapture(0)


@app.route("/HandGestureDetection")
def index4():
    return render_template("handDetect.html")


@socketio.on("interpretation_update")
def handle_interpretation_update(interpretation):
    socketio.emit("interpretation_result", interpretation)


def generate_frames():
    while True:
        ret, frame = cap.read()

        # Pasar el marco original a Mediapipe
        results = hands.process(frame)

        # Lógica de interpretación
        interpretation = ""
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                # Dibujar los landmarks en el marco
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, landmarks, mp_hands.HAND_CONNECTIONS
                )

                # Obtener la posición de los dedos
                thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

                thumb_tip_y = int(thumb_tip.y * frame.shape[0])
                index_tip_y = int(index_tip.y * frame.shape[0])
                middle_tip_y = int(middle_tip.y * frame.shape[0])
                ring_tip_y = int(ring_tip.y * frame.shape[0])
                pinky_tip_y = int(pinky_tip.y * frame.shape[0])

                # Obtener la posición del pulgar
                if (
                    thumb_tip_y
                    < landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                    * frame.shape[0]
                ):
                    interpretation = "bien"

                if (
                    thumb_tip_y
                    > landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                    * frame.shape[0]
                ):
                    interpretation = "mal"

        _, buffer = cv2.imencode(".jpg", cv2.flip(frame, 1))
        frame = buffer.tobytes()
        socketio.emit("interpretation_result", interpretation)
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/HandGestureDetection/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    socketio.run(app, debug=True, port="4002")
