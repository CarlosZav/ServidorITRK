def init_maquinaSecadorasRotaciones(app, socketio, emit):

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

            data_store = {
                'conteo_revSecadorasRot': conteo_revSecadorasRot,
                'estado_pruebaSecadorasRot': estado_pruebaSecadorasRot,
                'tiempo_pruebaSecadorasRot': tiempo_pruebaSecadorasRot,
                'velocidad_SecadorasRot': velocidad_SecadorasRot,
            }

        socketio.emit('datosServerPlanchas', data_store)
