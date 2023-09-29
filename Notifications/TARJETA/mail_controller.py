from json import load
from operator import truediv
import smtplib
from email.mime.text import MIMEText

sender = "Miso2022.pruebasautomatizadas@gmail.com"
password = "sogg xrzo jgpn gfxm"

class MailController:
    @staticmethod
    def send_email(to, cc, bcc, subject, body):
        try:
            msg = MIMEText(body, 'html')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(to)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, to, msg.as_string())
            return True
        except:
            return False