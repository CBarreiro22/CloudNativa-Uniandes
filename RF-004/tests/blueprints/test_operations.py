import unittest
from unittest.mock import patch

from flask import Flask

from src.main import operations_blueprint


class TestOperationsBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(operations_blueprint)
        self.tester = self.app.test_client()

    @patch('src.commands.post_service.PostService.get_post_information')
    @patch('src.commands.offer_service.OfferService.create_offer')
    @patch('src.commands.score_service.ScoreService.calculate_score_offer')
    @patch('src.commands.user_service.UserService.get_user_information')
    def test_create_offer_of_post_success(self, mock_get_user_info, mock_calculate_score, mock_create_offer,
                                          mock_get_post_info):
        mock_get_user_info.return_value = 'test_user_id'
        mock_get_post_info.return_value = ("route_id", None)
        mock_create_offer.return_value = ({"id": "123", "createdAt": "2023-09-10T12:00:00"}, None)
        mock_calculate_score.return_value = (10, None)

        response = self.tester.post('/rf004/posts/123/offers', json={
            "description": "Description",
            "size": "LARGE",
            "fragile": True,
            "offer": 100
        }, headers={'Authorization': 'Bearer test_token'})

        self.assertEqual(response.status_code, 201)
        expected_response = {
            "data": {
                "id": "123",
                "userId": "test_user_id",
                "createdAt": "2023-09-10T12:00:00",
                "postId": "123"
            },
            "msg": "Se creo la oferta dada la publicación con esta utilidad: 10"
        }
        self.assertEqual(response.json, expected_response)

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_create_offer_of_post_invalid_token(self, mock_get_user_info):
        # Simulate an invalid token scenario
        mock_get_user_info.return_value = None

        response = self.tester.post("/rf004/posts/test_post_id/offers", json={
            'description': 'test_description',
            'size': 'test_size',
            'fragile': True,
            'offer': 'test_offer'
        }, headers={'Authorization': 'Bearer invalid_token'})

        self.assertEqual(response.status_code, 401)

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_create_offer_of_post_missing_fields(self, mock_get_user_info):
        mock_get_user_info.return_value = "3334323"

        response = self.tester.post("/rf004/posts/test_post_id/offers", json={},
                                    headers={'Authorization': 'Bearer test_token'})

        self.assertEqual(response.status_code, 400)

    def test_check_health(self):
        response = self.tester.get("/rf004/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'pong')


if __name__ == '__main__':
    unittest.main()
