def init_maquinaPlanchas(app, socketio, emit):

    # Variables para prueba de planchas
    conteoCiclosPlanchas = 0
    estadoPruebaPlanchas = 0
    tiempoTranscurridoPlanchas = 0
    setCiclosPlanchas = 0
    pausarPlanchas = ""
    setTiempoElevadoPlanchas = 0
    setTiempoBajoPlanchas = 0

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
        emit('response', {
             'data': 'Message received by server'}, broadcast=True)

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
