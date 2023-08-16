from importlib.resources import path
import unittest
from wsgiref import headers
import requests
from unittest.mock import patch
from src.main import app


class TestRoutesOperations(unittest.TestCase):
    @patch('src.blueprints.operations')
    def test_create_route_token_vacio(self, mocked):
        tester = app.test_client(self)
        response = tester.post("/routes", json={
            'flightId': 'test',
            'sourceAirportCode': 'test',
            'sourceCountry': 'test',
            'destinyAirportCode': 'test',
            'destinyCountry': 'test',
            'bagCost': 'test',
            'plannedStartDate': 'test',
            'plannedEndDate': 'test'
        })
        statuscode = response.status_code
        self.assertEqual(statuscode, 403)

    # @patch('src.blueprints.operations')
    # def test_create_route_token_invalido(self, mocked):
    #     tester = app.test_client(self)
    #     response = tester.post("/routes", headers={"Authorization": 23}, json={
    #         'flightId': 'test',
    #         'sourceAirportCode': 'test',
    #         'sourceCountry': 'test',
    #         'destinyAirportCode': 'test',
    #         'destinyCountry': 'test',
    #         'bagCost': 123,
    #         'plannedStartDate': '2023-11-01',
    #         'plannedEndDate': '2023-11-01'
    #     })
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 400)

    @patch('src.blueprints.operations')
    def test_create_route_token_valido(self, mocked):
        tester = app.test_client(self)
        response = tester.post("/routes", headers={"Authorization": 23}, json={
            'flightId': 'test',
            'sourceAirportCode': 'test',
            'sourceCountry': 'test',
            'destinyAirportCode': 'test',
            'destinyCountry': 'test',
            'bagCost': 123,
            'plannedStartDate': '2023-11-01',
            'plannedEndDate': '2023-11-01'
        })
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)

    @patch('src.blueprints.operations')
    def test_create_route_planned_start_date_invalids(self, mocked):
        tester = app.test_client(self)
        response = tester.get("/routes/ping")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    @patch('src.blueprints.operations')
    def test_create_route_planned_start_date_invalidsoo(self, mocked):
        tester = app.test_client(self)
        response = tester.get("/routes/123")
        statuscode = response.status_code
        self.assertEqual(statuscode, 403)

    @patch('src.blueprints.operations')
    def test_reset_db(self, mocked):
        tester = app.test_client(self)
        response = tester.post("/routes/reset")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


    if __name__ == '__main__':
        unittest.main()
