import os
import pandas as pd

from src.config import FILTERED_DIR


def create_dataset_a(global_df):
    years = ["2022-23", "2023-24", "2024-25"]
    return global_df[global_df["Session"].isin(years)].copy()


def create_dataset_b(global_df):
    years = [
        "2018-19",
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
    ]
    carriers = ["AI", "AIE", "ALLIANCE", "BLUE", "INDIGO"]
    return global_df[
        (global_df["Session"].isin(years)) & (global_df["Airline"].isin(carriers))
    ].copy()


def create_dataset_c(global_df):
    years = ["2018-19", "2019-20", "2020-21"]
    return global_df[
        (global_df["Session"].isin(years)) & (global_df["Airline"] != "AKASA")
    ].copy()


def add_cargo_gap(df):
    df = df.copy()
    df["PLF_WLF_Gap"] = df["WLF"] - df["PLF"]
    return df


def create_all_datasets(global_df):
    a = add_cargo_gap(create_dataset_a(global_df))
    b = add_cargo_gap(create_dataset_b(global_df))
    c = add_cargo_gap(create_dataset_c(global_df))
    return a, b, c


def export_datasets(dataset_a, dataset_b, dataset_c):
    os.makedirs(FILTERED_DIR, exist_ok=True)
    dataset_a.to_csv(
        os.path.join(FILTERED_DIR, "dataset_a_3yr_market.csv"), index=False
    )
    dataset_b.to_csv(
        os.path.join(FILTERED_DIR, "dataset_b_7yr_recovery.csv"), index=False
    )
    dataset_c.to_csv(
        os.path.join(FILTERED_DIR, "dataset_c_3yr_pre_covid.csv"), index=False
    )
    print(f"Exported 3 datasets to {FILTERED_DIR}")
