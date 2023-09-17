import unittest

from src.main import app


class TestPingEndpoint(unittest.TestCase):

    def setUp(self):
        # Configura la aplicación para pruebas
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_ping_response(self):
        # Realiza una solicitud GET al endpoint /rf003/ping
        response = self.app.get('/rf003/ping')

        # Verifica que la respuesta sea "pong" y el código de estado sea 200
        self.assertEqual(response.data.decode('utf-8'), 'pong')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
