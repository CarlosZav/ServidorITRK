def init_maquinaHornos(app, socketio, emit):

    # Variables secadoras-Flexiones
    ciclosHornos = 0
    anguloApertura = 0
    velocidadHornos = 0
    pausarHornos = ""
    conteociclosHornos = 0
    estadoHornos = ""
    tiempoHornos = 0
    setVelocidadHornos = 0
    setciclosHornosAnimacion = 0
    tiempoPiston1Hornos = 0
    tiempoPiston2Hornos = 0
    tiempoPiston3Hornos = 0
    tiempoPiston4Hornos = 0

    estadoCalibracionLavadoras = ""
    sentidoLavadoras = ""
    gradosCalibrarLavadoras = 0

    # Funciones entre APP Y SERVIDOR SECADORAS-FLEX

    @socketio.on('datosFromHornos')
    def handle_message(data):
        global ciclosHornos, anguloAperturaHornos, velocidadHornos, pausarHornos, tiempoPiston1Hornos, tiempoPiston2Hornos, tiempoPiston3Hornos, tiempoPiston4Hornos
        # Extrae datos del JSON recibido
        if data:
            ciclosHornos = data.get("ciclosHornos")
            anguloApertura = data.get("anguloApertura")
            velocidadHornos = data.get("velocidadHornos")
            pausarHornos = data.get("pausarHornos")
            tiempoPiston1Hornos = data.get("tiempoPiston1Hornos")
            tiempoPiston2Hornos = data.get("tiempoPiston2Hornos")
            tiempoPiston3Hornos = data.get("tiempoPiston3Hornos")
            tiempoPiston4Hornos = data.get("tiempoPiston4Hornos")

            print("seteo Ciclos Hornos:", ciclosHornos)
            print("Angulo Apertura:", anguloApertura)
            print("Velocidad:", velocidadHornos)
            print("pausar:", pausarHornos)
            print("TiempoPiston 1:", tiempoPiston1Hornos)
            print("TiempoPiston 2:", tiempoPiston2Hornos)
            print("TiempoPiston 3:", tiempoPiston3Hornos)
            print("TiempoPiston 4:", tiempoPiston4Hornos)

            # Aquí se manda de una vez a la esp
            datos = {
                'ciclosHornos': ciclosHornos,
                'anguloApertura': anguloApertura,
                'velocidadHornos': velocidadHornos,
                'pausarHornos': pausarHornos,
                'tiempoPiston1Hornos': tiempoPiston1Hornos,
                'tiempoPiston2Hornos': tiempoPiston2Hornos,
                'tiempoPiston3Hornos': tiempoPiston3Hornos,
                'tiempoPiston4Hornos': tiempoPiston4Hornos,
            }
            # Aquí ya se están mandado los datos iniciales a la esp
            socketio.emit('mensajeHornos', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    @socketio.on('datosFromHornosPausar')
    def handle_message(data):
        global pausarHornos
        # Extrae datos del JSON recibido
        if data:
            pausarHornos = data.get("pausarHornos")
            print("pausarHornos: ", pausarHornos)

            # Aquí se manda de una vez a la esp
            datos = {
                'pausarHornos': pausarHornos,
            }
            socketio.emit('mensajeHornosPausar', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    # EVENTOS SERVIDOR-ESP Secadoras-Flexiones

    @socketio.on('datosEspHornos')
    def handle_message(msg):

        global conteociclosHornos, estadoHornos, tiempoHornos, velocidadHornos, ciclosHornos
        # Send all data back to the client

        if msg:
            conteociclosHornos = msg.get("conteoCiclosHornos")
            estadoHornos = msg.get("estadoHornos")
            tiempoHornos = msg.get("tiempoHornos")
            velocidadHornos = msg.get("velocidadHornos")
            ciclosHornos = msg.get("ciclosHornos")

            print(f"conteoCiclosHornos: {conteociclosHornos}")
            print(f"estadoHornos: {estadoHornos}")
            print(f"tiempoSecadorasFlex: {tiempoHornos}")
            print(f"velocidadHornos : {velocidadHornos}")
            print(f"ciclosHornos : {ciclosHornos}")

            data_store = {
                'conteoCiclosHornos': conteociclosHornos,
                'estadoHornos': estadoHornos,
                'tiempoHornos': tiempoHornos,
                'velocidadHornos': velocidadHornos,
                'ciclosHornos': ciclosHornos,
            }

            socketio.emit('datosServidorHornos', data_store)

    @socketio.on('datosfromCalibrarHornos')
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
            socketio.emit('mensajeCalibrarHornos', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    @socketio.on('recibirDatosServidorCalibracionHornos')
    def handle_recibir_todos_los_datos():
        global estadoCalibracion
        # Send all data back to the client
        data_store = {
            'estadoCalibracion': estadoCalibracion,
        }
        socketio.emit('datosServidorCalibracionHornos', data_store)

    # EVENTOS SERVIDOR-ESP Flexiones

    @socketio.on('calibrarEspConfirmacionHornos')
    def handle_message(msg):

        global estadoCalibracion
        print(f"Message received: {msg}")

        if msg:
            estadoCalibracion = msg.get("conexion")

            print(f"estado calibracion: {estadoCalibracion}")

        socketio.emit('calibracionConfirmacionHornosApp', msg)
