def init_calibracionSecadoras(app, socketio, emit):

    estadoCalibracion = ""
    sentido = ""
    gradosCalibrar = 0

    @socketio.on('datosfromCalibrarSecadoras')
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
            socketio.emit('mensajeCalibrarSecadoras', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    @socketio.on('recibirDatosServidorCalibracionSecadoras')
    def handle_recibir_todos_los_datos():
        global estadoCalibracion
        # Send all data back to the client
        data_store = {
            'estadoCalibracion': estadoCalibracion,
        }
        socketio.emit('datosServidorCalibracionSecadoras', data_store)

    # EVENTOS SERVIDOR-ESP Flexiones

    @socketio.on('datosEspCalibracionSecadoras')
    def handle_message(msg):

        global estadoCalibracion
        print(f"Message received: {msg}")

        if msg:
            estadoCalibracion = msg.get("estadoCalibracion")

            print(f"estado calibracion: {estadoCalibracion}")

        emit('response', {
             'data': 'Message received by server'}, broadcast=True)
