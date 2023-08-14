import os
from flask import Flask
from dotenv import load_dotenv
from .blueprints.operations import operations_blueprint

loaded = load_dotenv('.env.development')

app = Flask(__name__)
app.register_blueprint(operations_blueprint)


# @app.errorhandler(ApiError)
# def handle_exception(err):
#     response = {
#       "mssg": err.description,
#       "version": os.environ["VERSION"]
#     }
#     return jsonify(response), err.code
