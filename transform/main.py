import logging
from neighbourhoods import transform_neighbourhoods
from rents import transform_rents


logging.basicConfig(level=10)


def transform():
    logging.info("Transforming neighbourhoods dataset")
    transform_neighbourhoods()

    logging.info("Transforming rents dataset")
    transform_rents()


if __name__ == "__main__":
    transform()
