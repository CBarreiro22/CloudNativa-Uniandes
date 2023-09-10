class ApiError(Exception):
    code = 422
    description= "Default message"

class MissingToken(ApiError):
    code = 403
    description=""

class InvalidToken(ApiError):
    code=401
    descrption=""