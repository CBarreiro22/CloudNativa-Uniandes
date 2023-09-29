from  mail_controller import MailController 

archivo = open('template_usuario.html', 'r', encoding='utf-8')
html = archivo.read()

class NotificacionUsuario():
    def __init__(self, to, subject, ruv, username, dni, fullname, phonenumber,status):
        self.to = to
        self.subject = subject
        self.ruv = ruv
        self.username = username
        self.dni = dni
        self.fullname = fullname
        self.phonenumber = phonenumber
        self.status = status
    
    def send_email(self):
        body=html.replace('@@ESTATUS', self.status).replace('@@RUV',self.ruv).replace('@@USERNAME',self.username).replace('@@DNI', self.dni).replace('@@FULLNAME', self.fullname).replace('@@PHONENUMBER', self.phonenumber)
        if self.status =='VERIFICADA':
            body=body.replace('@@TIPO','alert-success')
        else:
            body=body.replace('@@TIPO','alert-danger')
        subject = 'NOTIFICACION USUARIO'
        MailController.send_email(self.to, '', '', subject, body)