from flask import Blueprint, request, jsonify

from ..commands.PostService import Post, PostsService
from ..commands.RoutesService import RoutesService, Route, RouteResponse

rf003_blueprint = Blueprint("rf003", __name__)


@rf003_blueprint.route(rule='/rf003/posts', methods=['POST'])
def addRff03() -> object:
    json_data = request.get_json()
    flightId = json_data['flightId']
    expiretAt = json_data["expireAt"]
    headers = request.headers
    user_id = None
    route_id = None
    response_route = RoutesService.get(flight=flightId, headers=headers)
    route_response_obj = None
    if response_route.status_code == 200 and len(response_route.json()) == 0:
        route = get_route(json_data)
        response_route = RoutesService().post(route, headers=headers)
        route_response_obj = RouteResponse(id=route_id,
                                           createdAt=response_route['createdAt'])
    elif response_route.status_code == 200 and len(response_route.json()) > 0:
        route_response_obj = RouteResponse(id=response_route.json()[0]['id'],
                                           createdAt=response_route.json()[0]['createdAt'])
        route_id = response_route.json()[0]['id']
    post = get_post(expireAt=expiretAt, routeId=route_id)

    response_post = PostsService.post(post=post, headers=headers)

    response_data = {
        "data": {
            "id": response_post["id"],
            "userId": response_post["userId"],
            "createdAt": response_post["createdAt"],
            "expireAt": response_post["expireAt"],
            "route": {
                "id": route_response_obj.flightId,
                "createdAt": route_response_obj.createdAt
            }
        },
        "msg": "Resumen de la operación"
    }
    return jsonify(response_data), 201


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
