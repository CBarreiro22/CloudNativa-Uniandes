import os

import requests


class ScoreService:
    @staticmethod
    def calculate_score_offer(token, offer_id, route_id):
        body = {
            "id_offer": offer_id,
            "id_route": route_id
        }
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        response = requests.post(os.environ["SCORES_PATH"] + '/score', headers=headers, data=body)

        if response.status_code == 200:
            json_data = response.json()
            score = json_data.get("score")
            return score, ""
        else:
            return "", response.status_code
