import pandas as pd

from src.config import FY_MONTHS


def seasonal_plf_pivot(dataset, domestic_only=True):
    df = dataset.copy()
    if domestic_only:
        df = df[df["Type"] == 1]

    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["Month_Name"] = pd.Categorical(
        df["Month_Name"], categories=FY_MONTHS, ordered=True
    )

    return df.pivot_table(
        values="PLF",
        index="Airline",
        columns="Month_Name",
        aggfunc="mean",
        observed=False,
    )


def recovery_trend_pivot(dataset, domestic_only=True):
    df = dataset.copy()
    if domestic_only:
        df = df[df["Type"] == 1]

    trend = df.groupby(["Session", "Airline"])["PLF"].mean().reset_index()
    return trend.pivot(index="Airline", columns="Session", values="PLF")


def recovery_trend_long(dataset, domestic_only=True):
    df = dataset.copy()
    if domestic_only:
        df = df[df["Type"] == 1]

    return df.groupby(["Session", "Airline"])["PLF"].mean().reset_index()


def cargo_dependency_analysis(dataset, domestic_only=True):
    df = dataset.copy()
    if domestic_only:
        df = df[df["Type"] == 1]

    analysis = (
        df.groupby("Airline")
        .agg(
            {
                "PLF": "mean",
                "WLF": "mean",
                "PLF_WLF_Gap": "mean",
            }
        )
        .reset_index()
    )

    return analysis.sort_values(by="PLF_WLF_Gap", ascending=False)


def cargo_yoy_pivot(dataset, domestic_only=True):
    df = dataset.copy()
    if domestic_only:
        df = df[df["Type"] == 1]

    trend = df.groupby(["Session", "Airline"])["PLF_WLF_Gap"].mean().reset_index()
    return trend.pivot(index="Airline", columns="Session", values="PLF_WLF_Gap")


def cargo_scatter_data(dataset, domestic_only=True):
    df = dataset.copy()
    if domestic_only:
        df = df[df["Type"] == 1]
    return df.dropna(subset=["PLF", "WLF"])
