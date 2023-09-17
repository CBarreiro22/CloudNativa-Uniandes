import unittest
from unittest.mock import patch, Mock
from src.commands.RoutesService import RoutesService, Route, RouteResponseJsonSchema

class TestRoutesService(unittest.TestCase):

    @patch('src.commands.RoutesService.requests.get')
    def test_get_success(self, mock_get):
        # Mock a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "1", "createdAt": "2023-09-17T20:06:56.886861"}]
        mock_get.return_value = mock_response

        # Call the get method with headers
        flight = "flight123"
        headers = {"Authorization": "Bearer token123"}
        response  = RoutesService.get(flight, headers)

        # Check that the request was made with the expected data
        mock_get.assert_called_once_with(
            url="http://localhost:3002/routes?flight=flight123",
            headers={"Authorization": "Bearer token123"}
        )

        # Check the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": "1", "createdAt": "2023-09-17T20:06:56.886861"}])

    @patch('src.commands.RoutesService.requests.post')
    def test_post_success(self, mock_post):
        # Mock a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "1", "createdAt": "2023-09-17T20:06:56.886861"}
        mock_post.return_value = mock_response

        # Create a sample Route object
        route = Route(
            flightId="flight123",
            sourceAirportCode="source123",
            sourceCountry="country123",
            destinyAirportCode="destiny123",
            destinyCountry="countryDestiny123",
            bagCost=10.0,
            plannedStartDate="2023-09-18T12:00:00",
            plannedEndDate="2023-09-19T12:00:00"
        )

        # Call the post method with headers
        headers = {"Authorization": "Bearer token123"}
        response = RoutesService.post(route, headers)

        # Check that the request was made with the expected data
        mock_post.assert_called_once_with(
            url="http://localhost:3002/routes",
            json={
                "flightId": "flight123",
                "sourceAirportCode": "source123",
                "sourceCountry": "country123",
                "destinyAirportCode": "destiny123",
                "destinyCountry": "countryDestiny123",
                "bagCost": 10.0,
                "plannedStartDate": "2023-09-18T12:00:00",
                "plannedEndDate": "2023-09-19T12:00:00"
            },
            headers={"Authorization": "Bearer token123"}
        )

        # Check the response data
       ## self.assertEqual(response.status_code, 200)
        self.assertEqual(response, {"id": "1", "createdAt": "2023-09-17T20:06:56.886861"})

    @patch('src.commands.RoutesService.requests.delete')
    def test_delete_success(self, mock_delete):
        # Mock a successful response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        # Call the delete method with headers
        route_id = "1"
        headers = {"Authorization": "Bearer token123"}
        response, http_status_code = RoutesService.delete(route_id, headers)



        # Check the response data
        self.assertEqual(http_status_code, 204)

if __name__ == '__main__':
    unittest.main()
