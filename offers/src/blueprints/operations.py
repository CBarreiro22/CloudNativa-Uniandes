import logging

import requests

from flask import jsonify, request, Blueprint
from jsonschema import ValidationError
from jsonschema.validators import validate
from ..commands.offers import Offers
from ..commands.offersFilter import OffersFilter
from ..config.config import Config
from ..errors.errors import no_token, json_invalid_new_offer, invalid_token
from ..models.model import newOfferResponseJsonSchema, OfferJsonSchema

operations_blueprint = Blueprint('operations', __name__)
new_offer_schema = {
    "type": "object",
    "properties":{
        "postId": {"type": "string"},
        "description": {"type": "string"},
        "size": {"type": "string"},
        "fragile": {"type": "boolean"},
        "offer": {"type": "integer"}
    },
    "required": ["postId","description","size","fragile","offer"],
}

@operations_blueprint.route('/offers', methods=['POST'])
def addOffer():
    json_data = request.get_json()
    token = validate_token(request)

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
    offer_schema = OfferJsonSchema()

    offer_data = offer_schema.dump(offer_result)

    return jsonify(offer_data)


def validate_token(request):
    token = request.headers.get('Authorization')
    if token == None or token == '':
        raise no_token
    return token


@operations_blueprint.route('/offers', methods=['GET'])
def get_offers():
    token = validate_token(request)
    owner = request.args.get('owner')
    postId = request.args.get('postId')
    no_user = owner == None or owner == ''
    print (f'owner: {postId} user: {owner}' )
    no_post_id = postId == None or postId ==''
    user_id = get_user_id(token)
    if not no_user and owner.upper() == "ME":
        owner = user_id
    offers_list = OffersFilter(user_id=owner,
                               post_id=postId,no_user=no_user,
                               no_post_id=no_post_id).execute()
    offer_schema = newOfferResponseJsonSchema()
    offers_data = [offer_schema.dump(r) for r in offers_list]
    return jsonify(offers_data)

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


def validate_new_offer_schema(json_data):
    try:
        validate (json_data, new_offer_schema)

    except ValidationError as e:
        raise json_invalid_new_offer
