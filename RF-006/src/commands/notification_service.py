import json
import os

import requests


class NotificationService:
    @staticmethod
    def sent_notication(email, RUV, lastForDigits, status, cardHolderName):
        body_request = {
            "email": email,
            "RUV": RUV,
            "lastForDigits": lastForDigits,
            "status": status,
            "cardHolderName": cardHolderName
        }
        updated_body_json = json.dumps(body_request)
        response = requests.post(os.environ["EMAIL_NOTIFICATION_PATH"] + '/funcion-notificar-tarjeta',
                                 data=updated_body_json)
        if response.status_code == 200:
            return response.json(), ''
        else:
            return "", response.status_code
