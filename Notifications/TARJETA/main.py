from notificacion_tarjeta import NotificacionTarjeta

def index(request):
    try:
        json=request.get_json()
        tarjeta= NotificacionTarjeta([json.get('email')], '', json.get('RUV'),json.get('lastForDigits'),json.get('status'),json.get('cardHolderName'))
        tarjeta.send_email()
        return '', 200
    except Exception as e:
        return str(e), 500

#tarjeta= NotificacionTarjeta(['bzaratepalomec@gmail.com'], '','1223-2323','1234','VERIFICADAs','Benito Zarate')
#tarjeta.send_email()