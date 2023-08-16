class ApiError(Exception):
    code = 401
    description = "Default message"


class TokenNotValid(ApiError):
    code = 401


class EmptyToken(ApiError):
    code = 403


class InvalidBody(ApiError):
    code = 400


class InvalidExpirationDate(ApiError):
    code = 412
    description = "La fecha expiración no es válida"
