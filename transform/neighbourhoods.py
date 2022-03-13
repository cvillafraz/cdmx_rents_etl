import pandas as pd
import utils.paths as path


def transform_neighbourhoods():
    df_n = pd.read_csv(path.data_raw_dir("neighbourhoods.csv"))

    df_n.drop(columns="Unnamed: 0", inplace=True)
    df_n.rename(columns={"nombre": "name"}, inplace=True)

    df_n.to_parquet(path.data_processed_dir("neighbourhoods.parquet"))


if __name__ == "__main__":
    transform_neighbourhoods()
