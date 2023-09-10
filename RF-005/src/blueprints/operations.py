import os
import requests
import json
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from src.errors.errors import InvalidToken, MissingToken
loaded = load_dotenv('.env.development')
USERS_PATH = os.environ["USERS_PATH"]
POSTS_PATH=os.environ["POSTS_PATH"]
ROUTES_PATH=os.environ["ROUTES_PATH"]
OFFERS_PATH=os.environ["OFFERS_PATH"]
SCORES_PATH=os.environ["SCORES_PATH"]

operations_blueprint= Blueprint('operations', __name__)

@operations_blueprint.route('/rf005/posts/<string:id>', methods=['GET'])
def get_offers(id):
    #validar token, obtener token y usuario
    value_token=get_token(request)
    #obtener usuarioId en la posición 0
    current_user_id=value_token[0]
    #obtener tokenId en la posición 1
    token= value_token[1]
    #REQUEST 1: consultar publicación por id
    post = requests.get(f"{POSTS_PATH}/posts/{id}", headers={"Authorization":token})
    #valida que exista la publicación. Status Code 200 indica que publicación existe, cualquier valor diferente no existe
    if post.status_code != 200:
        return '', 404
    #valida que el usuario tenga permisos sobre esa publicación
    if post.json()['userId'] != current_user_id:
            return '', 403
    #REQUEST 2: consultar route por routeId
    route = requests.get(f"{ROUTES_PATH}/routes/{post.json()['routeId']}", headers={"Authorization":token})
    #REQUEST 3: consultar publicaciones por postId
    offers = requests.get(f"{OFFERS_PATH}/offers/{id}", headers={"Authorization":token})
    #Por cada oferta, is a consultar el score al servicio de score
    offers_dictionary = json.loads(offers)
    ofertas = []
    for offer in offers_dictionary:
        di={}
        score = requests.get(f"{SCORES_PATH}/scores/{offer['id']}", headers={"Authorization":token})
        di["id"]=offer["id"]
        di["userId"]=offer["userId"]
        di["description"]=offer["description"]
        di["size"]=offer["size"]
        di["fragile"]=offer["fragile"]
        di["offer"]=offer["offer"]
        di["score"]=score.json()['score']
        di["createdAt"]=offer["createdAt"]
        ofertas.append(di)
        #offer["score"]=score.json()['score']
    #Ordenar por orden descendente con base al score
    ofertas = sorted(ofertas, key = lambda x : x.score, reverse=True)

    
    #  "data": {
    #     "id": identificador de la publicación,
    #     "expireAt": fecha y hora máxima en que se reciben ofertas en formato IDO,
    #     "route": {
    #         "id": identificador del trayecto,
    #         "flightId": identificador del vuelo,
    #         "origin": {
    #             "airportCode": código del aeropuerto de origen,
    #             "country": nombre del país de origen
    #         },
    #         "destiny": {
    #             "airportCode": código del aeropuerto de destino,
    #             "country": nombre del país de destino
    #         },
    #         "bagCost": costo de envío de maleta
    #     },
    #     "plannedStartDate": fecha y hora en que se planea el inicio del viaje en formato ISO,
    #     "plannedEndDate": fecha y hora en que se planea la finalización del viaje en formato ISO,
    #     "createdAt": fecha y hora de creación de la publicación en formato ISO,
    #     "offers": [
    #         {
    #             "id": identificador de la oferta,
    #             "userId": identificador del usuario que hizo la oferta,
    #             "description": descripción del paquete a llevar,
    #             "size": LARGE ó MEDIUM ó SMALL,
    #             "fragile": booleano que indica si es un paquete delicado o no,
    #             "offer": valor en dólares de la oferta para llevar el paquete,
    #             "score": utilidad que deja llevar este paquete en la maleta,
    #             "createdAt": fecha y hora de creación de la publicación en formato ISO
    #         }
    #     ]
    # }
    print (route)
    response = {
        "data":{
            "id": post.json()['id'],
            "route": json.dumps(route),
            "offers":json.dumps(ofertas)
        }
    }
    return jsonify(response), 200

def get_token(value):
    try:
        token =value.headers.get('Authorization')
        if token is None:
            raise MissingToken
        result = is_valid_token(token) 
        if not result[0]:
            raise InvalidToken
        return [result[1], token]
    except ValueError:
        return None
    
def is_valid_token(value):
    response_user = requests.get(f"{USERS_PATH}/users/me", headers={"Authorization":value})
    #print(response_user.json())
    if response_user.status_code == 200:
        return [True, response_user.json()['id']]
    else:
        return [False, None]