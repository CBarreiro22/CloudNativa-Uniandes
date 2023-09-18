class ApiError(Exception):
    code = 422
    description = "Default message"
class invalid_token(ApiError):
    code = 401
    description = "el token es invalido"
class no_token(ApiError):
    code = 403
    description = "No hay token en la solicitud"
class internal_server_error (ApiError):
    code = 503
    description = "servicio no disponible "
class json_invalid_new_offer(ApiError):
    code = 400
    description = "el request no cumple con los campos requeridos"
class duplicated_fligh (ApiError):
    code = 412
    description = "El usuario ya tiene una publicación para la misma fecha"

class ivalid_dates (ApiError):
    code = 412
    description = 'Las fechas del trayecto no son válidas'
class invalid_expiration_date (ApiError):
    code = 412
    description = 'La fecha expiración no es válida'