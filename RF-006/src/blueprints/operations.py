from datetime import datetime
from functools import wraps
from flask import Blueprint, jsonify
from flask import request

from scores.src.blueprints.scoreOperation import scores_blueprint
from ..errors.errors import invalid_json, invalid_expiration_date
from ..models.model import db_session, init_db, CreditCard, CreditCardSchema, CreateCreditCardSchema
from jsonschema.validators import validate

from ..commands.true_native_service import TrueNativeService
from ..commands.user_service import UserService

operations_blueprint = Blueprint('operations', __name__)

init_db()

credit_card_schema = {
    "type": "object",
    "properties": {
        "cardNumber": {
            "type": "string",
            "pattern": "^[0-9]{16}$"
        },
        "cvv": {
            "type": "string",
            "pattern": "^[0-9]{3}$"
        },
        "expirationDate": {
            "type": "string",
            "pattern": "^(0[1-9]|1[0-2])\/[0-9]{2}$"
        },
        "cardHolderName": {
            "type": "string"
        }
    },
    "required": ["cardNumber", "cvv", "expirationDate", "cardHolderName"]
}


def require_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if token is None or not token.startswith('Bearer '):
            return '', 403
        else:
            user_id, email_user = UserService.get_user_information(token)
            if user_id is None:
                return '', 401

        request.user_id = user_id
        request.email = email_user
        request.token = token
        return func(*args, **kwargs)

    return decorated


@operations_blueprint.route('/credit-cards/ping', methods=['GET'])
def check_health():
    return 'pong', 200


@operations_blueprint.route('/credit-cards', methods=['POST'])
@require_token
def create_credit_card():
    credit_card_data = request.get_json()
    validate_json(credit_card_data)
    expirationDate = credit_card_data['expirationDate']
    validate_expiration_date(expirationDate=expirationDate)

    transaction_id = uuid.uuid4()

    credit_card = persist_credit_card(credit_card_data, true_native_response)

    true_native_response, error_code = create_card_request(credit_card_data, transaction_id)
    if error_code:
        return '', error_code
    # llama persists (response)



    return CreateCreditCardSchema.dump(credit_card), 201


@operations_blueprint.route('credit-cards', methods=['GET'])
def get_credit_card():
    list_credit_cards = [CreditCardSchema.dump(p) for p in CreditCard.query.all()]
    return list_credit_cards


@scores_blueprint.route('/credit-cards/reset', methods=['POST'])
def reset_database():
    # Eliminar todos los registros de la tabla Users
    db_session.query(CreditCard).delete()

    # Realizar commit
    db_session.commit()

    return jsonify({"msg": "Todos los datos fueron eliminados"}), 200


def persist_credit_card(credit_card_data, true_native_response):
    userId = request.user_id
    email = request.email
    last_four_digit = lastFourDigits(credit_card_data.get('cardNumber'))
    ruv = true_native_response.get('RUV')
    issuer = true_native_response('issuer')
    status = true_native_response('status')
    credit_card = CreditCard(userId = userId, lastFourDigits = last_four_digit,
                             ruv=ruv, issuer=issuer, status=status, email=email)
    db_session.add(credit_card)
    db_session.commit()
    return credit_card

def lastFourDigits(cardNumber):
    # Obtén los últimos 4 caracteres
    lastFourDigits = cardNumber[-4:]

    return lastFourDigits


def validate_expiration_date(expirationDate):
    fecha_expiracion = datetime.strptime(expirationDate, "%m/%y")
    today = datetime.now()
    if (fecha_expiracion < today):
        raise invalid_expiration_date


def validate_json(json_data):
    try:
        validate(instance=json_data, schema=credit_card_schema)
    except Exception as e:
        print("errror de validación", e)
        raise invalid_json


def create_card_request(token, card_number, cvv, expiration_date, card_holder_name, transaction_identifier):
    response_card_request, status_code_error = TrueNativeService.register_card(token, card_number, cvv, expiration_date,
                                                                               card_holder_name,
                                                                               transaction_identifier)
    if not status_code_error:
        return response_card_request, ""
    return "", status_code_error
