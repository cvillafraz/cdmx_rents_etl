import logging
import math
import pandas as pd
from base import engine, Base, Session
from models import Neighbourhood, Rent
import utils.paths as path


logging.basicConfig(level=10)


def _load_neighbourhoods(session: Session):
    df_n = pd.read_parquet(path.data_processed_dir("neighbourhoods.parquet"))
    logging.info("Inserting on neighbourhoods table")
    for row in df_n.itertuples():
        neighbourhood = Neighbourhood(
            id=getattr(row, "id"), 
            name=getattr(row, "name"), 
            geom=getattr(row, "geom")
        )
        session.add(neighbourhood)
    session.commit()


def _load_rents(session: Session):
    df_rents = pd.read_parquet(path.data_processed_dir("rents.parquet"))
    logging.info("Inserting on rents table")
    for row in df_rents.itertuples():
        # Save rooms, bathrooms and price to check whether they are NaN later
        rooms = getattr(row, "rooms")
        bathrooms = getattr(row, "bathrooms") 
        price = getattr(row, "price")

        rent = Rent(
            id=getattr(row, "id"), 
            neighbourhood_id=getattr(row, "neighbourhood_id"),
            rooms=math.floor(rooms) if not math.isnan(rooms) else None,
            bathrooms=math.floor(bathrooms) if not math.isnan(bathrooms) else None,
            parking=getattr(row, "parking"),
            price=price if not math.isnan(price) else None, 
            geom=getattr(row, "geom"),
            date_in=getattr(row, "date_in")
        )
        session.add(rent)
    session.commit()
    


def _set_up_database():
    with engine.connect() as conn:
        logging.info("Enabling POSTGIS extension (if not enabled)")
        conn.execute("CREATE EXTENSION IF NOT EXISTS POSTGIS")

        logging.info("Creating tables")
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        logging.info("Creating trigger on rents")
        conn.execute("""CREATE TRIGGER on_insert_rent
                        BEFORE INSERT ON rents
                        FOR EACH ROW
                        EXECUTE PROCEDURE assign_neighbourhood_id()""")

def load():
    _set_up_database()
    session = Session()
    _load_neighbourhoods(session)
    _load_rents(session)


if __name__ == "__main__":
    load()
    