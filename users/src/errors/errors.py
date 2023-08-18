class ApiError(Exception):
    code = 500  # Código HTTP por defecto
    description = "An error occurred"

    def __init__(self, description=None):
        if description is not None:
            self.description = description


class InsufficientDataError(ApiError):
    code = 400
    description = "Insufficient data provided"


class InvalidCredentials(ApiError):
    code = 401
    description = "Invalid credentials"


class TokenNotHeader(ApiError):
    code = 403
    description = "El token no está en el encabezado de la solicitud"


class UserNotFound(ApiError):
    code = 404
    description = "User not found"


class UserExist(ApiError):
    code = 412
    description = "User already exists"
