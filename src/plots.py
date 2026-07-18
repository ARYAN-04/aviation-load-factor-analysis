import plotly.graph_objects as go
import plotly.express as px


def plot_seasonal_heatmap(pivot_df):
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_df.values,
            x=[str(c) for c in pivot_df.columns],
            y=pivot_df.index.tolist(),
            colorscale="YlGnBu",
            text=pivot_df.values.round(1),
            texttemplate="%{text}",
            textfont={"size": 11},
            colorbar_title="PLF (%)",
            hovertemplate="Airline: %{y}<br>Month: %{x}<br>PLF: %{z:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        title="Seasonal Demand Patterns: Average Domestic PLF (2022-2025)",
        xaxis_title="Financial Year Month",
        yaxis_title="Airline",
        yaxis=dict(autorange="reversed"),
        height=500,
        template="plotly_white",
    )
    return fig


def plot_recovery_trend(long_df):
    session_order = [
        "2018-19",
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
    ]
    fig = px.line(
        long_df,
        x="Session",
        y="PLF",
        color="Airline",
        markers=True,
        title="7-Year Domestic Recovery Trend: The COVID-19 Impact & Bounce Back",
        labels={"PLF": "Avg. Passenger Load Factor (%)", "Session": "Financial Year"},
        category_orders={"Session": session_order},
    )
    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color="red",
        annotation_text="80% Efficiency Threshold",
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        legend_title_text="Airlines",
        hovermode="x unified",
        yaxis_range=[0, 100],
        height=550,
        template="plotly_white",
    )
    return fig


def plot_cargo_scatter(scatter_df):
    session_order = ["2018-19", "2019-20", "2020-21"]
    fig = px.scatter(
        scatter_df,
        x="PLF",
        y="WLF",
        color="Airline",
        facet_col="Session",
        hover_data=["Date"],
        title="Cargo Dependency: PLF vs. WLF (Pre-COVID vs. Mid-COVID)",
        labels={"PLF": "Passenger Load Factor (%)", "WLF": "Weight Load Factor (%)"},
        category_orders={"Session": session_order},
        template="plotly_white",
    )
    for i in range(1, 4):
        fig.add_shape(
            type="line",
            line=dict(dash="dash", color="gray"),
            x0=0,
            x1=100,
            y0=0,
            y1=100,
            row=1,
            col=i,
        )
    fig.update_layout(height=500)
    return fig
