import random
import unittest
import uuid
from unittest.mock import patch

import setuptools
from faker import Faker

from offers.src.main import app
from offers.src.models.model import db_session

size_options = ["LARGE", "MEDIUM", "SMALL"]


def get_offer_data(post_id, user_id, description, size, fragile, offer):
    offer_data = {
        "postId": post_id,
        "userId": user_id,
        "description": description,
        "size": size,
        "fragile": fragile,
        "offer": offer
    }

    return offer_data


class TestOfferOperations(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client()

    def tearDown(self):
        db_session.remove()

    @patch('offers.src.commands.userService.UserService.get_user_information')
    def test_post_offer_ok(self, mock_get_user_info):
        mock_get_user_info.return_value = '70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1'
        post_id = str(uuid.uuid4())
        fake = Faker()
        description = fake.text(max_nb_chars=140)
        random_integer = random.randint(1, 10000)

        random_size = random.choice(size_options)
        random_fragile = random.choice([True, False])
        offer_data = get_offer_data(post_id=post_id,
                                    user_id=uuid.uuid4(),
                                    description=description, size=random_size, fragile=random_fragile,
                                    offer=random_integer)
        headers = {
            'Authorization': f'Bearer 468dca05-3aa5-4d84-8e70-93b8b54f7a15'
        }
        response = self.tester.post('/offers', json=offer_data, headers=headers)
        assert response.status_code == 201
        response_data = response.json
        assert "id" in response_data
        assert "userId" in response_data
        assert "createdAt" in response_data
        response = self.tester.post("/offers/reset", json='')
        assert response.status_code == 200
        response_data = response.json
        assert "msg" in response_data

    @patch('offers.src.commands.userService.UserService.get_user_information')
    def test_post_offer_no_token(self, mock_get_user_info):
        mock_get_user_info.return_value = '70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1'
        random_integer = random.randint(1, 10000)
        post_id = str(uuid.uuid4())
        fake = Faker()
        description = fake.text(max_nb_chars=140)

        random_size = random.choice(size_options)
        random_fragile = random.choice([True, False])
        offer_data = get_offer_data(post_id=post_id,
                                    user_id=uuid.uuid4(),
                                    description=description, size=random_size, fragile=random_fragile,
                                    offer=random_integer)

        response = self.tester.post('/offers', json=offer_data)
        assert response.status_code == 403

    @patch('offers.src.commands.userService.UserService.get_user_information')
    def test_post_offer_missing_fields(self, mock_get_user_info):
        mock_get_user_info.return_value = '70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1'
        offer_data = "{'offer':'1000'}"
        headers = {
            'Authorization': f'Bearer 468dca05-3aa5-4d84-8e70-93b8b54f7a15'
        }
        response = self.tester.post('/offers', json=offer_data, headers=headers)
        assert response.status_code == 400

    @patch('offers.src.commands.userService.UserService.get_user_information')
    def test_post_offer_invalid_size(self, mock_get_user_info):
        mock_get_user_info.return_value = '70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1'
        post_id = str(uuid.uuid4())
        fake = Faker()
        description = fake.text(max_nb_chars=140)
        random_integer = random.randint(1, 10000)

        random_size = random.choice(size_options)
        random_fragile = random.choice([True, False])


        headers = {
            'Authorization': f'Bearer 468dca05-3aa5-4d84-8e70-93b8b54f7a15'
        }
        offer_data = get_offer_data(post_id=post_id,
                                    user_id=uuid.uuid4(),
                                    description=description, size="INVALID", fragile=random_fragile,
                                    offer=random_integer)
        response = self.tester.post('/offers', json=offer_data, headers=headers)
        assert response.status_code == 412
        description = fake.text(max_nb_chars=200) + fake.text(max_nb_chars=200)
        offer_data = get_offer_data(post_id=post_id,
                                    user_id=uuid.uuid4(),
                                    description=description, size=random_size, fragile=random_fragile,
                                    offer=random_integer)
        response = self.tester.post('/offers', json=offer_data, headers=headers)
        assert response.status_code == 412
        offer_data = get_offer_data(post_id=post_id,
                                    user_id=uuid.uuid4(),
                                    description=fake.text(max_nb_chars=140), size=random_size, fragile=random_fragile,
                                    offer=-1)
        response = self.tester.post('/offers', json=offer_data, headers=headers)

    @patch('offers.src.commands.userService.UserService.get_user_information')
    def test_get_offer_all(self, mock_get_user_info):
        mock_get_user_info.return_value = '70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1'
        headers = {
            'Authorization': f'Bearer 468dca05-3aa5-4d84-8e70-93b8b54f7a15'
        }
        post_id = 0
        for i in range (5):
            post_id = str(uuid.uuid4())
            fake = Faker()
            description = fake.text(max_nb_chars=140)
            random_integer = random.randint(1, 10000)

            random_size = random.choice(size_options)
            random_fragile = random.choice([True, False])
            offer_data = get_offer_data(post_id=post_id,
                                        user_id=uuid.uuid4(),
                                        description=description, size=random_size, fragile=random_fragile,
                                        offer=random_integer)

            self.tester.post('/offers', json=offer_data,headers=headers)

        response_get = self.tester.get('/offers',  headers=headers)
        offer_list_data = response_get.get_json()
        assert response_get.status_code == 200
        assert len(offer_list_data) >= 5
        id = offer_list_data[0].get ("id")

        response_get = self.tester.get(f'/offers/{id}', headers=headers)
        assert response_get.status_code == 200

        response_get = self.tester.get(f'/offers/8eb3e4b9-6b33-417b-857d-9c2b5e9c3a5a', headers=headers)
        assert response_get.status_code == 404

        response = self.tester.get(f'/offers?post={post_id}',headers=headers)
        response.get_json()
        assert response.status_code == 200

        response = self.tester.get(f'/offers?owner=me', headers=headers)
        response.get_json()
        assert response.status_code == 200

        response = self.tester.get(f'/offers?owner=me&post={post_id}', headers=headers)
        response.get_json()
        assert response.status_code == 200

        response = self.tester.post("/offers/reset", json='')
        assert response.status_code == 200

    @patch('offers.src.commands.userService.UserService.get_user_information')
    def test_delete_offer(self, mock_get_user_info):
        mock_get_user_info.return_value = '70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1'
        post_id = str(uuid.uuid4())
        fake = Faker()
        description = fake.text(max_nb_chars=140)
        random_integer = random.randint(1, 10000)

        random_size = random.choice(size_options)
        random_fragile = random.choice([True, False])
        headers = {
            'Authorization': f'Bearer 468dca05-3aa5-4d84-8e70-93b8b54f7a15'
        }
        offer_data = get_offer_data(post_id=post_id,
                                    user_id=uuid.uuid4(),
                                    description=description, size=random_size, fragile=random_fragile,
                                    offer=random_integer)
        response = self.tester.post('/offers', json = offer_data, headers = headers)
        assert response.status_code == 201
        response_data = response.get_json()
        offer_id = response_data.get('id')
        assert len (offer_id) > 0
        response = self.tester.delete('/offers/70a3a66e-5c2e-4f87-9f5c-12c8eac9b2b1')

        assert response.status_code == 403
        response = self.tester.delete(f'/offers/{offer_id}',headers=headers)
        assert response.status_code == 200

        response = self.tester.delete("/offers/1", json=offer_data, headers=headers)
        assert response.status_code == 400
        response = self.tester.delete("/offers/8eb3e4b9-6b33-417b-857d-9c2b5e9c3a5a", headers=headers)
        assert response.status_code == 404

    def test_health(self):
        response = self.tester.get ('/offers/ping')
        assert response.status_code == 200
    def test_reset(self):
        response = self.tester.post ('/offers/reset')
        assert response.status_code == 200