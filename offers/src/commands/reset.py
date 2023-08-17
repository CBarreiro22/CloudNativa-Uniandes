from .base_command  import  BaseCommand
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ..models.model import Offer
import logging

Base = declarative_base()
class Reset (BaseCommand):
    def __init__(self, db_url):
        # Crear la conexión a la base de datos
        self.engine = create_engine(db_url)
        # Crear las tablas en la base de datos si no existen
        Base.metadata.create_all(self.engine)

    def drop_offer_table(self):
        try:
            # Borrar la tabla "offer" (ADVERTENCIA: Esto eliminará todos los datos de la tabla)
            logging.info("restarting table Offer")

            logging.info("table Offer has been deleted")
        except Exception as e:
            logging.error("Error al borrar la tabla 'offer':", str(e))
    def execute(self):
        self.drop_offer_table()
        return True
