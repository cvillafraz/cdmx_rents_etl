import subprocess
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=10)


def make_engine():
    DATABASE_URL = (
        subprocess.check_output(
            "heroku config:get DATABASE_URL -a homie-db", shell=True
        )
        .decode()
        .replace("postgres", "postgresql")
        .strip()
    )
    return create_engine(DATABASE_URL)
