import datetime
from datetime import datetime
from functools import wraps

from flask import Blueprint, request, jsonify

from src.models.post import Post

operations_blueprint = Blueprint('operations', __name__)


def is_invalid_iso8601_or_past(date_string):
    try:
        # expire_at_datetime = datetime.fromisoformat(date_string)
        current_datetime = datetime.now()
        return date_string <= current_datetime.isoformat()
    except ValueError:
        return True


def validate_request_body(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        json_data = request.get_json()
        if not json_data:
            return '', 400

        expireAt = json_data.get("expireAt")
        if is_invalid_iso8601_or_past(expireAt):
            return '', 412

        return func(*args, **kwargs)

    return decorated


def require_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if token is None or not token.startswith('Bearer '):
            return '', 403
        else:
            # user_id = UserService.get_user_information(token)
            user_id = "2324323232"
            if user_id is None:
                return '', 401

        # Guardar el user_id en el contexto del request
        request.user_id = user_id

        return func(*args, **kwargs)

    return decorated


@operations_blueprint.route('/posts', methods=['POST'])
@require_token
@validate_request_body
def divide():
    json = request.get_json()

    # Acceder al user_id guardado en el contexto del request
    user_id = request.user_id

    # Gaurdar objeto en DBA

    post_entity = Post("expireAt", user_id, json.get("expireAt"))

    # Crear el JSON de respuesta
    response_data = {
        "id": "post_id",
        "userId": user_id,  # Obtener el user_id del contexto del request
        "createdAt": datetime.now().isoformat()  # Convertir la fecha y hora a formato ISO 8601
    }

    return jsonify(response_data), 200
