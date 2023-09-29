import json
import os

import requests


class NotificationService:
    @staticmethod
    def sent_notication(email, RUV, lastForDigits, status, cardHolderName):
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json'
        }
        body_request = {
            "email": email,
            "RUV": RUV,
            "lastForDigits": lastForDigits,
            "status": status,
            "cardHolderName": cardHolderName
        }
        updated_body_json = json.dumps(body_request)
        response = requests.post(os.environ["EMAIL_NOTIFICATION_PATH"] + '/funcion-notificar-tarjeta',
                                 headers=headers, data=updated_body_json)
        return response.status_code

