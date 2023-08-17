import datetime
import os

import unittest
from dotenv import load_dotenv
from flask import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.config import Config
from src.models.model import db, OfferJsonSchema, Offer

# Cargar variables de entorno desde .env
env_config = Config(env_file='../.env.test')
db_user = env_config.get("DB_USER")
print(f"db user: {db_user}")
db_password = env_config.get("DB_PASSWORD")
db_host = env_config.get("DB_HOST")
db_port = env_config.get("DB_PORT")
db_name = env_config.get("DB_NAME")

db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
print(f"uri: {db_uri}")
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
class TestOfferModelAndSchema(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        #db.create_all(bind=engine)

    def tearDown(self):
        db.session.remove()
        #db.drop_all(bind=engine)

    def test_offer_insertion_and_serialization(self):
        offer_data = {
            "postId": "post123",
            "userId": "user123",
            "description": "Test description",
            "size": "LARGE",
            "fragile": False,
            "offer": 50,
            "createdAt": datetime.datetime(2023, 8, 15, 10, 30, 0)
        }

        # Insert the offer into the database
        new_offer = Offer(**offer_data)
        self.session.add(new_offer)
        self.session.commit()

        # Retrieve the offer from the database
        retrieved_offer = self.session.query(Offer).filter_by(postId="post123").first()
        self.assertIsNotNone(retrieved_offer)

        # Serialize the retrieved offer using the schema
        offer_schema = OfferJsonSchema()
        serialized_offer = offer_schema.dump(retrieved_offer)

        # Assertions
        self.assertEqual(serialized_offer["postId"], "post123")
        self.assertEqual(serialized_offer["userId"], "user123")
        self.assertEqual(serialized_offer["description"], "Test description")
        self.assertEqual(serialized_offer["size"], "LARGE")
        self.assertEqual(serialized_offer["fragile"], False)
        self.assertEqual(serialized_offer["offer"], 50)
        self.assertEqual(serialized_offer["createdAt"], "2023-08-15T10:30:00")


if __name__ == "__main__":
    unittest.main()