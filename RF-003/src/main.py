from dotenv import load_dotenv
from flask import Flask, jsonify

from .erros.errors import ApiError

from .blueprints.rf003 import rf003_blueprint

loaded = load_dotenv('RF-003/.env.development')

app = Flask (__name__)
app.register_blueprint (rf003_blueprint)



@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "mssg": err.description,
    }
    return jsonify(response), err.code
