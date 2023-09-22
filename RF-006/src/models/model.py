import enum
import os
import uuid
from datetime import datetime

from dotenv import load_dotenv
from marshmallow import fields, Schema
from sqlalchemy import Column, DateTime, create_engine, String, Enum
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

loaded = load_dotenv('.env.development')
engine = create_engine(
    f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}')

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


def reset_db():
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
        db_session.commit()


class CardIssuer(enum.Enum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    AMERICAN_EXPRESS = "AMERICAN_EXPRESS"
    OTHER = "OTHER"


class CreditCard():
    __tablename__ = 'credit_cards'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()), nullable=False)
    token = Column(String(256))
    userId = Column(String)
    lastFourDigits = Column(String(4))
    ruv = Column(String)
    issuer = Column(Enum(CardIssuer))
    status = Column(String, nullable=False)
    created_At = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_At = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    email = Column (String)

    def __init__(self, token, userId, last_Four_Digits, ruv, issuer, status, email):
        self.token = token
        self.userId = userId
        self.last_Four_Digits = last_Four_Digits
        self.ruv = ruv
        self.issuer = issuer
        self.status = status
        self.email = email
class CreateCreditCardSchema (Schema):
    id  = fields.String ()
    userId = fields.String()
    createdAt = fields.String()

class CreditCardSchema (Schema):
    id = fields.String()
    userId = fields.String()
    createdAt = fields.String()
    token  = fields.String()
    lastFourDigits = fields.String ()





