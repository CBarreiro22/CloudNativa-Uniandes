from functools import wraps

from flask import Blueprint
from flask import request

from ..commands.offer_service import OfferService
from ..commands.post_service import PostService
from ..commands.user_service import UserService
from ..commands.score_service import ScoreService

# from ..models.model import init_db
# from ..models.post import PostJsonSchema

operations_blueprint = Blueprint('operations', __name__)


# init_db()
# post_schema = PostJsonSchema()


def validate_request_body(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        json_data = request.get_json()
        required_fields = ['description', 'size', 'fragile', 'offer']
        for field in required_fields:
            if field not in json_data or json_data[field] is None:
                return '', 400
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

        request.user_id = user_id
        request.token = token
        return func(*args, **kwargs)

    return decorated


@operations_blueprint.route('/rf004/posts/<string:post_id>/offers', methods=['POST'])
@require_token
@validate_request_body
def create_offer_of_post(post_id):
    json = request.get_json()
    user_id = request.user_id
    route_id, error_post_service = PostService.get_post_information(request.token, user_id, post_id)
    if error_post_service:
        return '', error_post_service
    offer_response, error_offer_service = OfferService.create_offer(request.token, json, post_id)
    if error_offer_service:
        return '', error_offer_service
    offer_id = offer_response.get("id")
    offer_score, error_score_service = ScoreService.calculate_score_offer(request.token, offer_id, route_id)
    if error_score_service:
        return '', error_score_service
    response_body = {
        "data": {
            "id": offer_id,
            "userId": user_id,
            "createdAt": offer_response.get("createdAt"),
            "postId": post_id
        },
        "msg": "Se creo la oferta dada la publicación con esta utilidad: " + str(offer_score)
    }
    return response_body, 201