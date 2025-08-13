def init_maquinaSecadorasFlexiones(app, socketio, emit):

    # Variables secadoras-Flexiones
    flexionesSecadoras = 0
    anguloA = 0
    anguloB = 0
    velocidadFlexiones = 0
    pausarSecadorasFlex = ""
    conteoFlexSecadoras = 0
    estadoSecadorasFlex = ""
    tiempoSecadorasFlex = 0
    setVelocidadSecadorasFlex = 0
    setConteoFlexSecadoras = 0

    # MAQUINA SECADORA-ROTACIONES

    # Funciones entre APP Y SERVIDOR SECADORAS-FLEX
    @socketio.on('datosfromSecadorasFlex')
    def handle_message(data):
        global flexionesSecadoras, anguloA, anguloB, setVelocidadSecadorasFlex, pausarSecadorasFlex
        # Extrae datos del JSON recibido
        if data:
            flexionesSecadoras = data.get("flexionesSecadoras")
            anguloA = data.get("anguloA")
            anguloB = data.get("anguloB")
            setVelocidadSecadorasFlex = data.get("setVelocidadSecadorasFlex")
            pausarSecadorasFlex = data.get("pausarSecadorasFlex")

            print("seteo Flexiones secadoras:", flexionesSecadoras)
            print("Angulo A:", anguloA)
            print("Angulo B:", anguloB)
            print("Velocidad:", setVelocidadSecadorasFlex)
            print("pausarSecadorasFlex:", pausarSecadorasFlex)

            # Aquí se manda de una vez a la esp
            datos = {
                'flexionesSecadoras': flexionesSecadoras,
                'anguloA': anguloA,
                'anguloB': anguloB,
                'setVelocidadSecadorasFlex': setVelocidadSecadorasFlex,
                'pausarSecadorasFlex': pausarSecadorasFlex,
            }
            # Aquí ya se están mandado los datos iniciales a la esp
            socketio.emit('mensajeSecadorasFlex', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    @socketio.on('datosfromSecadorasFlexionesPausar')
    def handle_message(data):
        global pausarSecadorasFlex
        # Extrae datos del JSON recibido
        if data:
            pausarSecadorasFlex = data.get("pausarSecadorasFlex")
            print("pausarSecadorasFlex: ", pausarSecadorasFlex)

            # Aquí se manda de una vez a la esp
            datos = {
                'pausarSecadorasFlex': pausarSecadorasFlex,
            }
            socketio.emit('mensajeSecadorasFlexPausar', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    @socketio.on('recibirDatosServerFlexiones')
    def handle_recibir_todos_los_datos():
        global conteoFlexSecadoras, estadoSecadorasFlex, tiempoSecadorasFlex, velocidadFlexiones, flexionesSecadoras, setConteoFlexSecadoras
        # Send all data back to the client
        data_store = {
            'conteoFlexSecadoras': conteoFlexSecadoras,
            'estadoSecadorasFlex': estadoSecadorasFlex,
            'tiempoSecadorasFlex': tiempoSecadorasFlex,
            'velocidadFlexiones': velocidadFlexiones,
            'flexionesSecadoras': flexionesSecadoras,
            'setConteoFlexSecadoras': setConteoFlexSecadoras
        }
        socketio.emit('datosServidorasSecadorasFlex', data_store)

    # EVENTOS SERVIDOR-ESP Secadoras-Flexiones

    @socketio.on('datosEspSecadorasFlex')
    def handle_message(msg):

        global conteoFlexSecadoras, estadoSecadorasFlex, tiempoSecadorasFlex, velocidadFlexiones, flexionesSecadoras, setConteoFlexSecadoras

        if msg:
            conteoFlexSecadoras = msg.get("conteoFlexSecadoras")
            estadoSecadorasFlex = msg.get("estadoSecadorasFlex")
            tiempoSecadorasFlex = msg.get("tiempoSecadorasFlex")
            velocidadFlexiones = msg.get("velocidadFlexiones")
            flexionesSecadoras = msg.get("flexionesSecadoras")
            setConteoFlexSecadoras = msg.get("flexionesSecadoras")

            print(f"conteoFlexSecadoras: {conteoFlexSecadoras}")
            print(f"estadoSecadorasFlex: {estadoSecadorasFlex}")
            print(f"tiempoSecadorasFlex: {tiempoSecadorasFlex}")
            print(f"velocidadFlexiones : {velocidadFlexiones}")
            print(f"flexionesSecadoras : {flexionesSecadoras}")
            print(f"setConteoFlexSecadoras : {setConteoFlexSecadoras}")

            data_store = {
                'conteoFlexSecadoras': conteoFlexSecadoras,
                'estadoSecadorasFlex': estadoSecadorasFlex,
                'tiempoSecadorasFlex': tiempoSecadorasFlex,
                'velocidadFlexiones': velocidadFlexiones,
                'flexionesSecadoras': flexionesSecadoras,
                'setConteoFlexSecadoras': setConteoFlexSecadoras
            }

            socketio.emit('datosServidorasSecadorasFlex', data_store)
