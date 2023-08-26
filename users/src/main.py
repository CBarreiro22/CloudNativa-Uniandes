import os

from .blueprints.user import users_blueprint
from dotenv import load_dotenv
from flask import Flask, jsonify
from .errors.errors import ApiError
os.getenv('ENV')
app = Flask(__name__)
app.register_blueprint(users_blueprint)
loaded = load_dotenv('.env.development')

print(os.environ["VERSION"])
@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "mssg": err.description,
        "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
