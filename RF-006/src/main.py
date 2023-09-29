import threading

from dotenv import load_dotenv
from flask import Flask, jsonify

from .blueprints.operations import operations_blueprint
from .errors.errors import ApiError
from .polling.polling import polling

loaded = load_dotenv('.env.development')

app = Flask(__name__)
app.register_blueprint(operations_blueprint)
polling_lock = threading.Lock()
polling_started = False


def start_polling():
    global polling_started
    with polling_lock:
        if not polling_started:
            polling_thread = threading.Thread(target=polling)
            polling_thread.daemon = True
            polling_thread.start()
            polling_started = True

start_polling()

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description,
    }
    return jsonify(response), err.code
