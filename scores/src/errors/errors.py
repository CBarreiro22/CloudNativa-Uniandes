class ApiError(Exception):
    code = 500  # Código HTTP por defecto
    description = "Error en el servidor"

    def __init__(self, description=None):
        if description is not None:
            self.description = description


class TokenNotHeaderError(ApiError):
    code = 403
    description = "El token no está en el encabezado de la solicitud"


class InvalidToken(ApiError):
    code = 401
    description = "Token Invalido o esta vencido"
