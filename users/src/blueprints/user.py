import hashlib

from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy

from users.src.models.model import Usuario

db = SQLAlchemy()

# Crear el Blueprint para la gestión de usuarios
users_blueprint = Blueprint('users', __name__)


# Ruta para crear un nuevo usuario
@users_blueprint.route('/', methods=['POST'])
def create_user():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    dni = request.json.get("dni", None)
    fullname = request.json.get("fullname", None)
    phoneNumber = request.json.get("phoneNumber", None)

    password_encriptado = hashlib.sha256(request.json["password"]).hexdigest()
    # password_encriptado = hashlib.md5(request.json["password1"].encode('utf-8')).hexdigest()
    nuevo_usuario = Usuario(
        username=username, password=password, sat=password_encriptado, email=email)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return {"mensaje": "cuenta creada con éxito"}, 200

