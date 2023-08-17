import os

import requests
from dotenv import load_dotenv

loaded = load_dotenv('.env.development')


class UserService:
    @staticmethod
    def get_user_information(token):
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(
            os.environ["USER_SERVICE"], json=None, headers=headers)

        if response.status_code == 200:
            try:
                json_data = response.json()
                user_name = json_data.get("id")
                return user_name
            except ValueError:
                return None
        else:
            return None
