import os

import requests
from dotenv import load_dotenv
from marshmallow import Schema, fields

from ..erros.errors import internal_server_error
from .BaseCommand import BaseCommand

loaded = load_dotenv('.env.development')

ROUTES_PATH = os.environ["ROUTES_PATH"]


class RoutesService(BaseCommand):

    @staticmethod
    def get( flight, headers):

        try:
            response = requests.get(url=f"{ROUTES_PATH}/routes?flight={flight}", headers=headers)

            return response
        except requests.exceptions.RequestException as e:
            raise internal_server_error


    @staticmethod
    def post(route, headers):

        schema = RouteRequestJsonSchema()
        json_route = schema.dump(route)
        response = requests.post(url=f"{ROUTES_PATH}/routes", json=json_route, headers=headers)
        if response.status_code == 200:
            return RouteResponseJsonSchema().load (response.json())
        elif response.status_code != 200:
            return response.json(), response.status_code

    @staticmethod
    def delete (id, headers):
        response = requests.delete(f"{ROUTES_PATH}/routes/{id}", headers=headers)
        return response.json(), response.status_code


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


class RouteResponse:
    def __init__(self, id: object, createdAt: object) -> object:
        self.id = id
        self.createdAt = createdAt


class RouteRequestJsonSchema(Schema):
    flightId = fields.String()
    sourceAirportCode = fields.String()
    sourceCountry = fields.String()
    destinyAirportCode = fields.String()
    destinyCountry = fields.String()
    bagCost = fields.Number()
    plannedStartDate = fields.String()
    plannedEndDate = fields.String()


class RouteResponseJsonSchema(Schema):
    id = fields.String()
    createdAt = fields.String()
