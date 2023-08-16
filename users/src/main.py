import os
from .blueprints.user import users_blueprint
from dotenv import load_dotenv
from flask import Flask, jsonify


from .errors.errors import ApiError
from .models.model import db

loaded = load_dotenv('.env.development')


db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

print(db_host)
print(db_name)
print(db_user)
print(db_port)
print(db_password)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(users_blueprint)
db.init_app(app)


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "mssg": err.description,
        "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
