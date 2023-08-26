import os
import uuid
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy_utils import UUIDType

ENV = None

try:
    ENV = os.getenv('ENV')

except KeyError:
    print("no testing mode")

if ENV is not None and ENV == 'test':
    engine = create_engine('sqlite:///:memory:')
else:
    loaded = load_dotenv('.env.development')
    engine = create_engine(
        f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}')

db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


def reset_db():
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
        db_session.commit()


class Model:
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)

    def __init__(self):
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
