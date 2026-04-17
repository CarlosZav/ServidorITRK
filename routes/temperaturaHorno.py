import time


def init_temperaturaHorno(app, socketio, emit):

    estadoHorno = ""
    tempTermo1 = 0.0
    tempTermo2 = 0.0
    nombreIngeniero = ""
    tiempoPruebaHorno = 0
    pausarHornosTemperatura = "SI"
    tiempoMuestreoTemperatura = 0
    tiempoDato = 0.0
    tiempoDatoInicial = 0.0

    def data_update(tiempoPruebaHorno, tiempoMuestreoTemperatura):

        print("THREAD INICIADO")
        print(float(tiempoMuestreoTemperatura))
        print(float(tiempoPruebaHorno))

        nonlocal tiempoDatoInicial
        nonlocal tiempoDato

        inicio = time.time()
        tiempoDatoInicial = time.time()

        print(inicio)
        print(pausarHornosTemperatura)

        while ((time.time() - inicio) < float(tiempoPruebaHorno)) and (pausarHornosTemperatura == 'NO'):

            tiempoDato = time.time() - tiempoDatoInicial

            socketio.emit('updateDataEsp')
            print("PETICION DE DATOS")

            socketio.sleep(float(tiempoMuestreoTemperatura))

        socketio.emit('updateDataFinished')

    @socketio.on('datosFromTemperaturaHorno')
    def handle_message(data):

        nonlocal nombreIngeniero
        nonlocal tiempoPruebaHorno
        nonlocal pausarHornosTemperatura
        nonlocal tiempoMuestreoTemperatura

        # Extrae datos del JSON recibido
        if data:
            nombreIngeniero = data.get("nombreIngeniero")
            tiempoPruebaHorno = data.get("tiempoPruebaHorno")
            pausarHornosTemperatura = data.get("pausarHornosTemperatura")
            tiempoMuestreoTemperatura = data.get("tiempoMuestreoTemperatura")

            print("nombreIngeniero:", nombreIngeniero)
            print("tiempoPruebaHorno", tiempoPruebaHorno)
            print("pausarHornosTemperatura", pausarHornosTemperatura)
            print("tiempoMuestreoTemperatura", tiempoMuestreoTemperatura)

            # Aquí se manda de una vez a la esp
            datos = {
                'pausarHornosTemperatura': pausarHornosTemperatura,
            }

            socketio.emit('mensajeHornosTemperatura', {'mensaje': datos})
            print("Mensaje enviado a los clientes.")

            socketio.start_background_task(
                data_update, tiempoPruebaHorno, tiempoMuestreoTemperatura)

    @socketio.on('datosTemperaturaHornoPausar')
    def handle_message(data):
        if data:
            pausarHornosTemperatura = data.get("pausarHornosTemperatura")

        if pausarHornosTemperatura == "NO":
            socketio.start_background_task(
                data_update, tiempoPruebaHorno, tiempoMuestreoTemperatura)

    @socketio.on('newDataTemperature')
    def handle_recibir_todos_los_datos(data):

        if data:
            tempTermo1 = data.get("tempTermo1")
            tempTermo2 = data.get("tempTermo2")

            print("Termo 1: ", tempTermo1)
            print("Termo 2:",  tempTermo2)
            print("TiempoDato:", tiempoDato)

        # Send all data back to the client
        data_store = {
            'tempTermo1': tempTermo1,
            'tempTermo2': tempTermo2,
            'tiempoDato': tiempoDato,
        }
        socketio.emit('dataTemperatureApp', data_store)
