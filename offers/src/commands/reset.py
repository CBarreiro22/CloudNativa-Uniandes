from .base_command import BaseCommand
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from ..models.model import init_db, db_session
from ..models.offer import Offer
import logging

init_db()


class Reset(BaseCommand):

    def drop_offer_table(self):
        try:
            # Borrar la tabla "offer" (ADVERTENCIA: Esto eliminará todos los datos de la tabla)
            logging.info("restarting table Offer")
            db_session.query(Offer).delete()
            db_session.commit()
            logging.info("table Offer has been deleted")
        except Exception as e:
            logging.error("Error al borrar la tabla 'offer':", str(e))

    def execute(self):
        self.drop_offer_table()
        return True
