import unittest
from unittest.mock import patch, Mock
from src.commands.score_service import ScoreService


class TestScoreService(unittest.TestCase):
    @patch('src.commands.score_service.requests.post')
    def test_calculate_score_offer_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "score": 54342
        }
        mock_post.return_value = mock_response

        token = "test_token"
        offer_id = "34324324"
        route_id = "2323213"
        response_service = ScoreService.calculate_score_offer(token, offer_id, route_id)

        self.assertEqual(response_service[0], 54342)

    @patch('src.commands.score_service.requests.post')
    def test_calculate_score_offer_fail(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        token = "test_token"
        offer_id = "34324324"
        route_id = "2323213"
        response_service = ScoreService.calculate_score_offer(token, offer_id, route_id)

        self.assertEqual(response_service[1], 400)

if __name__ == '__main__':
        unittest.main()
