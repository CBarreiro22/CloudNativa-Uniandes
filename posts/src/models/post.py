from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Post:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    routeId = Column(String)
    userId = Column(String)
    expireAt = Column(DateTime)
    createdAt = Column(DateTime)

    def __init__(self):
        self.createdAt = datetime.now().isoformat()
