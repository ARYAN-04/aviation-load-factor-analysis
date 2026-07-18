import os
import pandas as pd

from src.config import PROCESSED_DIR

NUMERIC_COLS = [
    "Departures",
    "Hours",
    "Kilometers",
    "Passengers_Carried",
    "RPK",
    "ASK",
    "PLF",
    "ATK",
    "WLF",
]


def load_and_combine_data(directory=PROCESSED_DIR):
    all_files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    temp_list = []
    for file in all_files:
        df = pd.read_csv(os.path.join(directory, file))
        temp_list.append(df)
    return pd.concat(temp_list, ignore_index=True)


def cast_types(df):
    df = df.copy()
    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", ""), errors="coerce"
        )
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%y")
    return df


def load_global_df():
    df = load_and_combine_data()
    return cast_types(df)
