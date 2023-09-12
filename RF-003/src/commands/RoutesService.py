import os

import requests
from marshmallow import Schema, fields

from ..erros.errors import internal_server_error
from .BaseCommand import BaseCommand

OFFERS_PATH = os.environ["OFFERS_PATH"]


class RoutesService(BaseCommand):

    def get(self, flight, headers):

        try:
            response = requests.get(url=f"{OFFERS_PATH}/offers?flight={flight}", headers=headers)

            return response
        except requests.exceptions.RequestException as e:
            raise internal_server_error

    def post(self, route, headers):

        schema = RouteJsonSchema()
        json_route = schema.dump(route)
        response = requests.post(url=f"{OFFERS_PATH}/routes", json=json_route, headers=headers)

        return response


class Route:
    def __init__(self, flightId, sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost,
                 plannedStartDate, plannedEndDate):
        """

        :rtype: object
        """
        self.flightId = flightId
        self.sourceAirportCode = sourceAirportCode
        self.sourceCountry = sourceCountry
        self.destinyAirportCode = destinyAirportCode
        self.destinyCountry = destinyCountry
        self.bagCost = bagCost
        self.plannedStartDate = plannedStartDate
        self.plannedEndDate = plannedEndDate


class RouteJsonSchema(Schema):
    flightId = fields.String()
    sourceAirportCode = fields.String()
    sourceCountry = fields.String()
    destinyAirportCode = fields.String()
    destinyCountry = fields.String()
    bagCost = fields.Number()
    plannedStartDate = fields.String()
    plannedEndDate = fields.String()
