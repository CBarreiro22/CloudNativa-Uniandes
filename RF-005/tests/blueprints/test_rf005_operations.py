from tokenize import Token
import unittest
import json
from wsgiref import headers
from flask import jsonify
from unittest.mock import MagicMock, patch, Mock
from src.main import app
import requests_mock


class TestRF005Operations(unittest.TestCase):
    def setUp(self) -> None:
        self.mock = requests_mock.Mocker()
        self.mock.start()

    def tearDown(self):
        self.mock.stop()
        self.mock.reset()

    @patch('src.blueprints.operations.get_route')
    @patch('src.blueprints.operations.get_offers')
    @patch('src.blueprints.operations.get_post')
    @patch('src.blueprints.operations.requests.get')
    def test_filter_route(self, mocked, post, offers, route):
        token = '123ABC'
        user_id = 123456789
        route_id = 987654321

        response_route = MagicMock()
        response_route.status_code = 200
        response_route.json.return_value = {
            'id': '1', 'flightId': 0, 'sourceAirportCode': 0, 'sourceCountry': 0, 'destinyAirportCode': 0, 'destinyCountry': '', 'bagCost': 0, 'plannedStartDate': '', 'plannedEndDate': '', 'createdAt': 0}
        route.return_value = response_route

        response_offers = MagicMock()
        response_offers.status_code = 200
        response_offers.json.return_value = [{'id': '1'}]
        offers.return_value = response_offers

        response_post = MagicMock(headers={"Authorization": "FAKE_TOKEN"})
        response_post.status_code = 200
        response_post.json.return_value = {
            'id': 0, 'expireAt': 0, 'userId': user_id, 'routeId': route_id}
        post.return_value = response_post

    
        mocked.return_value = MagicMock(
            status_code=2000, json={'id': '123'}, headers={"Authorization": token})
        # token.register_uri('GET', 'mock://users/me', json={'userId': 'b'}, status_code=300)
        # mocked.get('mock://posts/12',status_code=200,{'json':{'userId': 'b'}},headers={"Authorization": "FAKE_TOKEN"})

        # mocked.return_value.status_code = 200
        # mocked.return_value.response=0

        tester = app.test_client(self)

        with patch("src.blueprints.operations.get_token") as t:
            t.return_value = [user_id, token]
            with patch("src.blueprints.operations.is_valid_token") as token:
                response1 = MagicMock()
                response1.status_code = 200
                response1.json.return_value = {'ido': '12345'}
                token.return_value = response1

                response = tester.get(
                    f"/rf005/posts/{'a509259c-da68-4e16-94de-982bc0073d0b'}", headers={"Authorization": token})

                statuscode = response.status_code
        # self.assertEqual(response.json, '')
        self.assertEqual(statuscode, 200)
