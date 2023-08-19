import datetime, os

import requests
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.config import Config
from src.main import app
from src.models.model import db, newOfferResponseJsonSchema, Offer

# Cargar variables de entorno desde .env
env_config = Config(env_file='../.env.test')
db_user = env_config.get("DB_USER")
print(f"db user: {db_user}")
db_password = env_config.get("DB_PASSWORD")
db_host = env_config.get("DB_HOST")
db_port = env_config.get("DB_PORT")
db_name = env_config.get("DB_NAME")
USERS_PATH = env_config.get("USERS_PATH")
os.environ['ENV'] = 'test'

db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
print(f"uri: {db_uri}")
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
class TestOfferOperations:

    def __init__(self):
        self.session = None

    def test_post_offer_ok(self):
        with app.test_client() as test_client:
            self.token = self.setup_user_token()
            offer_data = {
                "postId": "post123",
                "userId": "user123",
                "description": "Test description",
                "size": "LARGE",
                "fragile": False,
                "offer": 50,
                "createdAt": datetime.datetime(2023, 8, 15, 10, 30, 0)
            }
            headers = {
                'Authorization': f'{self.token}',
                # Add more headers as needed
            }
            response = test_client.post("/oferrs",json=offer_data, headers= headers)
            assert response.status_code == 200
            response_data = response.json
            assert "id" in response_data
            assert "createdAt" in response_data


    def setup_user_token (self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
            "dni": "12345678",
            "fullName": "Test User",  # Changed from "fullname" to "fullName"
            "phoneNumber": "123456789"
        }
        response = requests.post(USERS_PATH + '/users', json=data)
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = requests.post(USERS_PATH + '/users/auth', json=data)
        token = response.json['token']
        return token

