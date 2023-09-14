import os

from dotenv import load_dotenv
from flask import Flask, jsonify

from .blueprints.operations import operations_blueprint

loaded = load_dotenv('.env.development')

app = Flask(__name__)
app.register_blueprint(operations_blueprint)


def handle_exception(err):
    response = {
        "mssg": err.description,
        "version": os.environ["VERSION"]
    }
    return jsonify(response), Exception(err.code)
