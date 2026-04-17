def init_calibracionLavadoras(app, socketio, emit):

    estadoCalibracionLavadoras = ""
    sentidoLavadoras = ""
    gradosCalibrarLavadoras = 0

    @socketio.on('datosfromCalibrarLavadoras')
    def handle_message(data):
        global sentido, gradosCalibrar
        # Extrae datos del JSON recibido
        if data:
            gradosCalibrar = data.get("gradosCalibrar")
            sentido = data.get("sentido")

            print("grados:", gradosCalibrar)
            print("Sentido:", sentido)

            # Aquí se manda de una vez a la esp
            datos = {
                'gradosCalibrar': gradosCalibrar,
                'sentido': sentido,
            }
            socketio.emit('mensajeCalibrarLavadoras', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    @socketio.on('recibirDatosServidorCalibracionLavadoras')
    def handle_recibir_todos_los_datos():
        global estadoCalibracion
        # Send all data back to the client
        data_store = {
            'estadoCalibracion': estadoCalibracion,
        }
        socketio.emit('datosServidorCalibracionLavadoras', data_store)

    # EVENTOS SERVIDOR-ESP Flexiones

    @socketio.on('calibrarEspConfirmacionLavadoras')
    def handle_message(msg):

        global estadoCalibracion
        print(f"Message received: {msg}")

        if msg:
            estadoCalibracion = msg.get("conexion")

            print(f"estado calibracion: {estadoCalibracion}")

        socketio.emit('calibracionConfirmacionLavadorasApp', msg)
