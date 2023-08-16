import hashlib
import json
from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from users.src.models.model import db, Users
import uuid

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

    nuevo_usuario = Users(
        username=username, password=password, salt=password_encriptado, email=email, phone_number=phoneNumber or None,
        dni=dni or None,
        full_name=fullname or None)
    db.session.add(nuevo_usuario)
    db.session.commit()

    user = db.session.query(Users).filter_by(username=username).first()
    if user is not None:
        user.status = "VERIFICADO"
    else:
        user.status = "NO_VERIFICADO"
    db.session.commit()

    response = {
        "id": str(user.id),  # Convertir UUID a cadena antes de serializar
        "createdAt": user.createdAt.isoformat()
    }

    json_response = json.dumps(response)

    db.session.close()

    return json_response, 200


@users_blueprint.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = db.session.query(Users).get(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.json

    if "status" in data:
        user.status = data["status"]
    if "dni" in data:
        user.dni = data["dni"]
    if "fullName" in data:
        user.full_name = data["fullName"]
    if "phoneNumber" in data:
        user.phone_number = data["phoneNumber"]

    db.session.commit()

    return jsonify({"msg": "El usuario ha sido actualizado"}), 200


@users_blueprint.route('/users/auth', methods=['POST'])
def generate_token():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = db.session.query(Users).filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Generar un nuevo UUID como token
    token = str(uuid.uuid4())

    # Calcular la fecha de vencimiento del token (por ejemplo, 1 hora después de la generación)
    expire_at = datetime.utcnow() + timedelta(hours=1)

    # Puedes almacenar este token y su fecha de vencimiento en la base de datos si lo deseas

    response = {
        "id": str(user.id),
        "token": token,
        "expireAt": expire_at.isoformat()
    }

    return jsonify(response), 200
