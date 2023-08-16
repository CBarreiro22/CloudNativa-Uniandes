import uuid, datetime

from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, DateTime, Boolean, UUID, Enum
from sqlalchemy.orm import declarative_base


db = SQLAlchemy()

class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    postId = db.Column (String, primary_key =True, doc="id de la publicación"),
    userId = db.Column(String, doc="identificador del usuario que realizó la oferta"),
    description = db.Column(String(length=140), doc="descripción de no más de 140 caracteres sobre el paquete a llevar.")
    size = db.Column(Enum('LARGE', 'MEDIO', 'SMALL', name='size_enum'),
                doc="un valor que describe subjetivamente del tamaño del paquete, puede ser LARGE,MEDIUM,SMALL"),
    fragile =db.Column(Boolean, doc="si es un paquete delicado o no"),
    offer =db.Column(Integer, doc="valor en dólares de la oferta por llevar el paquete"),
    createdAt = db.Column(DateTime, default=datetime.datetime.utcnow,doc="fecha y hora de creación de la publicación")



class  OfferJsonSchema(Schema):
    id = fields.Str()
    userId  = fields.Str()
    createdAt  = fields.DateTime

