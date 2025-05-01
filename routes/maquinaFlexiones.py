def init_maquinaFlexiones(app, socketio, emit):

    # Variables para prueba de flexiones
    conteo_ciclosFlex = 0
    estado_pruebaFlex = 0
    tiempo_transcurridoFlex = 0
    seteo_ciclosFlexiones = 0
    pausarF = ""
    seteoAnguloA = 0
    seteoAnguloB = 0
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

        emit('response', {
             'data': 'Message received by server'}, broadcast=True)

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
