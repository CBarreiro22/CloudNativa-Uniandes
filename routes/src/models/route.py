from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, DateTime
from src.models.model import Model, Base


class Route(Model, Base):
    __tablename__ = 'routes'
    flightId = Column(String)
    sourceAirportCode = Column(String)
    sourceCountry = Column(String)
    destinyAirportCode = Column(String)
    destinyCountry = Column(String)
    bagCost = Column(Integer)
    plannedStartDate = Column(DateTime)
    plannedEndDate = Column(DateTime)

    def __init__(self, flight_id, source_airport_code, source_country, destiny_airport_code, destiny_country, bag_cost, planned_start_date, planned_end_date):
        Model.__init__(self)
        self.flightId = flight_id
        self.sourceAirportCode = source_airport_code
        self.sourceCountry = source_country
        self.destinyAirportCode = destiny_airport_code
        self.destinyCountry = destiny_country
        self.bagCost = bag_cost
        self.plannedStartDate = planned_start_date
        self.plannedEndDate = planned_end_date


class RouteJsonSchema(Schema):
    id=fields.String()
    flightId = fields.String()
    sourceAirportCode = fields.String()
    sourceCountry = fields.String()
    destinyAirportCode=fields.String()
    destinyCountry=fields.String()
    bagCost=fields.Number()
    plannedStartDate=fields.DateTime()
    plannedEndDate=fields.DateTime()
    createdAt = fields.DateTime()
   
