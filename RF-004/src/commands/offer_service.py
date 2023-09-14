import json
import os

import requests


class OfferService:

    @staticmethod
    def create_offer(token, body, postId):
        body["postId"] = postId
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        updated_body_json = json.dumps(body)
        response = requests.post(os.environ["OFFERS_PATH"] + '/offers', headers=headers, data=updated_body_json)
        if response.status_code == 201:
            return response.json(), ""
        else:
            return "", response.status_code
