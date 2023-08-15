import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phoneNumber = db.Column(db.String(64))
    dni = db.Column(db.String(12), nullable=True)  # Hacerlo opcional
    fullName = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(128))
    salt = db.Column(db.String(128))
    token = db.Column(db.String(128))
