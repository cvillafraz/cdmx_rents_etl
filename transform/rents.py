import pandas as pd
import numpy as np
import warnings
import utils.paths as path
from uuid import uuid4

warnings.filterwarnings("error")
from shapely import wkb
from shapely.geometry import Point


def transform_rents():
    df_rents = pd.read_csv(path.data_raw_dir("rents.csv"))
    df_rents = _fix_inconsistent_rooms(df_rents)
    df_rents = _fix_numeric_values(df_rents)
    df_rents = _date_to_datetime(df_rents)
    df_rents = _rename_cols(df_rents)
    df_rents = _make_uuid_col(df_rents)
    df_rents = _set_price_outliers_as_nan(df_rents)
    df_rents = _make_points_from_lon_lat(df_rents)
    df_rents = _drop_unnecesary_cols(df_rents)

    # Create empty column for neighbourhood_id foreign key
    df_rents["neighbourhood_id"] = None

    df_rents.to_parquet(path.data_processed_dir("rents.parquet"))


def _drop_unnecesary_cols(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=["latitude", "longitude", "Unnamed: 0"])


def _make_points_from_lon_lat(df: pd.DataFrame) -> pd.DataFrame:
    df["geom"] = df.apply(
        lambda r: wkb.dumps(Point(r["longitude"], r["latitude"]), hex=True, srid=4326),
        axis=1,
    )

    return df


def _set_price_outliers_as_nan(df: pd.DataFrame) -> pd.DataFrame:
    df["price"] = df["price"].mask((df["price"] <= 1) | (df["price"] >= 1e6))
    return df


def _rename_cols(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={"precio": "price"})


def _fix_numeric_values(df: pd.DataFrame) -> pd.DataFrame:
    df["longitude"] *= -1

    df["rooms"] = pd.to_numeric(df["rooms"], errors="coerce", downcast="float")

    return df


def _make_uuid_col(df: pd.DataFrame) -> pd.DataFrame:
    df["id"] = [uuid4().hex for _ in range(len(df.index))]
    return df


def _date_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df["date_in"] = pd.to_datetime(df["date_in"])
    return df


def _fix_inconsistent_rooms(df: pd.DataFrame) -> pd.DataFrame:
    rooms_patterns = [
        (df["rooms"].str.contains("uno|one", case=False, na=False), "1"),
        (df["rooms"].str.contains("dos", case=False, na=False), "2"),
        (df["rooms"].str.contains("cinco", case=False, na=False), "5"),
        (df["rooms"].str.contains("uno y medio", case=False, na=False), None),
        (df["rooms"].str.contains("8.1", case=False, na=False), "8"),
    ]

    rooms_criteria, rooms_values = zip(*rooms_patterns)
    df["rooms_normal"] = np.select(rooms_criteria, rooms_values, None)
    # Replace "None" values with original position
    df["rooms_normal"] = df["rooms_normal"].combine_first(df["rooms"])

    df["rooms"] = df["rooms_normal"]
    return df.drop(columns=["rooms_normal"])


if __name__ == "__main__":
    transform_rents()
