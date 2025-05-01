def init_maquinaCalentamiento(app, socketio, emit):
    # EVENTOS SERVIDOR-APP Calentamiento

    # Variable global para almacenar el valor del sensor más reciente
    sensor_value = 0
    conteo_ciclos = 0
    estado_ssr = ""
    tiempo_transcurrido = 0
    seteo_ciclos = 0
    seteo_tiempo_apagado = 0
    seteo_tiempo_encendido = 0

    @socketio.on('recibirDatosServer')
    def handle_recibir_todos_los_datos():
        global sensor_value, estado_ssr, conteo_ciclos, tiempo_transcurrido
        # Send all data back to the client
        data_store = {
            'sensor_value': sensor_value,
            'estado_ssr': estado_ssr,
            'conteo_ciclos': conteo_ciclos,
            'tiempo_transcurrido': tiempo_transcurrido
        }
        socketio.emit('datosServidor', data_store)

    @socketio.on('datosfromApp')
    def handle_message(data):
        global seteo_ciclos, seteo_tiempo_apagado, seteo_tiempo_encendido
        # Extrae datos del JSON recibido
        if data:
            seteo_ciclos = data.get("seteo_ciclos")
            seteo_tiempo_apagado = data.get("seteo_tiempo_apagado")
            seteo_tiempo_encendido = data.get("seteo_tiempo_encendido")

            print("Datos recibidos:")
            print("seteo ciclos:", seteo_ciclos)
            print("seteo_tiempo_apagado:", seteo_tiempo_apagado)
            print("seteo_tiempo_encendido:", seteo_tiempo_encendido)

            datos = {
                'seteo_ciclos': seteo_ciclos,
                'tiempo_apagado': seteo_tiempo_apagado,
                'tiempo_prendido': seteo_tiempo_encendido
            }
            socketio.emit('hola2', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

    # EVENTOS SERVIDOR-ESP Calentamiento

    @socketio.on('datos_esp')
    def handle_message(msg):

        global sensor_value, estado_ssr, conteo_ciclos, tiempo_transcurrido

        print(f"Message received: {msg}")

        if msg:
            sensor_value = msg.get("corriente")
            estado_ssr = msg.get("estado_ssr")
            conteo_ciclos = msg.get("conteo_ciclos")
            tiempo_transcurrido = msg.get("tiempo_transcurrido")

            print(f"Corriente: {sensor_value}")
            print(f"Estado ssr: {estado_ssr}")
            print(f"Num de ciclos: {conteo_ciclos}")
            print(f"Tiempo transcurrido: {tiempo_transcurrido}")

            data_store = {
                'sensor_value': sensor_value,
                'estado_ssr': estado_ssr,
                'conteo_ciclos': conteo_ciclos,
                'tiempo_transcurrido': tiempo_transcurrido
            }

            socketio.emit('datosServidor', data_store)

    # @socketio.on('event')
    # def handle_custom_event(data):
        # print(f"Custom event received: {data}")
        # emit('response', {'data': 'Event received by server'}, broadcast=True)
