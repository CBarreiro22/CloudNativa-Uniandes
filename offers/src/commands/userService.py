import os

import requests


class UserService:
    @staticmethod
    def get_user_information(token):
        headers = {'Authorization': token}
        response = requests.get(os.environ["USERS_PATH"], headers=headers)

        if response.status_code == 200:
            try:
                json_data = response.json()
                user_id = json_data.get("id")
                return user_id
            except ValueError:
                return None
