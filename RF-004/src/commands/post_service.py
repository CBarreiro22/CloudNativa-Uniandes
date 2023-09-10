import os
from datetime import datetime, timezone

import requests

ISO_FORMATTER = "%Y-%m-%dT%H:%M:%S"


class PostService:
    @staticmethod
    def get_post_information(token, user_id, post_id):
        headers = {'Authorization': token}
        response = requests.get(os.environ["POSTS_PATH"] + '/posts/' + post_id, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            error = is_valid_user_to_offer(user_id, json_data)
            if not error:
                return json_data.get("routeId"), ''
            return error
        else:
            return "", response.status_code


def is_valid_user_to_offer(user_id, json_data):
    post_user_id = json_data.get("userId")
    if user_id == post_user_id:
        return "", 412
    else:
        if not is_post_expired(json_data):
            return "", 412


def is_post_expired(json_data):
    post_expireAt = json_data.get("expireAt")
    if isinstance(post_expireAt, str):
        try:
            post_expireAt = datetime.strptime(post_expireAt.split('.')[0], ISO_FORMATTER)
        except ValueError:
            return True
    current_datetime = datetime.now(timezone.utc).replace(tzinfo=None)
    try:
        return post_expireAt > current_datetime
    except ValueError:
        return True
