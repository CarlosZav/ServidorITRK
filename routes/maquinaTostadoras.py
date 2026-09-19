def init_maquinaMultifuncional(app, socketio, emit):

    # Estado de las variables de la máquina multifuncional
    estado_multifuncional = {
        "ciclos_totales": 0,
        "ciclos_completados": 0,
        "tiempo_estimado": 0,
        "estado_prueba": "",
        "posicion_inicio": None,
        "posicion_final": None,
    }

    # APP MÓVIL → SERVIDOR → RASPBERRY
    @socketio.on('datosfromMultifuncional')
    def handle_comando_multifuncional(data):
        if not data:
            return

        print(f"[Multifuncional] Comando recibido de app: {data}")

        # Reenviar a la Raspberry (que escucha 'mensajeMultifuncional')
        socketio.emit('mensajeMultifuncional', {'mensaje': data})
        print(f"[Multifuncional] Comando reenviado a Raspberry: {data}")

    # RASPBERRY → SERVIDOR → APP MÓVIL
    @socketio.on('datos_espMultifuncional')
    def handle_datos_esp_multifuncional(data):
        if not data:
            return

        print(f"[Multifuncional] Datos recibidos de Raspberry: {data}")

        estado = data.get("estado")

        if estado == "config":
            estado_multifuncional["ciclos_totales"] = data.get("ciclos", 0)
            estado_multifuncional["ciclos_completados"] = 0
            estado_multifuncional["tiempo_estimado"] = data.get(
                "tiempoEstimado", 0)
            estado_multifuncional["estado_prueba"] = "config"

        elif estado == "cycle":
            estado_multifuncional["ciclos_completados"] = data.get("ciclos", 0)
            estado_multifuncional["estado_prueba"] = "cycle"

        elif estado == "finished":
            estado_multifuncional["estado_prueba"] = "finished"

        elif estado == "position":
            tipo = data.get("tipo")
            valor = data.get("valor")
            if tipo == "start":
                estado_multifuncional["posicion_inicio"] = valor
            elif tipo == "end":
                estado_multifuncional["posicion_final"] = valor

        socketio.emit('datosServidorMultifuncional', data)
        print(f"[Multifuncional] Datos reenviados a app: {data}")

    # APP MÓVIL → SERVIDOR
    @socketio.on('recibirDatosServerMultifuncional')
    def handle_pedir_estado():

        print(
            f"[Multifuncional] App pidió estado actual: {estado_multifuncional}")
        socketio.emit('datosServidorMultifuncional', estado_multifuncional)
