import os

from dotenv import load_dotenv
from flask import Flask, jsonify

from .blueprints.operations import operations_blueprint
from .errors.errors import ApiError

loaded = load_dotenv('.env.development')

app = Flask(__name__)
app.register_blueprint(operations_blueprint)


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description,
    }
    return jsonify(response), err.code
