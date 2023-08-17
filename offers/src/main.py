import os

from .config.config import Config
from .models.model import db

import logging
from flask import Flask, jsonify
from .blueprints.operations import operations_blueprint
from .errors.errors import ApiError

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


env_config = Config('.env.development')

db_user = env_config.get("DB_USER")
db_password = env_config.get("DB_PASSWORD")
db_host = env_config.get("DB_HOST")
db_port = env_config.get("DB_PORT")
db_name = env_config.get("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.url_map.strict_slashes = False

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
