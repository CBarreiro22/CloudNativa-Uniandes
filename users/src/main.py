import os

from flask_sqlalchemy import SQLAlchemy

from .blueprints.user import users_blueprint
from dotenv import load_dotenv
from flask import Flask, jsonify
from .errors.errors import ApiError

app = Flask(__name__)
app.register_blueprint(users_blueprint)
loaded = load_dotenv('.env.development')


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "mssg": err.description,
        "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
