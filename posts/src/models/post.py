from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy import Column, String, DateTime

from src.models.model import Model, Base


class Post(Model, Base):
    __tablename__ = 'posts'
    routeId = Column(String)
    userId = Column(String)
    expireAt = Column(DateTime)
    createdAt = Column(DateTime)

    def __init__(self, route_id, user_id, expire_at):
        Model.__init__(self)
        self.routeId = route_id
        self.userId = user_id
        self.expireAt = expire_at


class PostJsonSchema(Schema):
    id = fields.String()
    routeId = fields.String()
    userId = fields.String()
    expireAt = fields.DateTime()
    createdAt = fields.DateTime()
