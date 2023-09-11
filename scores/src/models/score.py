from sqlalchemy import Column, Double, Integer, String
from src.models.model import Model


class Scores(Model):
    __tablename__ = 'scores'

    id_offer = Column(String, name='id_offer', doc="id de la oferta")
    id_route = Column(String, name='id_route', doc="id del trayecto")
    offer = Column(Integer, doc="valor en dólares de la oferta por llevar el paquete")
    size = Column(String, name='size',
                  doc="un valor que describe subjetivamente del tamaño del paquete, puede ser LARGE,MEDIUM,SMALL")
    bagCost = Column(Integer, doc="costo del envío de una maleta en el trayecto")
    score = Column(Double, name='score',
                    doc="ganancia aproximada sobre una oferta realizada.(utilidad = monto oferta - (porcentaje de ocupación de una maleta * valor de la maleta en el trayecto))")

    def __init__(self, id_offer,id_route,offer, size, bagcost, score):
        self.id_offer = id_offer
        self.id_route = id_route
        self.offer = offer
        self.size = size
        self.bagCost = bagcost
        self.score = score

        super().__init__()

