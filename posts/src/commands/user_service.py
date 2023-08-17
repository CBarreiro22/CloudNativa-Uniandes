import requests

from ..config.config import Config

users_path = Config('.env.development').get('USERS_PATH')


class UserService:
    @staticmethod
    def get_user_information(token):
        headers = {'Authorization': token}
        response = requests.get(users_path, headers=headers)

        if response.status_code == 200:
            try:
                json_data = response.json()
                user_id = json_data.get("id")
                return user_id
            except ValueError:
                return None
        else:
            return None
