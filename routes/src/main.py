import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from .blueprints.operations import operations_blueprint
from .errors.errors import ApiError

loaded = load_dotenv('.env.development')

app = Flask(__name__)
app.register_blueprint(operations_blueprint)


@app.errorhandler(ApiError)
def handle_exception(err):
    if err.description == '':
        return err.description, err.code
    response = {
        "mssg": err.description,
        "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
