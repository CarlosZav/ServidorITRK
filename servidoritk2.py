from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import time
import sqlite3
import os
from datetime import datetime
import socket
from routes.maquinaCalentamiento import init_maquinaCalentamiento
from routes.maquinaFlexiones import init_maquinaFlexiones
from routes.maquinaPlanchas import init_maquinaPlanchas
from routes.maquinaSecadorasRotaciones import init_maquinaSecadorasRotaciones
from routes.maquinaSecadorasFlexiones import init_maquinaSecadorasFlexiones
from routes.calibracionSecadoras import init_calibracionSecadoras
from routes.maquinaClavijas import init_maquinaClavijas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


# Función para crear la base de datos y la tabla
"""def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hora TEXT NOT NULL,
            fecha TEXT NOT NULL,
            valor REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Función para guardar datos cada segundo con el valor del sensor
def save_data():
    global sensor_value
    while True:
        hora = datetime.now().strftime('%H:%M:%S')
        fecha = datetime.now().strftime('%Y-%m-%d')
       
        print(f"Guardando en DB: {hora}, {fecha}, {sensor_value}")  # Imprimir valor antes de guardar
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_data (hora, fecha, valor) VALUES (?, ?, ?)
        ''', (hora, fecha, sensor_value))
        conn.commit()
        conn.close()
       
        time.sleep(1)
"""
# Declare global variables at the top level
sensorValueC = 0
estadoSsrC = ""
conteoCiclosC = 0
tiempoTranscurridoC = 0
seteoCiclosC = 0
setTiempoApagadoC = 0
setTiempoEncendidoC = 0


@app.route('/')
def index():
    return "Socket.IO server running!"


@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'Connected to server!'}, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")


@socketio.on_error_default
def default_error_handler(e):
    print(f"An error occurred: {e}")
    # Aquí podrías agregar lógica para manejar el error adecuadamente.


init_maquinaCalentamiento(app, socketio, emit)

init_maquinaFlexiones(app, socketio, emit)

init_maquinaPlanchas(app, socketio, emit)

init_maquinaSecadorasRotaciones(app, socketio, emit)

init_maquinaSecadorasFlexiones(app, socketio, emit)

init_calibracionSecadoras(app, socketio, emit)

init_maquinaClavijas(app, socketio, emit)

# socketio.start_background_task(emitir_mensaje)


if __name__ == '__main__':
   # create_db()

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # Mostrar la dirección IP al iniciar el servidor
    print(f"El servidor está corriendo en: http://{local_ip}:5000")

   # threading.Thread(target=save_data, daemon=True).start()  # Inicia el guardado automático en segundo plano
    socketio.run(app, host='0.0.0.0', port=5000)
