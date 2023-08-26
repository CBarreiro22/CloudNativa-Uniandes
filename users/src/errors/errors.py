class ApiError(Exception):
    code = 500  # Código HTTP por defecto
    description = "An error occurred"

    def __init__(self, description=None):
        if description is not None:
            self.description = description


class InsufficientDataError(ApiError):
    code = 400
    description = "Insufficient data provided"


class InvalidCredentialsError(ApiError):
    code = 401
    description = "Invalid credentials"


class TokenNotHeaderError(ApiError):
    code = 403
    description = "El token no está en el encabezado de la solicitud"


class UserNotFound(ApiError):
    code = 404
    description = "User not found"


class UserExistError(ApiError):
    code = 412
    description = "El usuario ya existe"


class InternalServerError(ApiError):
    code = 500
    description = "Internal Error"
