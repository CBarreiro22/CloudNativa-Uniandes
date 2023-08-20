import os

from dotenv import load_dotenv

from flask import Flask, jsonify

from .blueprints.offer import offer_blueprint
from .errors.errors import ApiError

app = Flask(__name__)
app.register_blueprint(offer_blueprint)


loaded = load_dotenv('.env.development')


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "mssg": err.description,
        "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
