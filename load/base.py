from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from engine import make_engine

engine = make_engine()
Session = sessionmaker(engine)
Base = declarative_base()
