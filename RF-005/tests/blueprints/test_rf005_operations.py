from importlib.resources import path
import re
from tokenize import Token
import unittest
import json
from wsgiref import headers
from flask import jsonify
from unittest.mock import MagicMock, patch, Mock
from src.main import app
from src import main
from src.blueprints import operations


class TestRF005Operations(unittest.TestCase):
    # def setUp(self) -> None:
    #     self.mock = requests_mock.Mocker()
    #     self.mock.start()

    # def tearDown(self):
    #     self.mock.stop()
    #     self.mock.reset()
    
    @patch('src.blueprints.operations.get_score')
    @patch('src.blueprints.operations.get_route')
    @patch('src.blueprints.operations.get_offers')
    @patch('src.blueprints.operations.get_post')
    @patch('src.blueprints.operations.requests.get')
    def test_consultar_publicacion(self, mocked, post, offers, route, score):
        token = '123ABC'
        user_id = 123456789
        route_id = 987654321

        response_score = MagicMock()
        response_score.status_code = 200
        response_score.json.return_value = {'Score': 0}
        score.return_value = response_score

        response_route = MagicMock()
        response_route.status_code = 200
        response_route.json.return_value = {
            'id': '1', 'flightId': 0, 'sourceAirportCode': 0, 'sourceCountry': 0, 'destinyAirportCode': 0, 'destinyCountry': '', 'bagCost': 0, 'plannedStartDate': '', 'plannedEndDate': '', 'createdAt': 0}
        route.return_value = response_route

        response_offers = MagicMock()
        response_offers.status_code = 200
        response_offers.json.return_value = [ {'id': '1', 'userId': 0, 'description': 0, 'size': 0, 'fragile': 0, 'offer': '', 'Score': 0, 'createdAt': 0}]
        offers.return_value = response_offers

        response_post = MagicMock(headers={"Authorization": "FAKE_TOKEN"})
        response_post.status_code = 200
        response_post.json.return_value = {
            'id': 0, 'expireAt': 0, 'userId': user_id, 'routeId': route_id}
        post.return_value = response_post

        mocked.return_value = MagicMock(
            status_code=2000, json={'id': '123'}, headers={"Authorization": token})

        tester = app.test_client(self)

        with patch("src.blueprints.operations.get_token") as t:
            t.return_value = [user_id, token]
            # with patch("src.blueprints.operations.is_valid_token") as token1:
            #     response1 = MagicMock()
            #     response1.status_code = 9200
            #     response1.json.return_value = {'ido': '12345'}
            #     token1.return_value = response1

            response = tester.get(
                    f"/rf005/posts/{'a509259c-da68-4e16-94de-982bc0073d0b'}", headers={"Authorization": token})

            statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    @patch('src.blueprints.operations.get_route')
    @patch('src.blueprints.operations.get_offers')
    @patch('src.blueprints.operations.get_post')
    @patch('src.blueprints.operations.requests.get')
    def test2(self, mocked, post, offers, route):
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
        response_post.status_code = 500
        response_post.json.return_value = {
            'id': 0, 'expireAt': 0, 'userId': user_id, 'routeId': route_id}
        post.return_value = response_post

    
        mocked.return_value = MagicMock(
            status_code=2000, json={'id': '123'}, headers={"Authorization": token})

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
        self.assertEqual(statuscode, 404)


    @patch('src.blueprints.operations.get_route')
    @patch('src.blueprints.operations.get_offers')
    @patch('src.blueprints.operations.get_post')
    @patch('src.blueprints.operations.requests.get')
    def test3(self, mocked, post, offers, route):
        token = '123ABC'
        user_id = 123456789
        user_id2 = 1234567890
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
        response_post.status_code = 500
        response_post.json.return_value = {
            'id': 0, 'expireAt': 0, 'userId': user_id2, 'routeId': route_id}
        post.return_value = response_post

    
        mocked.return_value = MagicMock(
            status_code=2000, json={'id': '123'}, headers={"Authorization": token})

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
        self.assertEqual(statuscode, 404)
    
    
    @patch('src.blueprints.operations.requests.get')
    def test4(self,  post):
        token = '123ABC'
        user_id = 123456789
        route_id = 987654321

        response_post = MagicMock(headers={"Authorization": "FAKE_TOKEN"})
        response_post.status_code = 200
        response_post.json.return_value = {
            'id': 0, 'expireAt': 0, 'userId': user_id, 'routeId': route_id}
        post.return_value = response_post
        #resultado = operations.get_post(1,token)
        response = app.test_client(self).get(
                    f"/rf005/posts/{'a509259c-da68-4e16-94de-982bc0073d0b'}", headers={"Authorization": token})
        self.assertEqual(response.status_code, 403)
        
    @patch('src.blueprints.operations.requests.get')
    def test_no_token(self, mock):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = {}
        mock.return_value = response_mock
        response = app.test_client(self).get(
                    f"/rf005/posts/{'a509259c-da68-4e16-94de-982bc0073d0b'}")
        self.assertEqual(response.status_code, 403)
    
    #@patch('src.blueprints.operations.is_valid_token')
    @patch('src.blueprints.operations.requests.get')
    def test_invalid_token(self, mock):
        response_mock = MagicMock()
        response_mock.status_code = 400
        response_mock.json.return_value = {}
        mock.return_value = response_mock

       
       
        with patch("src.blueprints.operations.is_valid_token") as token2:
            response1 = MagicMock()
            response1.status_code = 400
            response1.json.return_value = {'ido': '12345'}
            token2.return_value = response1

            response = app.test_client(self).get(
                    f"/rf005/posts/{'a509259c-da68-4e16-94de-982bc0073d0b'}", headers={"Authorization": '123'})
        self.assertEqual(response.status_code, 404)
     

    
                

    @patch('src.blueprints.operations.requests.get')
    def test_check_health(self, mock):
        tester = app.test_client(self)
        response = tester.get("/rf005/posts/ping")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    if __name__ == '__main__':
        unittest.main()

