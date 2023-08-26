import os
import requests
import uuid
import datetime
from datetime import datetime
from dotenv import load_dotenv
from src.errors.errors import InvalidToken
from src.errors.errors import MissingToken
from src.models.route import RouteJsonSchema
from src.models.route import Route
from flask import Flask, Blueprint, request, jsonify
from src.models.model import db_session, init_db, reset_db

ISO_FORMATTER = "%Y-%m-%dT%H:%M:%S.%fZ"

loaded = load_dotenv('.env.development')
operations_blueprint = Blueprint('operations', __name__)
USERS_PATH = os.environ["USERS_PATH"]

init_db()
route_schema = RouteJsonSchema()

#1. Creación de trayecto
@operations_blueprint.route('/routes', methods=['POST'])
def create_route():
        get_token(request)
        json = request.get_json()
        flight_id = json.get('flightId')
        source_airport_code= json.get('sourceAirportCode')
        source_country=json.get('sourceCountry')
        destiny_airport_code=json.get('destinyAirportCode')
        destiny_country=json.get('destinyCountry')
        bag_cost=float( json.get('bagCost'))
        planned_start_date_str=json.get('plannedStartDate')
        planned_end_date_str=json.get('plannedEndDate')

        if flight_id is None or source_airport_code is None or source_country is None or destiny_airport_code is None or destiny_country is None or bag_cost is None or planned_start_date_str is None or planned_end_date_str is None:
            return '', 400

        planned_start_date = parse_iso_date(planned_start_date_str)
        planned_end_date = parse_iso_date(planned_end_date_str) 


        if planned_start_date is None or planned_end_date is None or not is_valid_date_route(planned_start_date,planned_end_date):
            return jsonify({ "msg": "Las fechas del trayecto no son válidas"}), 412
        result=Route.query.filter(Route.flightId == flight_id).first()
        if result is not None:
            return '', 412
        route_entity = Route(flight_id, source_airport_code, source_country,
                             destiny_airport_code, destiny_country, bag_cost, planned_start_date, planned_end_date)
        db_session.add(route_entity)
        db_session.commit()
        return jsonify({
                "id": route_entity.id,
            "createdAt": route_entity.createdAt.isoformat()}
        ), 201

#2. Ver y filtrar trayectos
@operations_blueprint.route('/routes', methods=['GET'])
def get_routes():
    get_token(request)
    #Retornar 400 en caso de que alguno de los campos de busqudedano tenga el formato especificado
    args = request.args
    flight = args.get('flight') or None
    if flight is not None:
        result = [route_schema.dump(r) for r in Route.query.filter(Route.flightId == flight)]
    else:
        result = [route_schema.dump(r) for r in Route.query.all()]
    return jsonify(result), 200

#3. Consultar un trayecto
@operations_blueprint.route('/routes/<string:id>', methods=['GET'])
def get_route(id):
    get_token(request)
    if not is_valid_uuid(id):
        return '', 400
    result=Route.query.filter(Route.id == id).first()
    if result is None:
        return '', 404
    return jsonify(route_schema.dump(result)), 200

#4. Eliminar trayecto
@operations_blueprint.route('/routes/<string:id>', methods=['DELETE'])
def delete_route(id):
    get_token(request)
    if not is_valid_uuid(id):
        return '', 400
    result = Route.query.filter(Route.id == id).first() 
    if result is None:
        return '',404
    db_session.delete(result)
    db_session.commit()
    return jsonify({
        "msg": "el trayecto fue eliminado"
    }), 200

#5. Consulta de salud del servicio
@operations_blueprint.route('/routes/ping', methods=['GET'])
def check_health():
    return 'pong', 200

#6. Restablecer base de datos
@operations_blueprint.route('/routes/reset', methods=['POST'])
def reset_database():
    reset_db()
    return jsonify({
        "msg": "Todos los datos fueron eliminados"
    }), 200

def get_token(value):
    try:
        print(value)
        token= value.headers.get('Authorization') 
        if token is None:
            raise MissingToken
        if not is_valid_token(token):
            raise InvalidToken
        return token
    except ValueError:
        return None

def is_valid_token(value):
    url = f"{USERS_PATH}/users/me"
    respuesta = requests.get(url, headers={"Authorization": value})
    return respuesta.status_code == 200

def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False

def parse_iso_date(date_str):
    try:
        return datetime.strptime(date_str, ISO_FORMATTER)
    except ValueError:
        return None

def is_valid_date_route(start_date, end_date):
    if start_date < datetime.now()  or end_date < datetime.now():
        return False
    if end_date < start_date:
        return False
    return True