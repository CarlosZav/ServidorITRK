from flask import Flask
from flask_socketio import SocketIO, emit
import threading
import time
import sqlite3
import os
from datetime import datetime
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Variable global para almacenar el valor del sensor más reciente
sensor_value = 0
conteo_ciclos = 0
estado_ssr = ""
tiempo_transcurrido = 0
seteo_ciclos = 0
seteo_tiempo_apagado = 0
seteo_tiempo_encendido = 0

# Variables para prueba de flexiones
conteo_ciclosFlex = 0
estado_pruebaFlex = 0
tiempo_transcurridoFlex = 0
seteo_ciclosFlexiones = 0
pausarF = ""
seteoAnguloA = 0
seteoAnguloB = 0

# Variables para prueba de planchas
conteoCiclosPlanchas = 0
estadoPruebaPlanchas = 0
tiempoTranscurridoPlanchas = 0
setCiclosPlanchas = 0
pausarPlanchas = ""
setTiempoElevadoPlanchas = 0
setTiempoBajoPlanchas = 0


# Variables secadoras-Rotaciones
revolucionesSecadoras = 0
revCambioSecadoras = 0
velocidadRevoluciones = 0
pausarSecadorasRot = ""
conteo_revSecadorasRot = 0
estado_pruebaSecadorasRot = ""
tiempo_pruebaSecadorasRot = 0
velocidad_SecadorasRot = 0
setRevSecadorasRot = 0

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


# EVENTOS SERVIDOR-APP Calentamiento

@socketio.on('recibirDatosServer')
def handle_recibir_todos_los_datos():
    global sensor_value, estado_ssr, conteo_ciclos, tiempo_transcurrido
    # Send all data back to the client
    data_store = {
        'sensor_value': sensor_value,
        'estado_ssr': estado_ssr,
        'conteo_ciclos': conteo_ciclos,
        'tiempo_transcurrido': tiempo_transcurrido
    }
    socketio.emit('datosServidor', data_store)


@socketio.on('datosfromApp')
def handle_message(data):
    global seteo_ciclos, seteo_tiempo_apagado, seteo_tiempo_encendido
    # Extrae datos del JSON recibido
    if data:
        seteo_ciclos = data.get("seteo_ciclos")
        seteo_tiempo_apagado = data.get("seteo_tiempo_apagado")
        seteo_tiempo_encendido = data.get("seteo_tiempo_encendido")

        print("Datos recibidos:")
        print("seteo ciclos:", seteo_ciclos)
        print("seteo_tiempo_apagado:", seteo_tiempo_apagado)
        print("seteo_tiempo_encendido:", seteo_tiempo_encendido)

        datos = {
            'seteo_ciclos': seteo_ciclos,
            'tiempo_apagado': seteo_tiempo_apagado,
            'tiempo_prendido': seteo_tiempo_encendido
        }
        socketio.emit('hola2', {'mensaje': datos})
        print("Mensaje enviado a los clientes.")

# EVENTOS SERVIDOR-ESP Calentamiento


@socketio.on('datos_esp')
def handle_message(msg):

    global sensor_value, estado_ssr, conteo_ciclos, tiempo_transcurrido

    print(f"Message received: {msg}")

    if msg:
        sensor_value = msg.get("corriente")
        estado_ssr = msg.get("estado_ssr")
        conteo_ciclos = msg.get("conteo_ciclos")
        tiempo_transcurrido = msg.get("tiempo_transcurrido")

        print(f"Corriente: {sensor_value}")
        print(f"Estado ssr: {estado_ssr}")
        print(f"Num de ciclos: {conteo_ciclos}")
        print(f"Tiempo transcurrido: {tiempo_transcurrido}")

    emit('response', {'data': 'Message received by server'}, broadcast=True)

# @socketio.on('event')
# def handle_custom_event(data):
    # print(f"Custom event received: {data}")
    # emit('response', {'data': 'Event received by server'}, broadcast=True)


def emitir_mensaje():
    global seteo_ciclos, seteo_tiempo_encendido, seteo_tiempo_apagado
    datos = {
        'seteo_ciclos': seteo_ciclos,
        'tiempo_apagado': seteo_tiempo_apagado,
        'tiempo_prendido': seteo_tiempo_encendido
    }
    socketio.sleep(5)  # No bloqueante
    socketio.emit('hola2', {'mensaje': datos})
    print("Mensaje enviado a los clientes.")


# Funciones entre APP Y SERVIDOR FLEXIONES

@socketio.on('datosfromFlexiones')
def handle_message(data):
    global seteo_ciclosFlexiones, seteoAnguloA, seteoAnguloB, pausarF
    # Extrae datos del JSON recibido
    if data:
        seteo_ciclosFlexiones = data.get("seteo_ciclosF")
        seteoAnguloA = data.get("seteo_anguloA")
        seteoAnguloB = data.get("seteo_anguloB")
        pausarF = data.get("pausar")

        print("seteo ciclos:", seteo_ciclosFlexiones)
        print("Angulo A:", seteoAnguloA)
        print("Angulo B:", seteoAnguloB)
        print("Pausar:", pausarF)

        # Aquí se manda de una vez a la esp
        datos = {
            'seteo_ciclosF': seteo_ciclosFlexiones,
            'seteoAnguloA': seteoAnguloA,
            'seteoAnguloB': seteoAnguloB,
            'pausarF': pausarF,
        }
        socketio.emit('mensajeFlexiones', {'mensaje': datos})
        print("Mensaje enviado a los clientes.")


@socketio.on('datosfromFlexiones_pausar')
def handle_message(data):
    global pausarF
    # Extrae datos del JSON recibido
    if data:
        pausarF = data.get("pausarF")
        print("Pausar: ", pausarF)

        # Aquí se manda de una vez a la esp
        datos = {
            'pausarF': pausarF,
        }
        socketio.emit('mensajeFlexiones_pausar', {'mensaje': datos})
        print("Mensaje enviado a los clientes.")


@socketio.on('recibirDatosServerFlexiones')
def handle_recibir_todos_los_datos():
    global conteo_ciclosFlex, estado_pruebaFlex, tiempo_transcurridoFlex
    # Send all data back to the client
    data_store = {
        'conteo_ciclosF': conteo_ciclosFlex,
        'estado_pruebaF': estado_pruebaFlex,
        'tiempo_transcurridoF': tiempo_transcurridoFlex
    }
    socketio.emit('datosServidorFlexiones', data_store)

# EVENTOS SERVIDOR-ESP Flexiones


@socketio.on('datos_espFlexiones')
def handle_message(msg):

    global conteo_ciclosFlex, estado_pruebaFlex, tiempo_transcurridoFlex
    print(f"Message received: {msg}")

    if msg:
        conteo_ciclosFlex = msg.get("conteo_ciclos")
        estado_pruebaFlex = msg.get("Estado")
        tiempo_transcurridoFlex = msg.get("tiempo_transcurrido")

        print(f"conteo ciclos: {conteo_ciclosFlex}")
        print(f"Estado prueba: {estado_pruebaFlex}")
        print(f"Tiempo transcurrido: {tiempo_transcurridoFlex}")

    emit('response', {'data': 'Message received by server'}, broadcast=True)


def emitir_mensajeFlexiones():
    global seteo_ciclosFlexiones, seteoAnguloA, seteoAnguloB, pausarF
    datos = {
        'seteo_ciclosF': seteo_ciclosFlexiones,
        'seteoAnguloA': seteoAnguloA,
        'seteoAnguloB': seteoAnguloB,
        'pausarF': pausarF
    }
    socketio.sleep(5)  # No bloqueante
    socketio.emit('mensajeFlexiones', {'mensaje': datos})
    print("Mensaje enviado a los clientes.")


# MAQUINA DE PLANCHAS

# Funciones entre APP Y SERVIDOR PLANCHAS

@socketio.on('datosFromPlanchas')
def handle_message(data):
    global setCiclosPlanchas, setTiempoElevadoPlanchas, setTiempoBajoPlanchas, pausarPlanchas
    # Extrae datos del JSON recibido
    if data:
        setCiclosPlanchas = data.get("setCiclos")
        setTiempoElevadoPlanchas = data.get("setTiempoElevado")
        setTiempoBajoPlanchas = data.get("setTiempoBajo")
        pausarPlanchas = data.get("pausar")

        print("seteo ciclos Planchas:", setCiclosPlanchas)
        print("Tiempo Alto seteado:", setTiempoElevadoPlanchas)
        print("Tiempo Bajo seteado:", setTiempoBajoPlanchas)
        print("Pausar Planchas:", pausarPlanchas)

        # Aquí se manda de una vez a la esp
        datos = {
            'setCiclos': setCiclosPlanchas,
            'setTiempoElevado': setTiempoElevadoPlanchas,
            'setTiempoBajo': setTiempoBajoPlanchas,
            'pausar': pausarPlanchas,
        }
        # Aquí ya se están mandado los datos iniciales a la esp
        socketio.emit('mensajePlanchas', {'mensaje': datos})
        print("Mensaje enviado a los clientes.")


@socketio.on('datosFromPlanchasPausar')
def handle_message(data):
    global pausarPlanchas
    # Extrae datos del JSON recibido
    if data:
        pausarPlanchas = data.get("pausar")
        print("Pausar: ", pausarPlanchas)

        # Aquí se manda de una vez a la esp
        datos = {
            'pausar': pausarPlanchas,
        }
        socketio.emit('mensajePlanchasPausar', {'mensaje': datos})
        print("Mensaje enviado a los clientes.")


@socketio.on('recibirDatosServerPlanchas')
def handle_recibir_todos_los_datos():
    global conteoCiclosPlanchas, estadoPruebaPlanchas, tiempoTranscurridoPlanchas, setCiclosPlanchas
    # Send all data back to the client
    data_store = {
        'conteoCiclosPlanchas': conteoCiclosPlanchas,
        'estadoPruebaPlanchas': estadoPruebaPlanchas,
        'tiempoTranscurridoPlanchas': tiempoTranscurridoPlanchas,
        'setCiclosPlanchas': setCiclosPlanchas
    }
    socketio.emit('datosServerPlanchas', data_store)


# EVENTOS SERVIDOR-ESP Planchas

@socketio.on('datosEspPlanchas')
def handle_message(msg):

    global conteoCiclosPlanchas, estadoPruebaPlanchas, tiempoTranscurridoPlanchas

    if msg:
        conteoCiclosPlanchas = msg.get("conteo_ciclos")
        estadoPruebaPlanchas = msg.get("Estado")
        tiempoTranscurridoPlanchas = msg.get("tiempo_transcurrido")

        print(f"conteo ciclos: {conteoCiclosPlanchas}")
        print(f"Estado prueba: {estadoPruebaPlanchas}")
        print(f"Tiempo transcurrido: {tiempoTranscurridoPlanchas}")
    emit('response', {'data': 'Message received by server'}, broadcast=True)


def emitir_mensajeFlexiones():
    global setCiclosPlanchas, pausarPlanchas, setTiempoElevadoPlanchas, setTiempoBajoPlanchas
    datos = {
        'setCiclosPlanchas': setCiclosPlanchas,
        'setTiempoApagado': setTiempoElevadoPlanchas,
        'setTiempoPrendido': setTiempoBajoPlanchas,
        'pausar': pausarPlanchas
    }
    socketio.sleep(5)  # No bloqueante
    socketio.emit('mensajePlanchas', {'mensaje': datos})
    print("Mensaje enviado a los clientes.")


# MAQUINA SECADORA-ROTACIONES

# Funciones entre APP Y SERVIDOR SECADORAS-ROTACIONES

@socketio.on('datosfromSecadorasRot')
def handle_message(data):
    global revolucionesSecadoras, revCambioSecadoras, velocidadRevoluciones, pausarSecadorasRot
    # Extrae datos del JSON recibido
    if data:
        revolucionesSecadoras = data.get("revolucionesSecadoras")
        revCambioSecadoras = data.get("revCambioSecadoras")
        velocidadRevoluciones = data.get("velocidadRevoluciones")
        pausarSecadorasRot = data.get("pausarSecadorasRot")

        print("seteo revoluciones secadoras:", revolucionesSecadoras)
        print("Revoluciones de cambio:", revCambioSecadoras)
        print("Velocidad seteada RPM:", velocidadRevoluciones)
        print("Pausar SecadorasRot:", pausarSecadorasRot)

        # Aquí se manda de una vez a la esp
        datos = {
            'revolucionesSecadoras': revolucionesSecadoras,
            'revCambioSecadoras': revCambioSecadoras,
            'velocidadRevoluciones': velocidadRevoluciones,
            'pausarSecadorasRot': pausarSecadorasRot,
        }
        # Aquí ya se están mandado los datos iniciales a la esp
        socketio.emit('mensajeSecadorasRot', {'mensaje': datos})
        print("Mensaje enviado a los clientes.")


@socketio.on('datosfromSecadorasRotaciones_pausar')
def handle_message(data):
    global pausarSecadorasRot
    # Extrae datos del JSON recibido
    if data:
        pausarSecadorasRot = data.get("pausarSecadorasRot")
        print("pausarSecadorasRot: ", pausarSecadorasRot)

        # Aquí se manda de una vez a la esp
        datos = {
            'pausarSecadorasRot': pausarSecadorasRot,
        }
        socketio.emit('mensajeSecadorasRotPausar', {'mensaje': datos})
        print("Mensaje enviado a los clientes.")


@socketio.on('recibirDatosServerSecadorasRot')
def handle_recibir_todos_los_datos():
    global conteo_revSecadorasRot, estado_pruebaSecadorasRot, tiempo_pruebaSecadorasRot, velocidad_SecadorasRot, setRevSecadorasRot
    # Send all data back to the client
    data_store = {
        'conteo_revSecadorasRot': conteo_revSecadorasRot,
        'estado_pruebaSecadorasRot': estado_pruebaSecadorasRot,
        'tiempo_pruebaSecadorasRot': tiempo_pruebaSecadorasRot,
        'velocidad_SecadorasRot': velocidad_SecadorasRot,
        'setRevSecadorasRot': setRevSecadorasRot
    }
    socketio.emit('datosServerPlanchas', data_store)

# EVENTOS SERVIDOR-ESP Secadoras-Rotacion


@socketio.on('datosEspSecadorasRot')
def handle_message(msg):

    global conteo_revSecadorasRot, estado_pruebaSecadorasRot, tiempo_pruebaSecadorasRot, velocidad_SecadorasRot, setRevSecadorasRot

    if msg:
        conteo_revSecadorasRot = msg.get("conteo_revSecadorasRot")
        estado_pruebaSecadorasRot = msg.get("estado_pruebaSecadorasRot")
        tiempo_pruebaSecadorasRot = msg.get("tiempo_pruebaSecadorasRot")
        velocidad_SecadorasRot = msg.get("velocidad_SecadorasRot")
        setRevSecadorasRot = msg.get("setRevSecadorasRot")

        print(f"conteo_revSecadorasRot: {conteo_revSecadorasRot}")
        print(f"estado_pruebaSecadorasRot: {estado_pruebaSecadorasRot}")
        print(f"tiempo_pruebaSecadorasRot: {tiempo_pruebaSecadorasRot}")
        print(f"velocidad_SecadorasRot: {velocidad_SecadorasRot}")
        print(f"velocidad_SecadorasRot: {velocidad_SecadorasRot}")

    emit('response', {'data': 'Message received by server'}, broadcast=True)

# socketio.start_background_task(emitir_mensaje)


if __name__ == '__main__':
   # create_db()

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # Mostrar la dirección IP al iniciar el servidor
    print(f"El servidor está corriendo en: http://{local_ip}:5000")

   # threading.Thread(target=save_data, daemon=True).start()  # Inicia el guardado automático en segundo plano
    socketio.run(app, host='0.0.0.0', port=5000)
