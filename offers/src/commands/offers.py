import logging
from enum import Enum

from .base_command import BaseCommand
from ..errors.errors import invalid_token, new_offer_business_errors
from ..models.model import db, Offer, newOfferResponseJsonSchema


class SizeEnum(Enum):
    LARGE = 'LARGE'
    MEDIUM = 'MEDIUM'
    SMALL = 'SMALL'

class Offers(BaseCommand):
    def __init__(self, post_id=None, user_id=None, description=None, size=None, fragile=None, offer=None):
        self.post_id = post_id
        self.user_id = user_id
        self.description = description
        self.size = size
        self.fragile = fragile
        self.offer = offer

    def add_offer(self):
        self.business_validation()
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
        if self.user_id == 0:
            raise invalid_token

        if (is_not_validate_size(self.size) or
                self.offer < 0 or
                len(self.description) > 140):
                raise new_offer_business_errors

    def execute(self):
        return self.add_offer()


def is_not_validate_size(input_string):
    try:
        size_enum_value = SizeEnum[input_string]
        return False  # La cadena es un valor válido del Enum
    except KeyError:
        return True

