import unittest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, Mock
from src.commands.post_service import PostService, is_post_expired


class TestPostService(unittest.TestCase):

    @patch('src.commands.post_service.requests.get')
    def test_get_post_information_success(self, mock_get):
        # Mocking a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        future_datetime = datetime.now(timezone.utc) + timedelta(days=1)
        mock_response.json.return_value = {
            "id": "123",
            "routeId": "23445",
            "expireAt": future_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            "userId": "12345",
            "createdAt": future_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        }

        mock_get.return_value = mock_response

        token = "test_token"
        user_id = "user123"
        post_id = "post123"
        response_service = PostService.get_post_information(token, user_id, post_id)

        self.assertEqual(response_service[0], "23445")

    @patch('src.commands.post_service.requests.get')
    def test_get_post_information_user_match(self, mock_get):
        # Mocking a response where user_id matches the post's userId
        mock_response = Mock()
        mock_response.status_code = 200
        future_datetime = datetime.now(timezone.utc) + timedelta(days=1)
        mock_response.json.return_value = {
            "id": "123",
            "userId": "user123",
            "expireAt": future_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
        }
        mock_get.return_value = mock_response

        token = "test_token"
        user_id = "user123"
        post_id = "post123"
        response_service = PostService.get_post_information(token, user_id, post_id)

        self.assertEqual(response_service[0], '')
        self.assertEqual(response_service[1], 412)

    @patch('src.commands.post_service.requests.get')
    def test_get_post_information_post_expired(self, mock_get):
        # Mocking a response where the post has expired
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "123",
            "userId": "user123",
            "createdAt": "05/05/2023",
            "expireAt": "2023-09-10T12:00:00"
        }
        mock_get.return_value = mock_response

        token = "test_token"
        user_id = "other_user"
        post_id = "post123"
        response_service = PostService.get_post_information(token, user_id, post_id)

        # Assert that the response contains an error and status code 412
        self.assertEqual(response_service[0], '')
        self.assertEqual(response_service[1], 412)

    @patch('src.commands.post_service.requests.get')
    def test_get_post_information_failure(self, mock_get):
        # Mocking a failed response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        token = "test_token"
        user_id = "user123"
        post_id = "post123"
        response_service = PostService.get_post_information(token, user_id, post_id)

        # Assert that the response contains an empty string and status code 404
        self.assertEqual(response_service[0], '')
        self.assertEqual(response_service[1], 404)

    def test_is_post_expired_value_error(self):
        json_data = {
            "expireAt": "invalid_date_format"
        }
        expired = is_post_expired(json_data)
        self.assertTrue(expired)

    def test_is_post_expired_current_datetime_error(self):
        json_data = {
            "expireAt": "2023-09-10T12:00:00"
        }
        with patch('src.commands.post_service.datetime') as mock_datetime:
            mock_datetime.now.side_effect = TypeError("Invalid current_datetime")
            expired = is_post_expired(json_data)
        self.assertTrue(expired)  # TypeError should result in post considered expired


if __name__ == '__main__':
    unittest.main()
