from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, DateTime
from src.models.model import Model, Base


class Route(Model, Base):
    __tablename__ = 'routes'
    flightId = Column(String)
    startAirportCode = Column(String)
    startCountry = Column(String)
    endAirportCode = Column(String)
    endCountry = Column(String)
    bagCost = Column(Integer)
    plannedStartDate = Column(DateTime)
    plannedEndDate = Column(DateTime)

    def __init__(self, flight_id, start_airport_code, start_country, end_airport_code, end_country, bag_cost, planned_start_date, planned_end_date):
        Model.__init__(self)
        self.flightId = flight_id
        self.startAirportCode = start_airport_code
        self.startCountry = start_country
        self.endAirportCode = end_airport_code
        self.endCountry = end_country
        self.bagCost = bag_cost
        self.plannedStartDate = planned_start_date
        self.plannedEndDate = planned_end_date


class RouteJsonSchema(Schema):
    id=fields.String()
    flightId = fields.String()
    startAirportCode = fields.String()
    startCountry = fields.String()
    endAirportCode=fields.String()
    endCountry=fields.String()
    bagCost=fields.Number()
    plannedStartDate=fields.DateTime()
    plannedEndDate=fields.DateTime()
    createdAt = fields.DateTime()
   
