import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Anomaly Detection",
    page_icon="🚨",
    layout="wide",
)


# ============================================================
# DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "dashboard_data"


@st.cache_data
def load_data():

    daily = pd.read_csv(
        DATA_DIR / "daily_metrics.csv"
    )

    daily["pickup_date"] = pd.to_datetime(
        daily["pickup_date"]
    )

    return daily


daily = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🚨 Demand Anomaly Detection")

st.markdown(
    """
    Identify days where taxi demand is unusually high or low
    compared with the normal demand pattern.
    """
)

st.divider()


# ============================================================
# ANOMALY CALCULATION
# ============================================================

window = 7

daily["rolling_mean"] = (
    daily["trip_count"]
    .rolling(
        window=window,
        min_periods=3
    )
    .mean()
)

daily["rolling_std"] = (
    daily["trip_count"]
    .rolling(
        window=window,
        min_periods=3
    )
    .std()
)

daily["upper_bound"] = (
    daily["rolling_mean"]
    + 2 * daily["rolling_std"]
)

daily["lower_bound"] = (
    daily["rolling_mean"]
    - 2 * daily["rolling_std"]
)

daily["anomaly"] = "Normal"

daily.loc[
    daily["trip_count"] > daily["upper_bound"],
    "anomaly"
] = "High Demand"

daily.loc[
    daily["trip_count"] < daily["lower_bound"],
    "anomaly"
] = "Low Demand"


# ============================================================
# COUNTS
# ============================================================

high_anomalies = daily[
    daily["anomaly"] == "High Demand"
]

low_anomalies = daily[
    daily["anomaly"] == "Low Demand"
]

total_anomalies = (
    len(high_anomalies)
    + len(low_anomalies)
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🚨 Total Anomalies",
        f"{total_anomalies:,}"
    )


with col2:

    st.metric(
        "🔴 High Demand Days",
        f"{len(high_anomalies):,}"
    )


with col3:

    st.metric(
        "🔵 Low Demand Days",
        f"{len(low_anomalies):,}"
    )


with col4:

    anomaly_rate = (
        total_anomalies / len(daily) * 100
        if len(daily) > 0
        else 0
    )

    st.metric(
        "📊 Anomaly Rate",
        f"{anomaly_rate:.2f}%"
    )


st.divider()


# ============================================================
# INSIGHT
# ============================================================

st.subheader("💡 Anomaly Summary")


if total_anomalies > 0:

    highest_anomaly = daily.loc[
        daily["trip_count"].idxmax()
    ]

    lowest_anomaly = daily.loc[
        daily["trip_count"].idxmin()
    ]

    st.info(
        f"""
        The dataset contains **{total_anomalies:,} detected
        demand anomalies** using a 7-day rolling baseline.

        The highest recorded daily demand was
        **{int(highest_anomaly["trip_count"]):,} trips**
        on **{highest_anomaly["pickup_date"].date()}**.

        The lowest recorded daily demand was
        **{int(lowest_anomaly["trip_count"]):,} trips**
        on **{lowest_anomaly["pickup_date"].date()}**.
        """
    )

else:

    st.success(
        "No demand anomalies were detected."
    )


# ============================================================
# DEMAND + ANOMALIES CHART
# ============================================================

st.subheader("📈 Demand Anomaly Timeline")


fig = px.line(
    daily,
    x="pickup_date",
    y="trip_count",
    title="Daily Demand with Anomaly Detection",
    labels={
        "pickup_date": "Date",
        "trip_count": "Trips",
    },
)

# Add rolling mean
fig.add_scatter(
    x=daily["pickup_date"],
    y=daily["rolling_mean"],
    mode="lines",
    name="7-Day Rolling Mean",
)


# High anomalies
high = daily[
    daily["anomaly"] == "High Demand"
]

fig.add_scatter(
    x=high["pickup_date"],
    y=high["trip_count"],
    mode="markers",
    name="High Demand",
    marker=dict(
        size=9,
        symbol="triangle-up",
    ),
)


# Low anomalies
low = daily[
    daily["anomaly"] == "Low Demand"
]

fig.add_scatter(
    x=low["pickup_date"],
    y=low["trip_count"],
    mode="markers",
    name="Low Demand",
    marker=dict(
        size=9,
        symbol="triangle-down",
    ),
)


fig.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# HIGH DEMAND TABLE
# ============================================================

st.subheader("🔴 High Demand Anomalies")

if len(high_anomalies) > 0:

    high_display = high_anomalies[
        [
            "pickup_date",
            "trip_count",
            "rolling_mean",
        ]
    ].copy()

    high_display["deviation_percent"] = (
        (
            high_display["trip_count"]
            - high_display["rolling_mean"]
        )
        / high_display["rolling_mean"]
        * 100
    )

    high_display["trip_count"] = (
        high_display["trip_count"]
        .astype(int)
    )

    high_display["rolling_mean"] = (
        high_display["rolling_mean"]
        .round(0)
        .astype(int)
    )

    high_display["deviation_percent"] = (
        high_display["deviation_percent"]
        .round(2)
    )

    high_display.columns = [
        "Date",
        "Trips",
        "Expected Trips",
        "Deviation %",
    ]

    high_display = high_display.sort_values(
        "Deviation %",
        ascending=False
    )

    st.dataframe(
        high_display,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.write("No high-demand anomalies detected.")


# ============================================================
# LOW DEMAND TABLE
# ============================================================

st.subheader("🔵 Low Demand Anomalies")

if len(low_anomalies) > 0:

    low_display = low_anomalies[
        [
            "pickup_date",
            "trip_count",
            "rolling_mean",
        ]
    ].copy()

    low_display["deviation_percent"] = (
        (
            low_display["trip_count"]
            - low_display["rolling_mean"]
        )
        / low_display["rolling_mean"]
        * 100
    )

    low_display["trip_count"] = (
        low_display["trip_count"]
        .astype(int)
    )

    low_display["rolling_mean"] = (
        low_display["rolling_mean"]
        .round(0)
        .astype(int)
    )

    low_display["deviation_percent"] = (
        low_display["deviation_percent"]
        .round(2)
    )

    low_display.columns = [
        "Date",
        "Trips",
        "Expected Trips",
        "Deviation %",
    ]

    low_display = low_display.sort_values(
        "Deviation %"
    )

    st.dataframe(
        low_display,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.write("No low-demand anomalies detected.")