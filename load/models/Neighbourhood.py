from sqlalchemy import Column, String, Integer
from geoalchemy2 import Geometry
from base import Base


class Neighbourhood(Base):
    __tablename__ = "neighbourhoods"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326))
