import time

from src.commands.notification_service import NotificationService
from src.commands.true_native_service import TrueNativeService
from src.models.model import init_db, CreditCard, db_session

init_db()


def polling():
    print('starting polling...')
    while True:
        try:
            credit_cards = CreditCard.query.filter_by(status='POR_VERIFICAR').all()

            for card in credit_cards:
                print(
                    f"Tarjeta de crédito ID: {card.id}, Usuario ID: {card.userId}, Status: {card.status}, RUV: {card.ruv}")
                true_native_response, status_code_error = check_status(ruv=card.ruv)
                if not status_code_error:
                    card.status = true_native_response.get('status')
                    sent_notification( card.email, card.ruv, card.lastFourDigits, card.status,card.cardHolderName)
            db_session.commit()
            time.sleep(1)

        except Exception as e:
            print(f"Error al consultar la base de datos: {str(e)}")


def check_status(ruv):
    response_card_request, status_code_error = TrueNativeService.get_card_status(ruv)
    if not status_code_error:
        return response_card_request, ""
    return "", status_code_error


def sent_notification(email, RUV, lastForDigits, status, cardHolderName):
    response_card_request, status_code_error = NotificationService.sent_notication(email, RUV, lastForDigits, status,
                                                                                   cardHolderName)

    if not status_code_error:
        return response_card_request, ""
    return "", status_code_error
