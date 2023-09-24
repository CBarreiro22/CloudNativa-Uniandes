import os
import random
import time

from src.commands.notification_service import NotificationService
from src.commands.true_native_service import TrueNativeService
from src.models.model import init_db, CreditCard, db_session

init_db()


def polling():
    if valid_thread_no_exist():
        print('starting polling...')
        while True:
            print("entre al while true " + str(random.randint(1, 100)))
            try:
                credit_cards = CreditCard.query.filter_by(status='POR_VERIFICAR').all()

                for card in credit_cards:
                    true_native_response, status_code_error = check_status(ruv=card.ruv)
                    if not status_code_error:
                        card.status = true_native_response.get('status')
                        sent_notification(card.email, card.ruv, card.lastFourDigits,
                                          card.status,
                                          card.cardHolderName)

                db_session.commit()
                time.sleep(1)
                print('sali del while true')

            except Exception as e:
                print(f"Error en el polling: {str(e)}")


def check_status(ruv):
    response_card_request, status_code_error = TrueNativeService.get_card_status(ruv)
    if not status_code_error:
        return response_card_request, ""
    return "", status_code_error


def sent_notification(email, RUV, lastForDigits, status, cardHolderName):
    status_code = NotificationService.sent_notication(email, RUV, lastForDigits, status,
                                                      cardHolderName)
    return status_code


def valid_thread_no_exist():
    mi_valor = os.environ.get('MI_VARIABLE')
    if mi_valor:
        return False
    os.environ['MI_VARIABLE'] = 'mi_valor'
    return True
