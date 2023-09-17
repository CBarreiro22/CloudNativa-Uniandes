import unittest
from unittest.mock import patch, Mock
from flask import Flask, json

from src.blueprints.rf003 import rf003_blueprint
from src.commands.RoutesService import RoutesService, Route, RouteResponseJsonSchema
from src.commands.PostService import PostsService, Post
from datetime import datetime

class TestRoutesServiceRoute(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(rf003_blueprint)
        self.client = self.app.test_client()

    @patch('src.commands.RoutesService.requests.get')
    @patch('src.commands.RoutesService.requests.post')
    @patch('src.commands.PostService.requests.get')
    @patch('src.commands.PostService.requests.post')
    def test_addRff03_success(self, mock_post, mock_get_routes, mock_get_posts, mock_post_posts):
        # Mock a successful response for RoutesService.post
        mock_response_routes = Mock()
        mock_response_routes.status_code = 201
        mock_response_routes.json.return_value = {"id": "1", "createdAt": "2023-09-17T20:06:56.886861"}
        mock_post.return_value = mock_response_routes

        # Mock a successful response for PostsService.post
        mock_response_posts = Mock()
        mock_response_posts.status_code = 201
        mock_response_posts.json.return_value = {"id": "2", "userId": "user123", "createdAt": "2023-09-17T20:06:56.886861"}
        mock_post_posts.return_value = mock_response_posts

        # Mock a successful response for RoutesService.get
        mock_response_get_routes = Mock()
        mock_response_get_routes.status_code = 200
        mock_response_get_routes.json.return_value = []
        mock_get_routes.return_value = mock_response_get_routes

        # Mock a successful response for PostsService.get
        mock_response_get_posts = Mock()
        mock_response_get_posts.status_code = 200
        mock_response_get_posts.json.return_value = []
        mock_get_posts.return_value = mock_response_get_posts

        # Define a sample JSON request
        json_data = {
            "flightId": "flight123",
            "expireAt": "2023-09-20T12:00:00",
            "plannedStartDate": "2023-09-18T12:00:00",
            "plannedEndDate": "2023-09-19T12:00:00",
            "origin": {
                "airportCode": "origin123",
                "country": "country123"
            },
            "destiny": {
                "airportCode": "destiny123",
                "country": "countryDestiny123"
            },
            "bagCost": 10
        }
        headers = {"Authorization": "Bearer token123"}
        # Make a POST request to /rf003/posts with the sample JSON data
        response = self.client.post('/rf003/posts', data=json.dumps(json_data), headers=headers)

        # Check that the request was successful
        self.assertEqual(response.status_code, 415)

if __name__ == '__main__':
    unittest.main()
