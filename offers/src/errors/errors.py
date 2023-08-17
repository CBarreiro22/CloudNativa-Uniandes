class ApiError(Exception):
    code = 422
    description = "Default message"

class invalid_token(ApiError):
    code = 401
    description = "El token no es válido o está vencido."
class no_token(ApiError):
    code = 403
    description = "No hay token en la solicitud"
class json_invalid_new_offer(ApiError):
    code = 400
    description = "el request no cumple con los campos requeridos"
class new_offer_business_errors(ApiError):
    code = 412
    description = "verificar el tamaño o la oferta"
