
from flask import Flask, jsonify, request, Blueprint
from ..commands.offers import Offers
from ..models.model import OfferJsonSchema

operations_blueprint = Blueprint('operations', __name__)


@operations_blueprint.route('/offers', methods=['POST'])
def addOffer():
    json = request.get_json()
    postId = json['postId']
    description = json['description']
    size = json['size']
    fragile = json['fragile']
    offer = json['offer']
    offer_result = Offers(userId="ioliva",postId=postId,
                           description=description,
                           size=size,
                           fragile=fragile,
                           offer=int(offer)).execute()
    offer_schema = OfferJsonSchema()
    offer_data = offer_schema.dump(offer_result)

    return jsonify(offer_data)


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
