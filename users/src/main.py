import os

from flask import Flask, jsonify

from .blueprints.user import users_blueprint
from .errors.errors import ApiError
app = Flask(__name__)
app.register_blueprint(users_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
