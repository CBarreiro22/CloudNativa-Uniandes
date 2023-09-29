from notificacion_usuario import NotificacionUsuario

def index(request):
    try:
        json=request.get_json()
        tarjeta= NotificacionUsuario([json.get('email')], '', json.get('RUV'),json.get('username'),json.get('dni'),json.get('fullname'),json.get('phonenumber'),json.get('status'))
        tarjeta.send_email()
        return '', 200
    except Exception as e:
        return str(e), 500

usuario= NotificacionUsuario(['bzaratepalomec@gmail.com'], '','','','','','','')
usuario.send_email()