import hashlib

from flask import jsonify, request, Blueprint
from datetime import datetime, timedelta
import uuid

from users.src.models.user import Users
from users.src.models.model import db_session, init_db

# Crear el Blueprint para la gestión de usuarios
users_blueprint = Blueprint('users', __name__)

init_db()


# Ruta para crear un nuevo usuario
@users_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    dni = data.get("dni")
    fullname = data.get("fullname")
    phoneNumber = data.get("phoneNumber")

    if not (username and password and email):
        return jsonify({"error": "Datos insuficientes"}), 400

    password_encoded = password.encode('utf-8')
    password_encriptado = hashlib.sha256(password_encoded).hexdigest()

    nuevo_usuario = Users(
        username=username,
        password=password,
        salt=password_encriptado,
        email=email,
        phone_number=phoneNumber,
        dni=dni,
        full_name=fullname
    )
    db_session.add(nuevo_usuario)
    db_session.commit()

    user = db_session.query(Users).filter_by(username=username).first()


    response = {
        "id": str(user.id),
        "createdAt": user.createdAt.isoformat()
    }

    db_session.close()

    return jsonify(response), 200


@users_blueprint.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = db_session.query(Users).get(user_id)

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

    db_session.commit()
    db_session.close()

    return jsonify({"msg": "El usuario ha sido actualizado"}), 200


@users_blueprint.route('/users/auth', methods=['POST'])
def generate_token():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = db_session.query(Users).filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Generar un nuevo UUID como token
    token = str(uuid.uuid4())

    # Calcular la fecha de vencimiento del token (por ejemplo, 1 hora después de la generación)
    expire_at = datetime.utcnow() + timedelta(hours=1)
    user.expireAt = expire_at
    user.token = token
    if user.token is not None:
        user.status = "VERIFICADO"
    else:
        user.status = "POR_VERIFICAR"
    db_session.commit()
    # Puedes almacenar este token y su fecha de vencimiento en la base de datos si lo deseas

    response = {
        "id": str(user.id),
        "token": token,
        "expireAt": expire_at.isoformat()
    }
    db_session.close()

    return jsonify(response), 200


# Ruta para consultar información del usuario
@users_blueprint.route('/users/me', methods=['GET'])
def get_user_info():
    # Obtener el token del encabezado Authorization
    token = request.headers.get('Authorization')

    if not token or not token.startswith('Bearer '):
        return jsonify({"error": "Token no válido"}), 403

    token = token.split(' ')[1]

    user = db_session.query(Users).filter_by(token=token).first()
    print(user.expireAt)
    if not user or user.expireAt < datetime.utcnow():
        return jsonify({"error": "Token inválido o vencido"}), 401

    response = {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "fullName": user.full_name,
        "dni": user.dni,
        "phoneNumber": user.phone_number,
        "status": user.status
    }

    return jsonify(response), 200
