from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Boolean
from geoalchemy2 import Geometry
from ..base import Base


class Rent(Base):
    __tablename__ = "rents"

    id = Column(String, primary_key=True)
    neighbourhood_id = Column(ForeignKey("neighbourhoods.id"))
    rooms = Column(Integer)
    bathrooms = Column(Integer)
    parking = Column(Boolean)
    price = Column(Float)
    geom = Column(Geometry(geometry_type="POINT", srid=4326))
    date_in = Column(DateTime)
