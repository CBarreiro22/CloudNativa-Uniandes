from flask import Blueprint, request
from ..commands.RoutesService import RoutesService, Route

rf003_blueprint = Blueprint("rf003", __name__)


@rf003_blueprint.route(rule='/rf003/posts', methods=['POSTS'])
def addRff03() -> object:
    json_data = request.get_json()
    flight = json_data['flight']
    headers = request.headers

    response = RoutesService.get(flight=flight, headers=headers)
    if response.status_code != 200:
        route = get_route(json_data)
        RoutesService.post(route, headers=headers)


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

