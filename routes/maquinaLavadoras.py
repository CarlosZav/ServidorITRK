def init_maquinaLavadoras(app, socketio, emit):

    # Variables secadoras-Flexiones
    ciclosLavadoras = 0
    anguloApertura = 0
    velocidadLavadoras = 0
    pausarLavadoras = ""
    conteoCiclosLavadoras = 0
    estadoLavadoras = ""
    tiempoLavadoras = 0
    setVelocidadLavadoras = 0
    setCiclosLavadorasAnimacion = 0
    tiempoPiston1 = 0
    tiempoPiston2 = 0
    tiempoPiston3 = 0
    tiempoPiston4 = 0

    # Funciones entre APP Y SERVIDOR SECADORAS-FLEX

    @socketio.on('datosFromLavadoras')
    def handle_message(data):
        global ciclosLavadoras, anguloApertura, velocidadLavadoras, pausarLavadoras, tiempoPiston1, tiempoPiston2, tiempoPiston3, tiempoPiston4
        # Extrae datos del JSON recibido
        if data:
            ciclosLavadoras = data.get("ciclosLavadoras")
            anguloApertura = data.get("anguloApertura")
            velocidadLavadoras = data.get("velocidadLavadoras")
            pausarLavadoras = data.get("pausarLavadoras")
            tiempoPiston1 = data.get("tiempoPiston1")
            tiempoPiston2 = data.get("tiempoPiston2")
            tiempoPiston3 = data.get("tiempoPiston3")
            tiempoPiston4 = data.get("tiempoPiston4")

            print("seteo Ciclos lavadoras:", ciclosLavadoras)
            print("Angulo Apertura:", anguloApertura)
            print("Velocidad:", velocidadLavadoras)
            print("pausar:", pausarLavadoras)
            print("TiempoPiston 1:", tiempoPiston1)
            print("TiempoPiston 2:", tiempoPiston2)
            print("TiempoPiston 3:", tiempoPiston3)
            print("TiempoPiston 4:", tiempoPiston4)

            # Aquí se manda de una vez a la esp
            datos = {
                'ciclosLavadoras': ciclosLavadoras,
                'anguloApertura': anguloApertura,
                'velocidadLavadoras': velocidadLavadoras,
                'pausarLavadoras': pausarLavadoras,
                'tiempoPiston1': tiempoPiston1,
                'tiempoPiston2': tiempoPiston2,
                'tiempoPiston3': tiempoPiston3,
                'tiempoPiston4': tiempoPiston4,
            }
            # Aquí ya se están mandado los datos iniciales a la esp
            socketio.emit('mensajeLavadoras', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    @socketio.on('datosFromLavadorasPausar')
    def handle_message(data):
        global pausarLavadoras
        # Extrae datos del JSON recibido
        if data:
            pausarLavadoras = data.get("pausarLavadoras")
            print("pausarLavadoras: ", pausarLavadoras)

            # Aquí se manda de una vez a la esp
            datos = {
                'pausarLavadoras': pausarLavadoras,
            }
            socketio.emit('mensajeLavadorasPausar', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    # EVENTOS SERVIDOR-ESP Secadoras-Flexiones

    @socketio.on('datosEspLavadoras')
    def handle_message(msg):

        global conteoCiclosLavadoras, estadoLavadoras, tiempoLavadoras, velocidadLavadoras, ciclosLavadoras
        # Send all data back to the client

        if msg:
            conteoCiclosLavadoras = msg.get("conteoCiclosLavadoras")
            estadoLavadoras = msg.get("estadoLavadoras")
            tiempoLavadoras = msg.get("tiempoLavadoras")
            velocidadLavadoras = msg.get("velocidadLavadoras")
            ciclosLavadoras = msg.get("ciclosLavadoras")

            print(f"conteoCiclosLavadoras: {conteoCiclosLavadoras}")
            print(f"estadoLavadoras: {estadoLavadoras}")
            print(f"tiempoSecadorasFlex: {tiempoLavadoras}")
            print(f"velocidadLavadoras : {velocidadLavadoras}")
            print(f"ciclosLavadoras : {ciclosLavadoras}")

            data_store = {
                'conteoCiclosLavadoras': conteoCiclosLavadoras,
                'estadoLavadoras': estadoLavadoras,
                'tiempoLavadoras': tiempoLavadoras,
                'velocidadLavadoras': velocidadLavadoras,
                'ciclosLavadoras': ciclosLavadoras,
            }

            socketio.emit('datosServidorLavadoras', data_store)
