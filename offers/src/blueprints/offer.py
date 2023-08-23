import logging
import os
import re
from functools import wraps

import requests

from flask import jsonify, request, Blueprint
from jsonschema import ValidationError
from jsonschema.validators import validate

from ..commands.offers import Offers
from ..commands.offersOperations import OffersOperations
from ..commands.userService import UserService

from ..errors.errors import json_invalid_new_offer, invalid_token, no_offer_found, uuid_not_valid
from ..models.offer import newOfferResponseJsonSchema, OfferJsonSchema

DELETE = 'DELETE'

offer_blueprint = Blueprint('offer', __name__)

new_offer_schema = {
    "type": "object",
    "properties": {
        "postId": {"type": "string"},
        "description": {"type": "string"},
        "size": {"type": "string"},
        "fragile": {"type": "boolean"},
        "offer": {"type": "integer"}
    },
    "required": ["postId", "description", "size", "fragile", "offer"],
}


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


@offer_blueprint.route('/offers', methods=['POST'])
@require_token
def addOffer() -> object:
    json_data = request.get_json()
    user_id = request.user_id
    validate_new_offer_schema(json_data=json_data)
    post_id = json_data['postId']
    description = json_data['description']
    size = json_data['size']
    offer = json_data['offer']
    fragile = json_data['fragile']
    logging.info(f'adding user {user_id}')
    offer_result = Offers(user_id=user_id,
                          post_id=post_id,
                          description=description,
                          size=size,
                          fragile=parse_bool(fragile),
                          offer=int(offer)).execute()
    offer_schema = newOfferResponseJsonSchema()
    offer_data = offer_schema.dump(offer_result)

    return jsonify(offer_data),201


@offer_blueprint.route('/offers', methods=['GET'])
@require_token
def get_offers():
    owner = request.args.get('owner')
    post_id = request.args.get('post')
    get_all = (owner is None and post_id is None)

    user_id = request.user_id
    if not owner is None and owner.upper() == "ME":
        owner = user_id
    if get_all:
        offers_list = OffersOperations().execute()
    else:
        offers_list = OffersOperations(user_id=owner,
                                   post_id=post_id).execute()
    offer_schema = OfferJsonSchema()
    offers_data = [offer_schema.dump(r) for r in offers_list]
    return jsonify(offers_data)


@offer_blueprint.route('/offers/<id>', methods=['GET', 'DELETE'])
@require_token
def get_offerById(id: object) -> object:
    if is_not_valid_uuid(id):
        raise uuid_not_valid

    if request.method == DELETE:
        OffersOperations(operation=DELETE, offer_id=id).execute()
        return jsonify({"msg": "la oferta fue eliminada"}), 200
    if request.method == 'GET':
        offer = OffersOperations(offer_id=id).execute()
        if not offer:
            raise no_offer_found
        offer_schema = OfferJsonSchema()
        offer_data = offer_schema.dump(offer)
        return jsonify(offer_data)


@offer_blueprint.route('/offers/ping', methods=['GET'])
def ping():
    return "pong", 200


@offer_blueprint.route('/offers/reset', methods=['POST'])
def reset():
    return OffersOperations(operation='RESET').execute()


def get_user_id(token):
    users_path = os.get('USERS_PATH')
    logging.info(users_path)
    logging.info(token)
    headers = {'Authorization': token}
    response = requests.get(users_path + '/users/me', headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('id')
    if response.status_code == 401:
        raise invalid_token
    raise invalid_token


def parse_bool(s):
    if isinstance(s, bool):
        return s


def is_not_valid_uuid(input_string):
    if input_string is None:
        return True
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    return not bool(uuid_pattern.match(input_string))


def validate_new_offer_schema(json_data):
    try:
        validate(json_data, new_offer_schema)

    except ValidationError as e:
        raise json_invalid_new_offer
