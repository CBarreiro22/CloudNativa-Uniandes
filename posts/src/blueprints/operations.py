import datetime
import uuid
from datetime import datetime, timezone
from functools import wraps

from flask import Blueprint, jsonify
from flask import request

from ..commands.user_service import UserService
from ..models.model import db_session, init_db, reset_db
from ..models.post import Post, PostJsonSchema

operations_blueprint = Blueprint('operations', __name__)

init_db()
post_schema = PostJsonSchema()
ISO_FORMATTER = "%Y-%m-%dT%H:%M:%S.%fZ"

def is_invalid_iso8601_or_past(date):
    if isinstance(date, str):
        try:
            date_str_without_decimals = date.split('.')[0]
            date = datetime.strptime(date_str_without_decimals, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return True
    current_datetime = datetime.now(timezone.utc).replace(tzinfo=None)
    try:
        return date <= current_datetime
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
            return jsonify({"msg": "La fecha expiración no es válida"}), 412

        return func(*args, **kwargs)

    return decorated


def require_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if token is None or not token.startswith('Bearer '):
            return '', 403
        else:
            user_id = UserService.get_user_information(token)
            if user_id is None:
                return '', 401

        # Guardar el user_id en el contexto del request
        request.user_id = user_id

        return func(*args, **kwargs)

    return decorated


@operations_blueprint.route('/posts', methods=['POST'])
@require_token
@validate_request_body
def create_post():
    json = request.get_json()
    user_id = request.user_id
    expire_at_date = parse_iso_date(json.get("expireAt"))

    post_entity = Post(route_id=json.get("routeId"), user_id=user_id, expire_at=expire_at_date)
    db_session.add(post_entity)
    db_session.commit()

    response_data = {
        "id": post_entity.id,
        "userId": user_id,
        "createdAt": post_entity.createdAt
    }
    return jsonify(response_data), 201


def validate_uuid_parameter(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        id_value = kwargs.get('id')
        if id_value is None:
            return '', 400

        try:
            uuid.UUID(id_value)
        except ValueError:
            return '', 400

        return func(*args, **kwargs)

    return decorated


@operations_blueprint.route('/posts/<string:id>', methods=['DELETE'])
@require_token
@validate_uuid_parameter
def delete_post(id):
    result_post = Post.query.filter(Post.id == id).first()
    if result_post is None:
        return '', 404
    db_session.delete(result_post)
    db_session.commit()

    return jsonify({
        "msg": "la publicación fue eliminada"
    }), 200


@operations_blueprint.route('/posts/<string:id>', methods=['GET'])
@require_token
@validate_uuid_parameter
def get_post(id):
    result_post = Post.query.filter(Post.id == id).first()
    if result_post is None:
        return '', 404
    return jsonify(post_schema.dump(result_post)), 200


def validate_posts_parameter(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        expire = request.args.get('expire')
        if expire is not None and expire not in ['true', 'false']:
            return '', 400
        return func(*args, **kwargs)

    return decorated


@operations_blueprint.route('/posts', methods=['GET'])
@require_token
@validate_posts_parameter
def get_posts():
    args = request.args
    route = args.get('route') or None
    owner = args.get('owner') or None
    expire = args.get('expire') or None
    if expire is None and route is None and owner is None:
        result = [post_schema.dump(p) for p in Post.query.all()]
    else:
        result = [
            post_schema.dump(p) for p in Post.query.all() if
            (
                (expire is None or (expire.lower() == "true" and is_invalid_iso8601_or_past(p.expireAt))
                 or
                 (expire.lower() == "false" and not is_invalid_iso8601_or_past(p.expireAt))
                 )
            ) and
            (
                (route is None or p.routeId == route)
            ) and
            (
                    (owner is None) or
                    (owner == 'me' and p.userId == request.user_id) or
                    (owner != 'me' and p.userId == owner)
            )
        ]
    return jsonify(result), 200


@operations_blueprint.route('/posts/reset', methods=['POST'])
def reset_database():
    reset_db()
    return jsonify({
        "msg": "Todos los datos fueron eliminados"
    }), 200


@operations_blueprint.route('/posts/ping', methods=['GET'])
def check_health():
    return 'pong', 200
def parse_iso_date(date_str):
    try:
        return datetime.strptime(date_str, ISO_FORMATTER)
    except ValueError:
        return None

def is_valid_date_route(start_date, end_date):
    if start_date < datetime.now()  or end_date < datetime.now():
        return False
    if end_date < start_date:
        return False
    return True