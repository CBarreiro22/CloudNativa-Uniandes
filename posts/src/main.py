from __future__ import absolute_import
from dotenv import load_dotenv
from flask import Flask, jsonify

from src.blueprints.operations import operations_blueprint
from src.errors.errors import ApiError
import os

loaded = load_dotenv('.env.development')

app = Flask(__name__)
app.register_blueprint(operations_blueprint)


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "mssg": err.description,
        "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
