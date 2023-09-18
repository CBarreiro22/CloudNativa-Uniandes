from flask import Blueprint, request, jsonify
from jsonschema.validators import validate
from jsonschema import ValidationError
from datetime import datetime
from ..erros.errors import no_token, invalid_token, json_invalid_new_offer, duplicated_fligh, ivalid_dates,invalid_expiration_date
from ..commands.PostService import Post, PostsService
from ..commands.RoutesService import RoutesService, Route, RouteResponse
ISO_FORMATTER = "%Y-%m-%dT%H:%M:%S.%fZ"
rf003_blueprint = Blueprint("rf003", __name__)
new_rf003_schema = {
    "type": "object",
    "properties": {
        "flightId": {
            "type": "string"
        },
        "expireAt": {
            "type": "string",
            "format": "date-time"
        },
        "plannedStartDate": {
            "type": "string",
            "format": "date-time"
        },
        "plannedEndDate": {
            "type": "string",
            "format": "date-time"
        },
        "origin": {
            "type": "object",
            "properties": {
                "airportCode": {
                    "type": "string"
                },
                "country": {
                    "type": "string"
                }
            },
            "required": ["airportCode", "country"]
        },
        "destiny": {
            "type": "object",
            "properties": {
                "airportCode": {
                    "type": "string"
                },
                "country": {
                    "type": "string"
                }
            },
            "required": ["airportCode", "country"]
        },
        "bagCost": {
            "type": "integer"
        }
    },
    "required": ["flightId", "expireAt", "plannedStartDate", "plannedEndDate", "origin", "destiny", "bagCost"]
}


@rf003_blueprint.route(rule='/rf003/posts', methods=['POST'])
def addRff03() -> object:
    json_data = request.get_json()
    validate_new_offer_schema(json_data=json_data)
    flightId = json_data['flightId']
    expiretAt = json_data["expireAt"]
    headers = request.headers

    route_id = None
    validate_dates (json_data)
    validate_expiration_date(json_data)
    response_route = RoutesService.get(flight=flightId, headers=headers)
    route_response_obj = None
    if response_route.status_code == 200 and len(response_route.json()) == 0:
        route = get_route(json_data)
        response_route, route_status_code = RoutesService().post(route, headers=headers)
        if route_status_code != 201:
            return response_route, route_status_code
        route_id = response_route['id']
        route_response_obj = RouteResponse(id=route_id,
                                           createdAt=response_route['createdAt'])
    elif response_route.status_code == 200 and len(response_route.json()) > 0:
        route_response_obj = RouteResponse(id=response_route.json()[0]['id'],
                                           createdAt=response_route.json()[0]['createdAt'])
        route_id = response_route.json()[0]['id']
    elif response_route.status_code == 403:
        raise no_token
    elif response_route.status_code == 401:
        raise invalid_token

    response_get_post = PostsService.get(route=route_id, headers=headers)
    if response_get_post.status_code == 200 and len(response_get_post.json()) > 0:
        raise duplicated_fligh
    if response_get_post.status_code != 200:
        return response_get_post, response_get_post.status_code

    post = get_post(expireAt=expiretAt, routeId=route_id)

    response_post, post_http_status = PostsService.post(post=post, headers=headers)

    if post_http_status == 201:
        response_data = {
            "data": {
                "id": response_post["id"],
                "userId": response_post["userId"],
                "createdAt": response_post["createdAt"],
                "expireAt": expiretAt,
                "route": {
                    "id": route_response_obj.id,
                    "createdAt": route_response_obj.createdAt
                }
            },
            "msg": "Resumen de la operación"
        }
        return jsonify(response_data), 201
    elif post_http_status != 200:
        RoutesService.delete(id = route_id, headers = headers)
        return response_post, post_http_status


@rf003_blueprint.route(rule='/rf003/ping', methods=['GET'])
def ping():
    return "pong", 200


def get_route(json_data):
    route = Route(flightId=json_data["flightId"],
                  sourceAirportCode=json_data["origin"]["airportCode"],
                  sourceCountry=json_data["origin"]["country"],
                  destinyAirportCode=json_data["destiny"]["airportCode"],
                  destinyCountry=json_data["destiny"]["country"],
                  bagCost=json_data["bagCost"],
                  plannedStartDate=json_data["plannedStartDate"],
                  plannedEndDate=json_data["plannedEndDate"])
    return route


def get_post(expireAt, routeId):
    return Post(expireAt=expireAt, routeId=routeId)


def validate_new_offer_schema(json_data):
    try:
        validate(json_data, new_rf003_schema)

    except ValidationError as e:
        raise json_invalid_new_offer

def validate_dates(json_data):
    planned_start_date = parse_iso_date(json_data['plannedStartDate'])
    planned_end_date = parse_iso_date(json_data['plannedEndDate'])

    if planned_start_date < datetime.now()  or planned_end_date < datetime.now():
        raise  ivalid_dates
    if planned_end_date < planned_start_date:
        raise ivalid_dates
def validate_expiration_date (json_data):
    expiration_date = parse_iso_date(json_data['expireAt'])
    if expiration_date < datetime.now():
        raise invalid_expiration_date
def parse_iso_date(date_str):
    try:
        return datetime.strptime(date_str, ISO_FORMATTER)
    except ValueError:
        return None
