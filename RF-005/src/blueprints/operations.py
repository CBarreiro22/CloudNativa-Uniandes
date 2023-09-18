from cmath import log
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
    post=get_post(id, token)
    #valida que exista la publicación. Status Code 200 indica que publicación existe, cualquier valor diferente no existe
    if post.status_code != 200:
        return '', 404
    #valida que el usuario tenga permisos sobre esa publicación
    if post.json()['userId'] != current_user_id:
            return '', 403
    #REQUEST 2: consultar route por routeId
    route = get_route(post.json()['routeId'], token)
    #REQUEST 3: consultar publicaciones por postId
    offers = get_offers(id, token)
    #Por cada oferta, is a consultar el score al servicio de score
    ofertas = []
    for offer in offers.json():
        di={}
        score = get_score(offer['id'],token)
        if score.status_code == 200:
            di["id"]=offer["id"]
            di["userId"]=offer["userId"]
            di["description"]=offer["description"]
            di["size"]=offer["size"]
            di["fragile"]=offer["fragile"]
            di["offer"]=offer["offer"]
            di["score"]=score.json()['Score'] 
            di["createdAt"]=offer["createdAt"]
            ofertas.append(di)
    #Ordenar por orden descendente con base al score
    ofertas = sorted(ofertas, key = lambda x : x["score"], reverse=True)
    response = {
        "data":{
            "id": post.json()['id'],
            "expireAt":post.json()['expireAt'],
            "route": {
                "id":route.json()['id'],
                "flightId":route.json()['flightId'],
                "origin":{
                    "airportCode":route.json()['sourceAirportCode'],
                    "country":route.json()['sourceCountry']
                },
                "destiny":{
                     "airportCode":route.json()['destinyAirportCode'],
                    "country":route.json()['destinyCountry']
                },
                "bagCost":route.json()['bagCost']
            },
            "plannedStartDate":route.json()['plannedStartDate'],
            "plannedEndDate":route.json()['plannedEndDate'],
            "createdAt":route.json()['createdAt'],
            "offers":ofertas
        }
    }
    return jsonify(response), 200

@operations_blueprint.route('/rf005/posts/ping', methods=['GET'])
def check_health():
    return 'pong', 200

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
    if response_user.status_code == 200:
        return [True, response_user.json()['id']]
    else:
        return [False, None]

def get_post(id, token):
    return requests.get(f"{POSTS_PATH}/posts/{id}", headers={"Authorization":token})

def get_offers(id, token):
    return requests.get(f"{OFFERS_PATH}/offers?post={id}", headers={"Authorization":token})

def get_route(route_id, token):
    return requests.get(f"{ROUTES_PATH}/routes/{route_id}", headers={"Authorization":token})

def get_score(offer_id, token):
    return requests.get(f"{SCORES_PATH}/score/{offer_id}", headers={"Authorization":token})