from sqlalchemy import Column, Integer, String
from src.models.model import Model


class Scores(Model):
    __tablename__ = 'scores'


    offer = Column(Integer, doc="valor en dólares de la oferta por llevar el paquete")
    size = Column(String, name='size',
                  doc="un valor que describe subjetivamente del tamaño del paquete, puede ser LARGE,MEDIUM,SMALL")
    bagCost = Column(Integer, doc="costo del envío de una maleta en el trayecto")
    scores = Column(Integer,
                    doc="ganancia aproximada sobre una oferta realizada.(utilidad = monto oferta - (porcentaje de ocupación de una maleta * valor de la maleta en el trayecto))")

    def __init__(self, offer, size, bagcost, scores):
        self.offer = offer
        self.size = size
        self.bagCost = bagcost
        self.scores = scores

        super().__init__()

