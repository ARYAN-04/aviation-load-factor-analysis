import streamlit as st
import pandas as pd

from src.data_loader import load_global_df
from src.datasets import create_all_datasets
from src.analysis import seasonal_plf_pivot, recovery_trend_long, cargo_scatter_data
from src.plots import plot_seasonal_heatmap, plot_recovery_trend, plot_cargo_scatter

st.set_page_config(page_title="Aviation Load Factor Analysis", layout="wide")
st.title("Aviation Load Factor Analysis")


@st.cache_data
def load_data():
    global_df = load_global_df()
    a, b, c = create_all_datasets(global_df)
    return {"A": a, "B": b, "C": c}


datasets = load_data()

with st.sidebar:
    st.header("Filters")
    dataset_choice = st.radio(
        "Dataset",
        ["A", "B", "C"],
        format_func=lambda x: {
            "A": "A — 3-Year Market (2022-25)",
            "B": "B — 7-Year Recovery (2018-25)",
            "C": "C — Pre/Mid-COVID (2018-21)",
        }[x],
    )

    active_df = datasets[dataset_choice]

    all_airlines = sorted(active_df["Airline"].unique())
    selected_airlines = st.multiselect("Airlines", all_airlines, default=all_airlines)

    type_map = {1: "Domestic", 2: "International"}
    all_types = sorted(active_df["Type"].unique())
    selected_types = st.multiselect(
        "Type",
        all_types,
        default=all_types,
        format_func=lambda t: type_map.get(t, str(t)),
    )

    active_df = active_df[
        (active_df["Airline"].isin(selected_airlines))
        & (active_df["Type"].isin(selected_types))
    ]

tab_heatmap, tab_recovery, tab_cargo = st.tabs(
    [
        "Seasonal Demand Heatmap",
        "COVID Recovery Trend",
        "Cargo Dependency",
    ]
)

with tab_heatmap:
    st.subheader("Seasonal PLF Heatmap")
    if active_df.empty:
        st.warning("No data for selected filters.")
    else:
        pivot = seasonal_plf_pivot(active_df, domestic_only=False)
        fig = plot_seasonal_heatmap(pivot)
        st.plotly_chart(fig, width="stretch")

with tab_recovery:
    st.subheader("7-Year Recovery Trend")
    if dataset_choice != "B":
        st.info("Switch to Dataset B (7-Year Recovery) for this chart.")
    elif active_df.empty:
        st.warning("No data for selected filters.")
    else:
        long_df = recovery_trend_long(active_df, domestic_only=False)
        fig = plot_recovery_trend(long_df)
        st.plotly_chart(fig, width="stretch")

with tab_cargo:
    st.subheader("Cargo Dependency: PLF vs WLF")
    if dataset_choice != "C":
        st.info("Switch to Dataset C (Pre/Mid-COVID) for this chart.")
    elif active_df.empty:
        st.warning("No data for selected filters.")
    else:
        scatter_df = cargo_scatter_data(active_df, domestic_only=False)
        fig = plot_cargo_scatter(scatter_df)
        st.plotly_chart(fig, width="stretch")
