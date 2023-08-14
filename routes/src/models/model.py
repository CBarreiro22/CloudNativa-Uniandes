import uuid
from datetime import datetime
from sqlalchemy import Column,  DateTime, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import UUID

engine= create_engine(f'postgresql://routesu:routesp@localhost:5432/routesdb')
db_session= scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from src.models import route
    Base.metadata.create_all(bind=engine)

def reset_db():
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
        db_session.commit()
class Model():
   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   createdAt = Column(DateTime)
   updatedAt = Column(DateTime)

   def __init__(self):
       self.createdAt = datetime.now()
       self.updatedAt = datetime.now()