import logging
from load.main import load
from transform.main import transform

if __name__ == "__main__":
    logging.info("ETL started, transforming datasets")
    transform()

    logging.info("Started loading data process")
    load()

    logging.info("ETL Finished")
