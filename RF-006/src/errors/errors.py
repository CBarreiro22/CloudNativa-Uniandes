class ApiError(Exception):
    code = 422
    description = "Default message"
class invalid_json(ApiError):
    code = 400
    description = "el request no cumple con los campos requeridos"
class invalid_expiration_date(ApiError):
    code = 412
    description = "la fecha de expiración es incorrecta"

class duplicated_credit_card(ApiError):
    code = 409
    description = "La tarjeta de crédito ya esta ingresada"