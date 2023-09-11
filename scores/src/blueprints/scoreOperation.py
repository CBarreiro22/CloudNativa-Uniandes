
import os
import requests
from flask import Blueprint, jsonify, request

from ..models.score import Scores
from ..errors.errors import TokenNotHeaderError
from src.models.model import init_db,db_session


# Crear el Blueprint para el calculo del score
scores_blueprint = Blueprint('scores', __name__)
OFFER_PATH = os.environ["OFFERS_PATH"]
ROUTE_PATH = os.environ["ROUTE_PATH"]

init_db()

@scores_blueprint.route('/score', methods=['POST'])
def score_operation():

    # Obtener los parámetros id_offer e id_route de la solicitud POST
    data = request.json
    id_offer = data.get("id_offer")
    id_route = data.get("id_route")

    if not (id_offer and id_route):
        return jsonify({"error": "Los parámetros id_offer e id_route son obligatorios"}), 400

    # Obtener el token del usuario, por ejemplo, desde el encabezado "Authorization"
    token = request.headers.get("Authorization")

    # Verificar que se haya proporcionado un token
    if not token:
        return jsonify({"error": "Token de autorización no proporcionado"}), 401

    # Incluir el token en el encabezado "Authorization" de las solicitudes a los endpoints offer y route
    headers = {
        "Authorization": token
    }


    # Realizar una solicitud GET a la ruta /offers/id_offer
    offer_response = requests.get(f"{OFFER_PATH}/offers/{id_offer}", headers=headers)
    print(offer_response.status_code)
    if offer_response.status_code != 200:
        if offer_response.status_code == 401:
            return jsonify({"error": "Token invalido o esta vencido"}), 401
        return jsonify({"error": "Error al obtener la oferta"}), 500

    offer_data = offer_response.json()
    offer_value = offer_data.get("offer")
    offer_size = offer_data.get("size")

    # Realizar una solicitud GET a la ruta /routes/id_route
    route_response = requests.get(f"{ROUTE_PATH}/routes/{id_route}", headers=headers)

    if route_response.status_code != 200:
        return jsonify({"error": "Error al obtener la ruta"}), 500

    route_data = route_response.json()
    bag_cost = route_data.get("bagCost")

    # Realizar el cálculo del score utilizando los valores obtenidos
    score = calcular_score(offer_value, offer_size, bag_cost)
    nuevo_score = Scores(
        id_offer=id_offer,
        id_route=id_route,
        offer=offer_value,
        size=offer_size,
        bagcost=bag_cost,
        score=score
    )
    print(nuevo_score)
    db_session.add(nuevo_score)

    db_session.commit()

    # Devolver el score calculado como respuesta
    return jsonify({"score": score}), 200
   

    #try:
    #except Exception as e:
     #   return jsonify({"error": "Error interno del servidor"}), 500

def calcular_score(offer_value, offer_size, bag_cost):
    # monto oferta - (porcentaje de ocupación de una maleta * valor de la maleta en el trayecto)
    if offer_size == 'SMALL':
        procentagesBag =1
    else:
        if(offer_size == 'MEDIUM'):
            procentagesBag =0.5
        else:
            procentagesBag =0.25
    
    utility = offer_value - (procentagesBag * bag_cost)

    return utility

@scores_blueprint.route('/score/<string:id_offer>', methods=['GET'])
def get_score_info(id_offer):
    # Obtener el token del encabezado Authorization
    token = request.headers.get('Authorization')
    print("INgreso al metodo")
    if not token or not token.startswith('Bearer '):
        raise TokenNotHeaderError("El token no está en el encabezado de la solicitud")

    print(id_offer,"id_offer")
    token = token.split(' ')[1]
    print(token,"token")
    score = db_session.query(Scores).filter_by(id_offer=id_offer).first()
    print(score,"score")
    if score is None:
        return jsonify({"error": "Puntaje no encontrado"}), 404  # Devuelve un error 404 si no se encuentra el puntaje
    response = {
        "id": str(score.id),
        "Score": score.score
    }
    return jsonify(response), 200

@scores_blueprint.route('/score/reset', methods=['POST'])
def reset_database():
    # Eliminar todos los registros de la tabla Users
    db_session.query(Scores).delete()

    # Realizar commit y cerrar la sesión
    db_session.commit()

    return jsonify({"msg": "Todos los datos fueron eliminados"}), 200