import os

import requests


class UserService:
    @staticmethod
    def get_user_information(token):
        headers = {'Authorization': token}
        response = requests.get(os.environ["USERS_PATH"]+'/users/me', headers=headers)

        if response.status_code == 200:
            try:
                json_data = response.json()
                user_id = json_data.get("id")
                email_user = json_data.get("email")
                return user_id, email_user
            except ValueError:
                return None, None
        else:
            return None, None
