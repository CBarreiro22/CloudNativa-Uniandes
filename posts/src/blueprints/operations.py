from datetime import datetime

from flask import Flask, jsonify, request, Blueprint
from functools import wraps

from src.errors.errors import *

operations_blueprint = Blueprint('operations', __name__)


def is_invalid_iso8601_or_past(date_string):
    try:
        expire_at_datetime = datetime.fromisoformat(date_string)
        current_datetime = datetime.now()
        return expire_at_datetime <= current_datetime
    except ValueError:
        return True


def validate_request_body(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        json_data = request.get_json()
        if not json_data:
            raise InvalidBody

        expireAt = json_data.get("expireAt")
        if is_invalid_iso8601_or_past(expireAt):
            raise InvalidExpirationDate

        return func(*args, **kwargs)

    return decorated


def require_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if token is None or not token.startswith('Bearer '):
            raise EmptyToken
        # else:
        #     user_id = UserService.get_user_information(token)
        #     if user_id is None:
        #         raise TokenNotValid
        #
        # # Guardar el user_id en el contexto del request
        # request.user_id = user_id

        return func(*args, **kwargs)

    return decorated


@operations_blueprint.route('/posts', methods=['POST'])
@require_token
@validate_request_body
def divide():
    json = request.get_json()

    # Acceder al user_id guardado en el contexto del request
    # user_id = request.user_id

    # Gaurdar objeto en DBA

    # Crear el JSON de respuesta
    response_data = {
        "id": "post_id",
        "userId": "request.user_id",  # Obtener el user_id del contexto del request
        "createdAt": datetime.now().isoformat()  # Convertir la fecha y hora a formato ISO 8601
    }

    return jsonify(response_data), 200
