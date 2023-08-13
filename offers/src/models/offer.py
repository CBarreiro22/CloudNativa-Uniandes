import uuid, datetime
from enum import Enum

from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import validates
from .model  import  Model, Base



class Offer(Model, Base):
    __tablename__ = 'offer'
    id = Column(String, default=str(uuid.uuid4())),
    postId = Column (String, PrimaryKey =True, doc="id de la publicación"),
    userId = Column(String, doc="identificador del usuario que realizó la oferta"),
    description = Column(String(length=140), doc="descripción de no más de 140 caracteres sobre el paquete a llevar.")
    size = Column(Enum('LARGE', 'MEDIO', 'SMALL', name='size_enum'), doc="un valor que describe subjetivamente del tamaño del paquete, puede ser LARGE,MEDIUM,SMALL"),
    fragile =Column(Boolean, doc="si es un paquete delicado o no"),
    offer =Column(Integer, doc="valor en dólares de la oferta por llevar el paquete"),
    createdAt = Column(DateTime, default=datetime.datetime.utcnow,doc="fecha y hora de creación de la publicación"),

    # Constructor
    def  __init__(self,  postId,userId,description,size,fragile,offer):
        Model.__init__(self)
        self.postId  =  postId
        self.userId  =  userId
        self.description = description
        self.size = size
        self.fragile = fragile
        self.offer = offer


class  OfferJsonSchema(Schema):
    id = fields.Str()
    userId  = fields.Str()
    createdAt  = fields.DateTime

