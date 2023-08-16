import hashlib

from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy

from users.src.models.model import db, Users

# Crear el Blueprint para la gestión de usuarios
users_blueprint = Blueprint('users', __name__)


# Ruta para crear un nuevo usuario
@users_blueprint.route('/users', methods=['POST'])
def create_user():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    dni = request.json.get("dni", None)
    fullname = request.json.get("fullname", None)
    phoneNumber = request.json.get("phoneNumber", None)

    password_encoded = password.encode('utf-8')
    password_encriptado = hashlib.sha256(password_encoded).hexdigest()
    # password_encriptado = hashlib.md5(request.json["password1"].encode('utf-8')).hexdigest()
    nuevo_usuario = Users(
        username=username, password=password, salt=password_encriptado, email=email, phone_number=phoneNumber, dni=dni,
        full_name=fullname)
    db.session.add(nuevo_usuario)
    db.session.commit()

    user = db.session.query(Users).filter_by(username=username).first()
    if user is not None:
        user.status = "VERIFICADO"
    db.session.close()

    return {"mensaje": "cuenta creada con éxito"}, 200
