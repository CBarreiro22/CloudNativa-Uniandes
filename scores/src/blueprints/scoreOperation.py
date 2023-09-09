
import requests
from flask import Blueprint, jsonify, request
from src.models.model import init_db


# Crear el Blueprint para el calculo del score
scores_blueprint = Blueprint('scores', __name__)

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
    offer_response = requests.get(f"http://192.168.1.58:3003/offers/{id_offer}", headers=headers)
    print(offer_response)

    if offer_response.status_code != 200:
        return jsonify({"error": "Error al obtener la oferta"}), 500

    offer_data = offer_response.json()
    print(offer_data)
    offer_value = offer_data.get("offer")
    print(offer_value)
    offer_size = offer_data.get("size")
    print(offer_size)

    # Realizar una solicitud GET a la ruta /routes/id_route
    route_response = requests.get(f"http://192.168.1.58:3002/routes/{id_route}", headers=headers)

    if route_response.status_code != 200:
        return jsonify({"error": "Error al obtener la ruta"}), 500

    route_data = route_response.json()
    bag_cost = route_data.get("bagCost")

    # Realizar el cálculo del score utilizando los valores obtenidos
    score = calcular_score(offer_value, offer_size, bag_cost)
    print(score)
    # Devolver el score calculado como respuesta
    return jsonify({"score": score}), 200
   # try:

    #except Exception as e:
    #    return jsonify({"error": "Error interno del servidor"}), 500

def calcular_score(offer_value, offer_size, bag_cost):
    print("ingreso a calcular score")
    print(offer_value,"offer value")
    print(offer_size,"offer size")
    print(bag_cost,"bag cost")
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

