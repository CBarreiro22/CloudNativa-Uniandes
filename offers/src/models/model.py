import uuid, datetime

from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from sqlalchemy import String, Integer, DateTime, Boolean, UUID, Enum



db = SQLAlchemy()

class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    postId = db.Column (String, primary_key =True, doc="id de la publicación")
    userId = db.Column(String, doc="identificador del usuario que realizó la oferta")
    description = db.Column(String(length=140), doc="descripción de no más de 140 caracteres sobre el paquete a llevar.")
    size = db.Column(Enum('LARGE', 'MEDIO', 'SMALL', name='size_enum'),
                doc="un valor que describe subjetivamente del tamaño del paquete, puede ser LARGE,MEDIUM,SMALL")
    fragile =db.Column(Boolean, doc="si es un paquete delicado o no")
    offer =db.Column(Integer, doc="valor en dólares de la oferta por llevar el paquete")
    createdAt = db.Column(DateTime, default=datetime.datetime.utcnow,doc="fecha y hora de creación de la publicación")


# Schema definition remains the same

if __name__ == '__main__':
    db.create_all()

class  newOfferResponseJsonSchema(Schema):
    id = fields.String()
    userId  = fields.String()
    createdAt  = fields.DateTime(format="%Y-%m-%dT%H:%M:%S")
class OfferJsonSchema(Schema):
    id = fields.String()
    postId = fields.String()
    description = fields.String()
    size = fields.String()
    fragile = fields.Boolean()
    offer = fields.Integer()
    createdAt = fields.DateTime(format="%Y-%m-%dT%H:%M:%S")
    userId = fields.String()

