import hashlib

from flask import jsonify, request, Blueprint
from datetime import datetime, timedelta
import uuid
from ..errors.errors import TokenNotHeaderError, InsufficientDataError, \
    UserExistError, UserNotFound, InvalidCredentialsError, InternalServerError
from ..models.user import Users
from ..models.model import db_session, init_db

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

    nuevo_usuario = Users(
        username=username,
        password=password,
        salt=password_encriptado,
        email=email,
        phone_number=phoneNumber,
        dni=dni,
        full_name=fullname
    )
    try:
        db_session.add(nuevo_usuario)
        db_session.commit()

        user = db_session.query(Users).filter_by(username=username).first()

        response = {
            "id": str(user.id),
            "createdAt": user.createdAt.isoformat()
        }

        db_session.close()

        return jsonify(response), 201
    except:
        db_session.rollback()
        raise UserExistError("El usuario ya existe")


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
    db_session.close()

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
        raise UserNotFound("Credenciales inválidas")

    # Generar un nuevo UUID como token
    token = str(uuid.uuid4())

    # Calcular la fecha de vencimiento del token (por ejemplo, 1 hora después de la generación)
    expire_at = datetime.utcnow() + timedelta(hours=1)
    user.expireAt = expire_at
    user.token = token
    #if user.token is not None:
    #    user.status = "VERIFICADO"
    #else:
    #    user.status = "POR_VERIFICAR"
    db_session.commit()

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
        raise TokenNotHeaderError("El token no está en el encabezado de la solicitud")

    token = token.split(' ')[1]

    user = db_session.query(Users).filter_by(token=token).first()
    if not user or user.expireAt < datetime.utcnow():
        raise InvalidCredentialsError("Invalid or expired token")

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
    db_session.close()

    return jsonify({"msg": "Todos los datos fueron eliminados"}), 200
