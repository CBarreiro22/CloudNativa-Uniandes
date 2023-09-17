import unittest
from datetime import datetime

from src.blueprints.rf003 import validate_new_offer_schema


class TestNewOfferSchemaValidation(unittest.TestCase):

    def test_valid_schema(self):
        # Datos de prueba que cumplen con el esquema
        valid_data = {
            "flightId": "FL123",
            "expireAt": "2023-09-30T12:00:00.000Z",
            "plannedStartDate": "2023-10-01T08:00:00.000Z",
            "plannedEndDate": "2023-10-10T18:00:00.000Z",
            "origin": {
                "airportCode": "ABC",
                "country": "CountryA"
            },
            "destiny": {
                "airportCode": "XYZ",
                "country": "CountryB"
            },
            "bagCost": 50
        }

        # Debería pasar la validación sin errores
        self.assertIsNone(validate_new_offer_schema(valid_data))

    def test_invalid_schema(self):
        # Datos de prueba que no cumplen con el esquema (faltan campos)
        invalid_data = {
            "flightId": "FL123",
            "expireAt": "2023-09-30T12:00:00.000Z",
            # Faltan campos requeridos
        }

        # Debería lanzar una excepción de validación de esquema
        with self.assertRaises(Exception):  # Ajusta esto según el tipo de excepción real que raises
            validate_new_offer_schema(invalid_data)

if __name__ == '__main__':
    unittest.main()
