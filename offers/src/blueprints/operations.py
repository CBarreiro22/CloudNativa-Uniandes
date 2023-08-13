from flask import Flask, jsonify, request, Blueprint
from ..commands.offers import Offers
import os

operations_blueprint = Blueprint('operations', __name__)


@operations_blueprint.route('/offers', methods=['POST'])
def addOffer():
    json = request.get_json()
    postId = json['postId'];
    description = json['description']
    size = ['size']
    fragile = ['fragile']
    offer = ['offer']
    result = Offers(postId=postId,
                    description=description,
                    size=size,
                    fragile=fragile,
                    offer=offer).execute()
    return jsonify(jsonify)
