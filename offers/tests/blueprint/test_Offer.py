import os
import random
import uuid

import pytest
import requests

from offers.src.main import app
# Cargar variables de entorno desde .env

options = ["LARGE", "MEDIUM", "SMALL"]


@pytest.fixture(scope="class")
def setup_user_and_get_id(request):
    users_path = os.getenv("USERS_PATH")
    data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com",
        "dni": "12345678",
        "fullName": "Test User",
        "phoneNumber": "123456789"
    }
    response_create_user = requests.post(users_path + '/users', json=data)
    user_id = response_create_user.json()['id']
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = requests.post(users_path + '/users/auth', json=data)
    token = response.json()['token']

    def teardown():
        requests.post(users_path + '/users/reset', json='')

    request.addfinalizer(teardown)
    return user_id, token


class TestOfferOperations:

    @pytest.fixture
    def test_client(self):
        with app.test_client() as client:
            yield client

    def test_post_offer_ok(self, setup_user_and_get_id, test_client):
        user_id, token = setup_user_and_get_id
        post_id = str(uuid.uuid4())
        random_integer = random.randint(1, 10000)
        description_test = "Descripción de prueba menor a 140 caracteres"
        random_option = random.choice(options)
        random_boolean = random.choice([True, False])
        offer_data = {
            "postId": post_id,
            "userId": user_id,
            "description": description_test,
            "size": random_option,
            "fragile": random_boolean,
            "offer": random_integer
        }

        headers = {
            'Authorization': f'Bearer {token}'
            # Add more headers as needed
        }
        print(offer_data)
        response = test_client.post('/offers', json=offer_data, headers=headers)
        print(response.json)
        assert response.status_code == 200
        response_data = response.json
        assert "id" in response_data
        assert "createdAt" in response_data
        response = test_client.post("/offers/reset", json='')
        assert response.status_code == 200
        response_data = response.json
        assert "msg" in response_data
