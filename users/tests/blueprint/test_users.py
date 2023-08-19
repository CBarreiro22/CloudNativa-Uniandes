import pytest

from users.src.main import app
from users.src.models.model import db_session
from users.src.models.user import Users


class TestUserOperations:

    @pytest.fixture
    def test_client(self):
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def user_data(self):
        return {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
            "dni": "12345678",
            "fullName": "Test User",
            "phoneNumber": "123456789"
        }

    @pytest.fixture
    def response(self, user_data, test_client):
        login_data = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        response = test_client.post('/users/auth', json=login_data)
        return response

    @pytest.fixture
    def token(self, response):
        return response.json['token']

    @pytest.fixture
    def user_id(self, response):
        return response.json['id']

    @pytest.fixture
    def headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def user_me_response(self, test_client, headers):
        return test_client.get('/users/me', headers=headers)

    def test_create_user(self, test_client, user_data):
        response = test_client.post('/users', json=user_data)
        assert response.status_code == 201
        response_data = response.json
        assert "id" in response_data
        assert "createdAt" in response_data

    def test_user_exist(self, test_client, user_data):
        response = test_client.post('/users', json=user_data)
        assert response.status_code == 412
        response_data = response.json['mssg']
        assert 'El usuario ya existe' in response_data

    def test_update_user(self, test_client):
        create_data = {
            "username": "testuser2",
            "password": "testpassword2",
            "email": "test2@example.com",
            "dni": "12345678",
            "fullName": "Test User",
            "phoneNumber": "123456789"
        }
        response = test_client.post('/users', json=create_data)
        user_id = response.json["id"]

        # Fetch the user to ensure the updates were applied
        login_data = {
            "username": "testuser2",
            "password": "testpassword2"
        }
        token_response = test_client.post('/users/auth', json=login_data)
        token = token_response.json["token"]

        headers = {
            "Authorization": f"Bearer {token}"
        }
        update_data = {
            "status": "NO_VERIFICADO",
            "dni": "87654321",
            "fullName": "Updated User",
            "phoneNumber": "987654321"
        }
        update_url = f'/users/{user_id}'
        response = test_client.patch(update_url, json=update_data)

        assert response.status_code == 200
        response_data = response.json
        assert "msg" in response_data
        response = test_client.get('/users/me', headers=headers)
        assert response.status_code == 200
        user_data = response.json
        assert user_data["status"] == update_data["status"]
        assert user_data["dni"] == update_data["dni"]
        assert user_data["fullName"] == update_data["fullName"]
        assert user_data["phoneNumber"] == update_data["phoneNumber"]

    # ... (Other test methods)

    def test_get_user_info(self, test_client, user_me_response):  # Create a test user first

        assert user_me_response.status_code == 200
        response_data = user_me_response.json
        assert "id" in response_data
        assert "username" in response_data
        assert "email" in response_data
        assert "fullName" in response_data
        assert "dni" in response_data
        assert "phoneNumber" in response_data
        assert "status" in response_data

    def test_generate_token(self, test_client, response):
        assert response.status_code == 200
        response_data = response.json
        assert "id" in response_data
        assert "token" in response_data
        assert "expireAt" in response_data

    def test_reset_database(self, test_client):
        response = test_client.post('/users/reset')

        assert response.status_code == 200
        response_data = response.json
        assert "msg" in response_data

        # You can also add additional assertions to ensure that the database is actually empty
        # after the reset. This depends on how your database setup and testing environment work.
        # For example, if you are using SQLAlchemy and an in-memory SQLite database, you can
        # do something like this:

        # Check if the Users table is empty after the reset
        with app.app_context():
            user_count = db_session.query(Users).count()
            assert user_count == 0
        # Check if the session is closed after the reset
        # assert db_session.is_active == False
