import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone_number = db.Column(db.String(64), nullable=True)
    dni = db.Column(db.String(12), nullable=True)
    full_name = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(128), nullable=True)
    status = db.Column(db.String(128), nullable=False)
    expire_at = db.Column(DateTime, default=datetime.datetime.utcnow)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Usuario(id={self.id}, username={self.username}, email={self.email})>"
