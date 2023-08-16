
from flask import Flask, jsonify, request, Blueprint

import os

from ..commands import db
from ..commands.offers import Offers

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
