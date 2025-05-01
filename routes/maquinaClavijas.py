def init_maquinaClavijas(app, socketio, emit):
    # EVENTOS SERVIDOR-APP Calentamiento

    # Variable global para almacenar el valor del sensor más reciente
    sensorValueC = 0
    conteoCiclosC = 0
    estadoSsrC = ""
    tiempoTranscurridoC = 0
    seteoCiclosC = 0
    setTiempoApagadoC = 0
    setTiempoEncendidoC = 0

    @socketio.on('recibirDatosServerC')
    def handle_recibir_todos_los_datos():
        global sensorValueC, estadoSsrC, conteoCiclosC, tiempoTranscurridoC
        # Send all data back to the client
        data_store = {
            'sensorValueC': sensorValueC,
            'estadoSsrC': estadoSsrC,
            'conteoCiclosC': conteoCiclosC,
            'tiempoTranscurridoC': tiempoTranscurridoC
        }
        socketio.emit('datosServidorC', data_store)

    @socketio.on('datosfromAppC')
    def handle_message(data):
        global seteoCiclosC, setTiempoApagadoC, setTiempoEncendidoC
        # Extrae datos del JSON recibido
        if data:
            seteoCiclosC = data.get("seteoCiclosC")
            setTiempoApagadoC = data.get("setTiempoApagadoC")
            setTiempoEncendidoC = data.get("setTiempoEncendidoC")

            print("Datos recibidos:")
            print("seteo ciclos:", seteoCiclosC)
            print("setTiempoApagadoC:", setTiempoApagadoC)
            print("setTiempoEncendidoC:", setTiempoEncendidoC)

            datos = {
                'seteoCiclosC': seteoCiclosC,
                'setTiempoApagadoC': setTiempoApagadoC,
                'setTiempoEncendidoC': setTiempoEncendidoC
            }
            socketio.emit('datosSetC', {'datosClavijas': datos})
            print("Mensaje enviado a los clientes.")

    # EVENTOS SERVIDOR-ESP Calentamiento

    @socketio.on('datosEspC')
    def handle_message(msg):

        global sensorValueC, estadoSsrC, conteoCiclosC, tiempoTranscurridoC

        print(f"Message received: {msg}")

        if msg:
            sensorValueC = msg.get("corriente")
            estadoSsrC = msg.get("estadoSsrC")
            conteoCiclosC = msg.get("conteoCiclosC")
            tiempoTranscurridoC = msg.get("tiempoTranscurridoC")

            print(f"Corriente: {sensorValueC}")
            print(f"Estado ssr: {estadoSsrC}")
            print(f"Num de ciclos: {conteoCiclosC}")
            print(f"Tiempo transcurrido: {tiempoTranscurridoC}")

            data_store = {
                'sensorValueC': sensorValueC,
                'estadoSsrC': estadoSsrC,
                'conteoCiclosC': conteoCiclosC,
                'tiempoTranscurridoC': tiempoTranscurridoC
            }

            socketio.emit('datosServidorC', data_store)

    # @socketio.on('event')
    # def handle_custom_event(data):
        # print(f"Custom event received: {data}")
        # emit('response', {'data': 'Event received by server'}, broadcast=True)
