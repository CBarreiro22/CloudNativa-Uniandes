import hashlib
import os
import uuid
from datetime import datetime, timedelta
from operator import or_

import requests
from flask import jsonify, request, Blueprint
from ..errors.errors import TokenNotHeaderError, InsufficientDataError, \
    UserExistError, UserNotFound, InvalidCredentialsError, InternalServerError
from ..models.model import db_session, init_db
from ..models.user import Users

EMAIL_NOTIFICATION_PATH = os.environ["EMAIL_NOTIFICATION_PATH"]
TRUE_NATIVE_PATH = os.environ["TRUE_NATIVE_PATH"]
USER_PATH = os.environ["USER_PATH"]
SECRET_TOKEN = os.environ["TOKEN_SERVICE"]

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
        raise InsufficientDataError("Datos insuficientes")

    password_encoded = password.encode('utf-8')
    password_encriptado = hashlib.sha256(password_encoded).hexdigest()

    user = db_session.query(Users).filter(or_(Users.username == username, Users.email == email)).first()
    if not user is None:
        raise UserExistError

    new_user = Users(
        username=username,
        password=password,
        salt=password_encriptado,
        email=email,
        phone_number=phoneNumber,
        dni=dni,
        full_name=fullname
    )
    try:
        db_session.add(new_user)

        db_session.commit()
        print("funcionb check")
        check_user(new_user)

        response = {
            "id": str(new_user.id),
            "createdAt": new_user.createdAt.isoformat()
        }
        return jsonify(response), 201
    except ValueError as e:
        raise UserExistError


def check_user(new_user):
    data = {
        "transactionIdentifier": str(uuid.uuid4()),
        "userIdentifier": str(new_user.id),
        "userWebhook": f'{USER_PATH}/users/40',
        "user": {
            "email": new_user.email,
            "dni": new_user.dni,
            "fullName": new_user.full_name,
            "phone": new_user.phone_number
        }
    }
    print(data)
    headers = {
        "Authorization": f"{SECRET_TOKEN}"
    }
    request = requests.post(f"{TRUE_NATIVE_PATH}/native/verify", json=data, headers=headers)
    print(request)


@users_blueprint.route('/users/<string:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = db_session.query(Users).filter_by(id=user_id).first()

    if not user:
        raise UserNotFound("Usuario no encontrado")

    data = request.json

    if not data:
        raise InsufficientDataError("La petición no contiene campos para actualizar")

    valid_fields = ["status", "dni", "fullName", "phoneNumber"]
    invalid_fields = [field for field in data if field not in valid_fields]

    if invalid_fields:
        raise InsufficientDataError(f"Campos inválidos: {', '.join(invalid_fields)}")

    if "status" in data:
        user.status = data["status"]
    if "dni" in data:
        user.dni = data["dni"]
    if "fullName" in data:
        user.full_name = data["fullName"]
    if "phoneNumber" in data:
        user.phone_number = data["phoneNumber"]

    db_session.commit()

    return jsonify({"msg": "el usuario ha sido actualizado"}), 200


@users_blueprint.route('/users/auth', methods=['POST'])
def generate_token():
    data = request.json

    # Verificar si faltan campos en los datos JSON
    if "username" not in data or "password" not in data:
        raise InsufficientDataError("Campos faltantes en los datos")

    username = data.get("username")
    password = data.get("password")

    user = db_session.query(Users).filter_by(username=username).first()

    # Manejar el caso cuando el usuario no existe
    if not user:
        raise UserNotFound("Usuario no encontrado")

    # Verificar la contraseña del usuario
    if user.password != password:
        raise InvalidCredentialsError()

    # Verified Status
    if user.status == "POR_VERIFICAR":
        raise InvalidCredentialsError("Usuario no ha sido verificado")

    print(user.status)

    if user.status == "NO_VERIFICADO":
        raise InvalidCredentialsError("Usuario no fue verificado, no puede ingresar a la plataforma")

    # Generar un nuevo UUID como token
    token = str(uuid.uuid4())

    # Calcular la fecha de vencimiento del token
    expire_at = datetime.utcnow() + timedelta(hours=1)
    user.expireAt = expire_at
    user.token = token
    db_session.commit()

    response = {
        "id": str(user.id),
        "token": token,
        "expireAt": expire_at.isoformat()
    }

    return jsonify(response), 200


# Ruta para consultar información del usuario
@users_blueprint.route('/users/me', methods=['GET'])
def get_user_info():
    # Obtener el token del encabezado Authorization
    token = request.headers.get('Authorization')

    if not token or not token.startswith('Bearer '):
        raise TokenNotHeaderError("El token no está en el encabezado de la solicitud")

    token = token.split(' ')[1]

    user = db_session.query(Users).filter_by(token=token).first()
    if not user or user.expireAt < datetime.utcnow():
        raise InvalidCredentialsError("Invalid or expired token")

    print(user.status)
    if user.status == "NO_VERIFICADO":
        raise InvalidCredentialsError("Usuario no fue verificado, no puede ingresar a la plataforma")

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


@users_blueprint.route('/users/ping', methods=['GET'])
def health_check():
    try:
        # Código que podría generar excepciones
        return "pong", 200
    except Exception as e:
        # Manejo de la excepción
        raise InternalServerError("Error interno")


@users_blueprint.route('/users/reset', methods=['POST'])
def reset_database():
    # Eliminar todos los registros de la tabla Users
    db_session.query(Users).delete()

    # Realizar commit y cerrar la sesión
    db_session.commit()

    return jsonify({"msg": "Todos los datos fueron eliminados"}), 200


@users_blueprint.route('/users/40', methods=['PATCH'])
def webhook_user():
    # data received from webhook
    data = request.json
    print("ingreso webhook")
    # verified information
    required_fields = ["RUV", "userIdentifier", "createdAt", "status", "score", "verifyToken"]
    for field in required_fields:
        if field not in data:
            raise InsufficientDataError(f"El campo {field} no está en los datos")

    RUV = data.get("RUV")
    userIdentifier = data.get("userIdentifier")
    score = data.get("score")
    verifyToken = data.get("verifyToken")
    user = db_session.query(Users).filter_by(id=userIdentifier).first()

    # The message hasn't been changed
    token = f"{SECRET_TOKEN}:{RUV}:{score}"
    sha_token = hashlib.sha256(token.encode()).hexdigest()

    if sha_token != verifyToken:
        return jsonify({"error": "El mensaje ha sido alterado"}), 401

    # Verified Score
    if score > 60:
        user.status = "VERIFICADO"
    else:
        user.status = "NO_VERIFICADO"

    print(user.status)
    db_session.commit()

    enviarCorreo(user, data)

    return jsonify({"status": user.status}), 200


def enviarCorreo(user, data):
    data_enviar = {
        "email": user.email,
        "RUV": data.get("RUV"),
        "username": user.username,
        "dni": user.dni,
        "status": user.status,
        "fullname": user.full_name,
        "phonenumber": user.phone_number
    }

    data_enviar = {key: value if value is not None else '' for key, value in data_enviar.items()}
    request = requests.post(f'{EMAIL_NOTIFICATION_PATH}/funcion-notificar-usuario', json=data_enviar)

    print("Este es el request", request.status_code)
