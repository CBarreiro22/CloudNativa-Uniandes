import logging, requests, re

from flask import jsonify, request, Blueprint, app, make_response
from jsonschema import ValidationError
from jsonschema.validators import validate
from ..commands.offers import Offers
from ..commands.offersOperations import OffersOperations
from ..config.config import Config
from ..errors.errors import no_token, json_invalid_new_offer, invalid_token, no_offer_found, uuid_not_valid
from ..models.model import newOfferResponseJsonSchema, OfferJsonSchema

DELETE = 'DELETE'

operations_blueprint = Blueprint('operations', __name__)

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


@operations_blueprint.route('/offers', methods=['POST'])
def addOffer() -> object:
    json_data = request.get_json()
    token = validate_token()

    validate_new_offer_schema(json_data=json_data)

    post_id = json_data['postId']
    description = json_data['description']
    size = json_data['size']
    fragile = json_data['fragile']
    offer = json_data['offer']
    user_id = get_user_id(token)
    logging.info(f'adding user {user_id}')
    offer_result = Offers(user_id=user_id,
                          post_id=post_id,
                          description=description,
                          size=size,
                          fragile=parse_bool(fragile),
                          offer=int(offer)).execute()
    offer_schema = newOfferResponseJsonSchema()
    offer_data = offer_schema.dump(offer_result)

    return jsonify(offer_data)


def validate_token():
    token = request.headers.get('Authorization')
    if token == None or token == '':
        raise no_token
    return token


@operations_blueprint.route('/offers', methods=['GET'])
def get_offers():
    token = validate_token()
    owner = request.args.get('owner')
    post_id = request.args.get('postId')

    user_id = get_user_id(token)
    if not owner is None and owner.upper() == "ME":
        owner = user_id
    offers_list = OffersOperations(user_id=owner,
                                   post_id=post_id).execute()
    offer_schema = newOfferResponseJsonSchema()
    offers_data = [offer_schema.dump(r) for r in offers_list]
    return jsonify(offers_data)


@operations_blueprint.route('/offers/<id>', methods=['GET', DELETE])
def get_offerById(id: object) -> object:
    if is_not_valid_uuid(id):
        raise uuid_not_valid
    token = validate_token()
    get_user_id(token)
    if request.method == 'GET':
        offer = OffersOperations(offer_id=id).execute()
        if not offer:
            raise no_offer_found
        offer_schema = newOfferResponseJsonSchema()
        offer_data = offer_schema.dump(offer)
        return jsonify(offer_data)
    if request.method == DELETE:
        OffersOperations(operation=DELETE, offer_id=id).execute()
        return jsonify({"msg": "la oferta fue eliminada"}), 200


@operations_blueprint.route('/offers/ping', methods=['GET'])
def ping():
    return "pong", 200

@operations_blueprint.route('/offers/reset', methods=['POST'])
def reset():

    return OffersOperations(operation='RESET').execute()

def get_user_id(token):
    users_path = Config('.env.development').get('USERS_PATH')
    logging.info(users_path)
    logging.info(token)
    headers = {'Authorization': token}
    response = requests.get(users_path, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('id')
    if response.status_code == 401:
        raise invalid_token
    raise invalid_token


def parse_bool(s):
    if isinstance(s, bool):
        return s
    s_lower = s.lower()
    if s_lower in ("true", "yes", "1"):
        return True
    elif s_lower in ("false", "no", "0"):
        return False
    else:
        raise ValueError(f"Invalid boolean string: {s}")


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
