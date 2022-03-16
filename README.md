# HOMIE ETL

A pipeline to transform neighbourhoods and properties for rent data from Mexico City, and load the data into
a Heroku Postgres instance

## Steps to replicate

1. Create a Heroku app called homie-db, and install [Heroku Postgres](https://www.heroku.com/postgres)
2. Connect to the instance from PgAdmin or psql, and create a Postgres function executing the code in load/assign_neighbourhood_id
3. Login to Heroku using the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
4. Create and activateConda environment from environment.yml
   ```
   conda env create -f environment.yml
   conda activate homie_etl
   ```
5. Run index.py file

## Project Organization

    ├── LICENSE
    ├── README.md
    ├── index.py           <- Main script. Runs transform and load functions.
    │
    ├── data
    │   ├── processed      <- The final, canonical data sets to load.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── load               <- Scripts and files related to the data loading process.
        ├── models         <- SQLAlchemy models classes.
            ├── Neighbourhood.py        <- neighbourhoods table model.
            └── Rents.py        <- rents table model.
        │
        ├── assign_neighbourhood_id.sql  <- Creates trigger function to associate rents with neighbourhoods. To be executed in PgAdmin or psql
        │
        ├── base.py        <- Create database engine, declare SQLAlchemy Session and Base classes.
        ├── engine.py      <- Get database url from heroku, return create engine function.
        └── main.py        <- Contains main load function.
    │
    ├── transform          <- Scripts and files related to the data transform process.
        ├── main.py        <- Contains main load function. Imports transform functions from rents.py and neighbourhoods.py.
        ├── neighbourhoods.py  <- Transformations applied to the neighbourhoods dataset.
        └── rents.py       <- Transformations applied to the rents dataset.
    │
    ├── utils              <- Scripts to help with common tasks.
        └── paths.py   <- Helper functions to relative file referencing across project.
    │
    ├── environment.yml    <- The requirements file for reproducing the environment.
    │
    └── setup.py           <- Makes project pip installable (pip install -e .)
