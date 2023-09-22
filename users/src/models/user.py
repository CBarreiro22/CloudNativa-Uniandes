import datetime
from sqlalchemy import Column, String, DateTime
from .model import Model


class Users(Model):
    __tablename__ = 'users'
    STATUS_CHOICES = ("POR_VERIFICAR", "NO_VERIFICADO", "VERIFICADO")

    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    phone_number = Column(String(64), nullable=True)
    dni = Column(String(12), nullable=True)
    full_name = Column(String(64), nullable=True)
    password = Column(String(128), nullable=False)
    salt = Column(String(128), nullable=False)
    token = Column(String(128), nullable=True)
    status = Column(String(128), default="POR_VERIFICAR")
    expireAt = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, password, salt, email, phone_number=None, dni=None, full_name=None):
        self.username = username
        self.password = password
        self.salt = salt
        self.email = email
        self.phone_number = phone_number
        self.dni = dni
        self.full_name = full_name

        super().__init__()
