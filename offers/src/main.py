import os

from dotenv import load_dotenv

from flask import Flask, jsonify

from .errors.errors import ApiError

app = Flask(__name__)


def initialize_blueprints(app):
    # Importa los blueprints y configúralos
    from .blueprints.offer import offer_blueprint

    # Registra los blueprints en la instancia de app
    app.register_blueprint(offer_blueprint)


initialize_blueprints(app)

loaded = load_dotenv('.env.development')


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "mssg": err.description,
        "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
