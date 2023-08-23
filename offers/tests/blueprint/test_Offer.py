import os
import random
import subprocess
import time
import unittest
import uuid
from unittest.mock import patch, Mock

import pytest
import requests

from offers.src.main import app
from offers.src.models.model import db_session

options = ["LARGE", "MEDIUM", "SMALL"]


class TestOfferOperations(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client()

    def tearDown(self):
        db_session.remove()

    @patch('offers.src.commands.userService.UserService.get_user_information')
    def test_post_offer_ok(self, mock_get_user_info):
        mock_get_user_info.return_value = '70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1'
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
        }
        response = self.tester.post('/offers', json=offer_data, headers=headers)
        assert response.status_code == 200
        response_data = response.json
        assert "id" in response_data
        assert "createdAt" in response_data
        response = self.tester.post("/offers/reset", json='')
        assert response.status_code == 200
        response_data = response.json
        assert "msg" in response_data

    @patch('offers.src.commands.userService.UserService.get_user_information')
    def test_post_offer_no_token(self, mock_get_user_info):
        mock_get_user_info.return_value = '70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1'
        random_integer = random.randint(1, 10000)
        description_test = "Descripción de prueba menor a 140 caracteres"
        random_option = random.choice(options)
        random_boolean = random.choice([True, False])
        offer_data = {
            "postId": "fefefefe",
            "userId": "468dca05-3aa5-4d84-8e70-93b8b54f7a15",
            "description": description_test,
            "size": random_option,
            "fragile": random_boolean,
            "offer": random_integer
        }
        response = self.tester.post('/offers', json=offer_data)
        assert response.status_code == 403
