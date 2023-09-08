import os

from flask import Flask, jsonify

from scores.src.blueprints.score_operation import scores_blueprint
from .errors.errors import ApiError
app = Flask(__name__)
app.register_blueprint(scores_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description,
      "version": "1.0"
    }
    return jsonify(response), err.code