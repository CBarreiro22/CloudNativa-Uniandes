from flask import Flask, Blueprint, request, jsonify
from src.models.model import Base
import requests

operations_blueprint = Blueprint('operations', __name__)
USERS_PATH = os.environ["USERS_PATH"]


@operations_blueprint.route('/routes', methods=['POST'])
def create_route():
    json = request.get_json()
    print(json['flightId'])
    print(json['sourceAirportCode'])
    print(json['sourceCountry'])
    print(json['destinyAirportCode'])
    print(json['destinyCountry'])
    print(json['bagCost'])
    print(json['plannedStartDate'])
    print(json['plannedEndDate'])
    return 'routes', 201


@operations_blueprint.route('/routes', methods=['GET'])
def get_routes():
    args = request.args
    flight = args.get('flight') or None
    print(flight)
    if flight is not None:
        return 'retorna filtrando', 200
    # tareas = Tarea.query.with_entities(Tarea.id, Tarea.file_name, Tarea.file_name_converted,
    #                                            Tarea.time_stamp, Tarea.new_format, Tarea.status).limit(query_max)

    token = '123'
    url = f"{USERS_PATH}/users/me"
    respuesta = requests.get(url, headers={"Authorization": token})
    resultado = respuesta.json()
    return 'routes', 200


@operations_blueprint.route('/routes/<string:id>', methods=['GET'])
def get_route(id):
    print(id)
    return jsonify({
        "id": "id del trayecto",
        "flightId": "código del vuelo",
        "sourceAirportCode": "código del aeropuerto de origen",
        "sourceCountry": "nombre del país de origen",
        "destinyAirportCode": "código del aeropuerto de destino",
        "destinyCountry": "nombre del país de destino",
        "bagCost": "costo de envío de maleta",
        "plannedStartDate": "fecha y hora de inicio del trayecto",
        "plannedEndDate": "fecha y hora de finalización del trayecto",
        "createdAt": "fecha y hora de creación del trayecto en formato ISO"
    }), 200


@operations_blueprint.route('/routes/<string:id>', methods=['DELETE'])
def delete_route(id):
    print(id)
    return jsonify({
        "msg": "el trayecto fue eliminado"
    }), 200


@operations_blueprint.route('/routes/ping', methods=['GET'])
def check_health():
    return 'pong', 200


@operations_blueprint.route('/routes/reset', methods=['POST'])
def reset_database():
    return jsonify({
        "msg": "Todos los datos fueron eliminados"
    }), 200
