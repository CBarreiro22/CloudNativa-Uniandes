import unittest

from src.blueprints.rf003 import get_route


class TestGetRoute(unittest.TestCase):

    def test_get_route(self):
        # Datos de prueba
        json_data = {
            "flightId": "FL123",
            "origin": {
                "airportCode": "ABC",
                "country": "CountryA"
            },
            "destiny": {
                "airportCode": "XYZ",
                "country": "CountryB"
            },
            "bagCost": 50,
            "plannedStartDate": "2023-10-01T08:00:00.000Z",
            "plannedEndDate": "2023-10-10T18:00:00.000Z"
        }

        # Llama a la función get_route con los datos de prueba
        route = get_route(json_data)

        # Verifica que los atributos de la ruta se hayan configurado correctamente
        self.assertEqual(route.flightId, "FL123")
        self.assertEqual(route.sourceAirportCode, "ABC")
        self.assertEqual(route.sourceCountry, "CountryA")
        self.assertEqual(route.destinyAirportCode, "XYZ")
        self.assertEqual(route.destinyCountry, "CountryB")
        self.assertEqual(route.bagCost, 50)
        self.assertEqual(route.plannedStartDate, "2023-10-01T08:00:00.000Z")
        self.assertEqual(route.plannedEndDate, "2023-10-10T18:00:00.000Z")

if __name__ == '__main__':
    unittest.main()
