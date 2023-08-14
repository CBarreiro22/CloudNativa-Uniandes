import os
import requests
import uuid
from dotenv import load_dotenv
from src.models.route import RouteJsonSchema
from src.models.route import Route
from flask import Flask, Blueprint, request, jsonify
from src.models.model import db_session, init_db, reset_db

loaded = load_dotenv('.env.development')
operations_blueprint = Blueprint('operations', __name__)
USERS_PATH = os.environ["USERS_PATH"]

init_db()
route_schema = RouteJsonSchema()

@operations_blueprint.route('/routes', methods=['POST'])
def create_route():
    json = request.get_json()
    flight_id=json['flightId']
    source_airport_code= json['sourceAirportCode']
    source_country=json['sourceCountry']
    destiny_airport_code=json['destinyAirportCode']
    destiny_country=json['destinyCountry']
    bag_cost=json['bagCost']
    planned_start_date=json['plannedStartDate']
    planned_end_date=json['plannedEndDate']
    route_entity = Route(flight_id, source_airport_code, source_country,
                         destiny_airport_code, destiny_country, bag_cost, planned_start_date, planned_end_date)
    db_session.add(route_entity)
    db_session.commit()
    return jsonify({
            "id": route_entity.id,
        "createdAt": route_entity.createdAt.isoformat()}
    ), 201

 # tareas = Tarea.query.with_entities(Tarea.id, Tarea.file_name, Tarea.file_name_converted,
    #                                            Tarea.time_stamp, Tarea.new_format, Tarea.status).limit(query_max)

    token = '123'
    # url = f"{USERS_PATH}/users/me"
    # respuesta = requests.get(url, headers={"Authorization": token})
    # resultado = respuesta.json()
@operations_blueprint.route('/routes', methods=['GET'])
def get_routes():
    args = request.args
    flight = args.get('flight') or None
    if flight is not None:
        result = route_schema.dump(Route.query.filter(Route.flightId == flight).first())
    else:
        result = [route_schema.dump(tarea) for tarea in Route.query.all()]
    return jsonify(result), 200


@operations_blueprint.route('/routes/<string:id>', methods=['GET'])
def get_route(id):
    result = route_schema.dump(Route.query.filter(Route.id == id).first())
    return jsonify(result), 200


@operations_blueprint.route('/routes/<string:id>', methods=['DELETE'])
def delete_route(id):
    token= get_token(request)
    print(token)
    if token is None:
        return '', 403
    if not is_valid_token(token):
        return '', 401
    if not is_valid_uuid(id):
        return '', 400
    route_entity = Route.query.filter(Route.id == id).first() 
    if route_entity is None:
        return '',404
    db_session.delete(route_entity)
    db_session.commit()
    return jsonify({
        "msg": "el trayecto fue eliminado"
    }), 200


@operations_blueprint.route('/routes/ping', methods=['GET'])
def check_health():
    return 'pong', 200


@operations_blueprint.route('/routes/reset', methods=['POST'])
def reset_database():
    reset_db()
    return jsonify({
        "msg": "Todos los datos fueron eliminados"
    }), 200


def get_token(value):
    try:
        return value.headers.get('Authorization') 
    except ValueError:
        return None

def is_valid_token(value):
    return True

def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False