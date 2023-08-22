import os
import random
import subprocess
import time
import uuid

import pytest
import requests

from offers.src.main import app

# Cargar variables de entorno desde .env

options = ["LARGE", "MEDIUM", "SMALL"]



class TestOfferOperations:


    @pytest.fixture
    def test_client(self):
        with app.test_client() as client:
            yield client

    def test_post_offer_ok(self,  test_client):

        post_id = str(uuid.uuid4())
        random_integer = random.randint(1, 10000)
        description_test = "Descripción de prueba menor a 140 caracteres"
        random_option = random.choice(options)
        random_boolean = random.choice([True, False])
        offer_data = {
            "postId": post_id,
            "userId": "468dca05-3aa5-4d84-8e70-93b8b54f7a15",
            "description": description_test,
            "size": random_option,
            "fragile": random_boolean,
            "offer": random_integer
        }

        headers = {
            'Authorization': f'Bearer 468dca05-3aa5-4d84-8e70-93b8b54f7a15'
            # Add more headers as needed
        }
        response = test_client.post('/offers', json=offer_data, headers=headers)
        assert response.status_code == 200
        response_data = response.json
        assert "id" in response_data
        assert "createdAt" in response_data
        response = test_client.post("/offers/reset", json='')
        assert response.status_code == 200
        response_data = response.json
        assert "msg" in response_data
