import enum
import os
import uuid
from datetime import datetime

from dotenv import load_dotenv
from marshmallow import fields, Schema
from sqlalchemy import Column, DateTime, create_engine, String, Enum
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy_utils import UUIDType

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


class CreditCard(Base):
    __tablename__ = 'credit_cards'
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    token = Column(String(256))
    userId = Column(String)
    lastFourDigits = Column(String(4))
    ruv = Column(String)
    issuer = Column(String)
    status = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    email = Column(String)
    creditCardHash = Column(String)

    def __init__(self, token, userId, lastFourDigits, ruv, issuer, status, email, creditCardHash):
        self.token = token
        self.userId = userId
        self.lastFourDigits = lastFourDigits
        self.ruv = ruv
        self.issuer = issuer
        self.status = status
        self.email = email
        self.creditCardHash = creditCardHash


class CreateCreditCardSchema(Schema):
    id = fields.String()
    userId = fields.String()
    createdAt = fields.String()


class CreditCardSchema(Schema):
    id = fields.String()
    userId = fields.String()
    createdAt = fields.String()
    updatedAt = fields.String()
    status = fields.String()
    issuer = fields.String()
    token = fields.String()
    lastFourDigits = fields.String()
