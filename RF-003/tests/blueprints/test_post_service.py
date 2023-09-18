import unittest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, Mock
from src.commands.PostService import PostsService


class TestPost_rf003_Service(unittest.TestCase):

    @patch('src.commands.PostService.requests.post')
    def test_post_success(self, mock_post):
        # Mock a successful response
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {"post_id": "123"}

        # Create a sample Post object
        post = {
            "routeId": "1afa9681-149b-49ce-8733-eb4536c5045e",
            "expireAt": "2023-09-18T20:06:56.771Z"
        }

        # Call the post method with headers
        headers = {"Authorization": "Bearer token123"}
        response, status_code = PostsService.post(post, headers)

        # Check that the request was made with the expected data
        mock_post.assert_called_once_with(
            url="http://localhost:3001/posts",
            json={"routeId": "1afa9681-149b-49ce-8733-eb4536c5045e", "expireAt": "2023-09-18T20:06:56.771Z"},
            headers={"Authorization": "Bearer token123"}
        )

        self.assertEqual(status_code, 201)

    @patch('src.commands.PostService.requests.get')
    def test_get_success(self, mock_get):
        # Mock a successful response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{"post_id": "123"}]

        # Call the get method with headers
        route = "route123"
        headers = {"Authorization": "Bearer token123"}
        response = PostsService.get(route, headers)

        # Check that the request was made with the expected data
        mock_get.assert_called_once_with(
            url="http://localhost:3001/posts?route=route123&expire=false&owner=me",
            headers={"Authorization": "Bearer token123"}
        )

        # Check the response data
        self.assertEqual(response.status_code, 200)

    @patch('src.commands.PostService.requests.get')
    def test_get_invalid_token(self, mock_get):
        # Mock a successful response
        mock_response = mock_get.return_value
        mock_response.status_code = 401
        mock_response.json.return_value = [{"post_id": "123"}]

        # Call the get method with headers
        route = "route123"
        headers = {"Authorization": "Bearer token123"}
        response , http_status = PostsService.get(route, headers)

        # Check that the request was made with the expected data
        mock_get.assert_called_once_with(
            url="http://localhost:3001/posts?route=route123&expire=false&owner=me",
            headers={"Authorization": "Bearer token123"}
        )

        # Check the response data
        self.assertEqual(http_status, 401)

    @patch('src.commands.PostService.requests.get')
    def test_get_no_token(self, mock_get):
        # Mock a successful response
        mock_response = mock_get.return_value
        mock_response.status_code = 403
        mock_response.json.return_value = [{"post_id": "123"}]

        # Call the get method with headers
        route = "route123"
        headers = {"Authorization": "Bearer token123"}
        response, http_status = PostsService.get(route, headers)

        # Check that the request was made with the expected data
        mock_get.assert_called_once_with(
            url="http://localhost:3001/posts?route=route123&expire=false&owner=me",
            headers={"Authorization": "Bearer token123"}
        )

        # Check the response data
        self.assertEqual(http_status, 403)


if __name__ == '__main__':
    unittest.main()
