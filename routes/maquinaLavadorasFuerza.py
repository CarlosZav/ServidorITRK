def init_maquinaLavadorasFuerza(app, socketio, emit):

    # Variables secadoras-Flexiones
    ciclosLavadorasFuerza = 0
    anguloApertura = 45
    velocidadLavadorasFuerza = 0
    pausarLavadorasFuerza = ""
    conteoCiclosLavadorasFuerza = 0
    estadoLavadorasFuerza = ""
    tiempoLavadorasFuerza = 0
    fuerzaInicial = 0
    fuerzaFinal = 0
    fuerzaEjercida = 0

    # Funciones entre APP Y SERVIDOR SECADORAS-FLEX

    @socketio.on('datosFromLavadorasFuerza')
    def handle_message(data):
        global ciclosLavadorasFuerza, velocidadLavadorasFuerza, pausarLavadorasFuerza, fuerzaInicial, fuerzaFinal
        # Extrae datos del JSON recibido
        if data:
            ciclosLavadorasFuerza = data.get("ciclosLavadorasFuerza")
            velocidadLavadorasFuerza = data.get("velocidadLavadorasFuerza")
            pausarLavadorasFuerza = data.get("pausarLavadorasFuerza")
            fuerzaInicial = data.get("fuerzaInicial")
            fuerzaFinal = data.get("fuerzaFinal")

            print("seteo Ciclos lavadoras fuerza:", ciclosLavadorasFuerza)
            print("Velocidad:", velocidadLavadorasFuerza)
            print("pausar:", pausarLavadorasFuerza)
            print("Fuerza Final:", fuerzaFinal)
            print("Fuerza Inicial:", fuerzaInicial)

            # Aquí se manda de una vez a la esp
            datos = {
                'ciclosLavadorasFuerza': ciclosLavadorasFuerza,
                'velocidadLavadorasFuerza': velocidadLavadorasFuerza,
                'pausarLavadorasFuerza': pausarLavadorasFuerza,
                'fuerzaInicial': fuerzaInicial,
                'fuerzaFinal': fuerzaFinal,
            }
            # Aquí ya se están mandado los datos iniciales a la esp
            socketio.emit('mensajeLavadorasFuerza', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    @socketio.on('datosFromLavadorasPausarFuerza')
    def handle_message(data):
        global pausarLavadorasFuerza
        # Extrae datos del JSON recibido
        if data:
            pausarLavadorasFuerza = data.get("pausarLavadorasFuerza")
            print("pausarLavadorasFuerza: ", pausarLavadorasFuerza)

            # Aquí se manda de una vez a la esp
            datos = {
                'pausarLavadorasFuerza': pausarLavadorasFuerza,
            }
            socketio.emit('mensajeLavadorasPausarFuerza', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    # EVENTOS SERVIDOR-ESP

    @socketio.on('datosEspLavadorasFuerza')
    def handle_message(msg):

        global conteoCiclosLavadorasFuerza, estadoLavadorasFuerza, tiempoLavadorasFuerza, velocidadLavadorasFuerza, ciclosLavadorasFuerza, fuerzaEjercida, fuerzaFinal
        # Send all data back to the client

        if msg:
            conteoCiclosLavadorasFuerza = msg.get(
                "conteoCiclosLavadorasFuerza")
            estadoLavadorasFuerza = msg.get("estadoLavadorasFuerza")
            tiempoLavadorasFuerza = msg.get("tiempoLavadorasFuerza")
            velocidadLavadorasFuerza = msg.get("velocidadLavadorasFuerza")
            fuerzaEjercida = msg.get("fuerzaEjercida")
            ciclosLavadorasFuerza = msg.get("ciclosLavadorasFuerza")
            fuerzaFinal = msg.get("fuerzaFinal")

            print(
                f"conteoCiclosLavadorasFuerza: {conteoCiclosLavadorasFuerza}")
            print(f"estadoLavadoras: {estadoLavadorasFuerza}")
            print(f"tiempo: {tiempoLavadorasFuerza}")
            print(f"fuerza Ejercida : {fuerzaEjercida}")
            print(f"ciclos Lavadoras Fuerza : {ciclosLavadorasFuerza}")
            print(f"Fuerza Final : {fuerzaFinal}")

            data_store = {
                'conteoCiclosLavadorasFuerza': conteoCiclosLavadorasFuerza,
                'estadoLavadorasFuerza': estadoLavadorasFuerza,
                'tiempoLavadorasFuerza': tiempoLavadorasFuerza,
                'velocidadLavadorasFuerza': velocidadLavadorasFuerza,
                'fuerzaEjercida': fuerzaEjercida,
                'ciclosLavadorasFuerza': ciclosLavadorasFuerza,
                'fuerzaFinal': fuerzaFinal,
            }

            socketio.emit('datosServidorLavadorasFuerza', data_store)
