import logging

from .base_command import BaseCommand
from ..errors.errors import invalid_token, new_offer_business_errors
from ..models.model import db, Offer, OfferJsonSchema

size_values = ["LARGE", "MEDIUM", "SMALL"]


def is_not_size_valid_option(value):
    if value in size_values:
        return False
    return True


class Offers(BaseCommand):
    def __init__(self, post_id, user_id, description, size, fragile, offer):
        # Crear la conexión a la base de datos
        self.post_id = post_id
        self.user_id = user_id
        self.description = description
        self.size = size
        self.fragile = fragile
        self.offer = offer
    def add_offer(self):
        try:
            # Crear una instancia de la clase Offer
            nueva_oferta = Offer(
                postId=self.post_id,
                userId=self.user_id,
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

    def business_validation(self):
        return (is_not_size_valid_option(self.size) or
                self.offer < 0 or
                len(self.description) > 140)
    def execute(self):
        if self.user_id == 0:
            raise invalid_token
        if self.business_validation():
            raise new_offer_business_errors
        new_offer = self.add_offer()
        return new_offer
