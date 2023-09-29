from time import sleep
from mail_controller import MailController

archivo = open('template_tarjeta.html', 'r', encoding='utf-8')
html = archivo.read()

class NotificacionTarjeta():
    def __init__(self, to, subject, ruv, last_four_digits, status, card_holder_name):
        self.to = to
        self.subject = subject
        self.ruv = ruv
        self.last_four_digits = last_four_digits
        self.status = status
        self.card_holder_name = card_holder_name
    
    def send_email(self):
        body=html.replace('@@ESTATUS', self.status).replace('@@RUV',self.ruv).replace('@@LASTFOURDIGITS',self.last_four_digits).replace('@@NAME', self.card_holder_name)
        if self.status =='VERIFICADA':
            body=body.replace('@@TIPO','alert-success')
        else:
            body=body.replace('@@TIPO','alert-danger')
        subject = 'NOTIFICACION TARJETA'
        MailController.send_email(self.to, '', '', subject, body)