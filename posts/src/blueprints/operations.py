import datetime
from datetime import datetime
from functools import wraps
from flask import Blueprint, request, jsonify
from src.models.model import db_session, init_db
from src.models.post import Post, PostJsonSchema

operations_blueprint = Blueprint('operations', __name__)

init_db()
post_schema = PostJsonSchema()

def is_invalid_iso8601_or_past(date_string):
    try:
        current_datetime = datetime.now()
        return date_string <= current_datetime.isoformat()
    except ValueError:
        return True


def validate_request_body(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        json_data = request.get_json()
        required_fields = ['routeId', 'expireAt']
        for field in required_fields:
            if field not in json_data or json_data[field] is None:
                return '', 400

        expireAt = json_data.get("expireAt")
        if is_invalid_iso8601_or_past(expireAt):
            return 'La fecha expiración no es válida', 412

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

    post_entity = Post(json.get("routeId"), user_id, json.get("expireAt"))
    db_session.add(post_entity)
    db_session.commit()

    # Crear el JSON de respuesta

    response_data = {
        "id": post_entity.id,
        "userId": user_id,
        "createdAt": post_entity.createdAt
    }

    return jsonify(response_data), 201
