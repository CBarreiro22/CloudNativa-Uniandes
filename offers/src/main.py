import os,logging

from dotenv import load_dotenv

from .commands import db
from .config import config

loaded = load_dotenv('.env.development')

from flask import Flask, jsonify
from .blueprints.operations import operations_blueprint
from .errors.errors import ApiError


# Configure the root logger
logging.basicConfig(level=logging.DEBUG,  # Set the minimum log level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='app.log',  # Log to a file
                    filemode='w')

# Create a console handler and set the level to DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and attach it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the root logger
logging.getLogger('').addHandler(console_handler)

app: Flask = Flask(__name__)
app.register_blueprint(operations_blueprint)
app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_DATABASE_URI'] = config.Config.SQLALCHEMY_DATABASE_URI
app.url_map.strict_slashes = False

db.init_app()
db.create_all()

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
