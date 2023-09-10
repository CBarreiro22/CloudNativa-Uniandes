# import unittest
# from unittest.mock import patch, Mock
# from src.commands.user_service import UserService
#
#
# class TestUserService(unittest.TestCase):
#     @patch('src.commands.user_service.requests.get')
#     def test_get_user_information_success(self, mock_get):
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {"id": "test_user_id"}
#         mock_get.return_value = mock_response
#
#         token = "test_token"
#         user_id = UserService.get_user_information(token)
#
#         self.assertEqual(user_id, "test_user_id")
#
#     @patch('src.commands.user_service.requests.get')
#     def test_get_user_information_invalid_response(self, mock_get):
#         mock_response = Mock()
#         mock_response.status_code = 400
#         mock_get.return_value = mock_response
#
#         token = "test_token"
#         user_id = UserService.get_user_information(token)
#
#         self.assertIsNone(user_id)
#
#     @patch('src.commands.user_service.requests.get')
#     def test_get_user_information_invalid_json(self, mock_get):
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_response.json.side_effect = ValueError
#         mock_get.return_value = mock_response
#
#         token = "test_token"
#         user_id = UserService.get_user_information(token)
#
#         self.assertIsNone(user_id)
#
#     if __name__ == '__main__':
#         unittest.main()
