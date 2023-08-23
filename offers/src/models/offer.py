from marshmallow import fields, Schema
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from .model import Model


class newOfferResponseJsonSchema(Schema):
    id = fields.String()
    userId = fields.String()
    createdAt = fields.DateTime(format="%Y-%m-%dT%H:%M:%S")


class OfferJsonSchema(Schema):
    id = fields.String()
    postId = fields.String()
    description = fields.String()
    size = fields.String()
    fragile = fields.Boolean()
    offer = fields.Integer()
    createdAt = fields.DateTime(format="%Y-%m-%dT%H:%M:%S")
    userId = fields.String()


class Offer(Model):
    __tablename__ = 'offer'

    postId = Column(String, primary_key=True, doc="id de la publicación")
    userId = Column(String, doc="identificador del usuario que realizó la oferta")
    description = Column(String(length=140), doc="descripción de no más de 140 caracteres sobre el paquete a llevar.")
    size = Column(String, name='size',
                  doc="un valor que describe subjetivamente del tamaño del paquete, puede ser LARGE,MEDIUM,SMALL")
    fragile = Column(Boolean, doc="si es un paquete delicado o no")
    offer = Column(Integer, doc="valor en dólares de la oferta por llevar el paquete")

    def __init__(self, postId, userId, description, size, fragile, offer):
        self.postId = postId
        self.userId = userId
        self.description = description
        self.size = size
        self.fragile = fragile
        self.offer = offer

        super().__init__()
