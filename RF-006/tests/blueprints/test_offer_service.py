import unittest
from unittest.mock import patch, Mock
from src.commands.offer_service import OfferService


class TestOfferService(unittest.TestCase):
    @patch('src.commands.offer_service.requests.post')
    def test_create_offer_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value =  {
                "id": "123",
                "userId": "23445",
                "createdAt": "05/05/2023"
        }
        mock_post.return_value = mock_response

        token = "test_token"
        post_id = "12345"
        offer_body = {
            "fragile": True,
            "description": "This is a test offer.",
            "size": "LARGE",
            "offer": "valor en dólares de la oferta para llevar el paquete",
        }
        response_service = OfferService.create_offer(token, offer_body, post_id)

        self.assertEqual(response_service[0].get("id"), "123")

    @patch('src.commands.offer_service.requests.post')
    def test_create_offer_success_invalid_body(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        token = "test_token"
        post_id = "12345"
        offer_body = {
            "description": "This is a test offer.",
            "size": "LARGE",
            "offer": "valor en dólares de la oferta para llevar el paquete",
        }
        response_service = OfferService.create_offer(token, offer_body, post_id)

        self.assertEqual(response_service[1], 400)

    if __name__ == '__main__':
        unittest.main()
