from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
import datetime
import logging

from sqlalchemy.testing.config import db_url

from .base_command import BaseCommand
from ..models.model import db, Offer, OfferJsonSchema


class Offers(BaseCommand):
    def __init__(self, db_url, postId, userId, description, size, fragile, offer):
        # Crear la conexión a la base de datos
        self.postId = postId
        self.userId = userId
        self.description = description
        self.size = size
        self.fragile = fragile
        self.offer = offer
    def add_offer(self):
        try:
            # Crear una instancia de la clase Offer
            nueva_oferta = Offer(
                postId=self.postId,
                userId=self.userId,
                description=self.description,
                size=self.size,
                fragile=self.fragile,
                offer=self.offer
            )
            # Crear una sesión para interactuar con la base de datos

            # Agregar la nueva oferta a la sesión y confirmar la transacción para que se guarde en la base de datos
            db.session.add(nueva_oferta)
            db.session.commit()
            logging.info("Oferta agregada exitosamente.")
            return nueva_oferta
        except Exception as e:
            logging.error("Error al agregar la oferta:", str(e))

    def execute(self):
        nueva_offerta = self.add_offer()
        return OfferJsonSchema().dump(nueva_offerta)
