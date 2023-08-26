import unittest
from unittest.mock import Mock, patch

from offers.src.commands.userService import UserService


class TestUserService(unittest.TestCase):
    @patch('offers.src.commands.userService.requests.get')
    def test_get_user_information_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1"}
        mock_get.return_value = mock_response

        token = "468dca05-3aa5-4d84-8e70-93b8b54f7a15"
        user_id = UserService.get_user_information(token)

        self.assertEqual(user_id, "70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1")

    @patch('offers.src.commands.userService.requests.get')
    def test_get_user_information_invalid_token(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"id": "70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1"}
        mock_get.return_value = mock_response

        self.assertEqual(mock_response.status_code, 401)

    @patch('offers.src.commands.userService.requests.get')
    def test_get_user_information_invalid_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        token = "468dca05-3aa5-4d84-8e70-93b8b54f7a15"
        user_id = UserService.get_user_information(token)

        self.assertIsNone(user_id)

    @patch('offers.src.commands.userService.requests.get')
    def test_get_user_information_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError
        mock_get.return_value = mock_response

        token = "468dca05-3aa5-4d84-8e70-93b8b54f7a15"
        user_id = UserService.get_user_information(token)

        self.assertIsNone(user_id)

    if __name__ == '__main__':
        unittest.main()