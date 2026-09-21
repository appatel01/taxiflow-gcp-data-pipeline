import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


st.set_page_config(
    page_title="Demand Intelligence",
    page_icon="🧠",
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

    hourly = pd.read_csv(
        DATA_DIR / "hourly_metrics.csv"
    )

    weekday = pd.read_csv(
        DATA_DIR / "weekday_metrics.csv"
    )

    daily["pickup_date"] = pd.to_datetime(
        daily["pickup_date"]
    )

    return daily, hourly, weekday


daily, hourly, weekday = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🧠 Demand Intelligence")

st.markdown(
    "Understand when taxi demand is highest, lowest, "
    "and how demand changes throughout the dataset."
)

st.divider()


# ============================================================
# CALCULATIONS
# ============================================================

peak_hour_row = hourly.loc[
    hourly["trip_count"].idxmax()
]

lowest_hour_row = hourly.loc[
    hourly["trip_count"].idxmin()
]

peak_weekday_row = weekday.loc[
    weekday["trip_count"].idxmax()
]

peak_hour = int(
    peak_hour_row["pickup_hour"]
)

peak_hour_trips = int(
    peak_hour_row["trip_count"]
)

lowest_hour = int(
    lowest_hour_row["pickup_hour"]
)

lowest_hour_trips = int(
    lowest_hour_row["trip_count"]
)

peak_weekday = peak_weekday_row["day_name"]

peak_weekday_trips = int(
    peak_weekday_row["trip_count"]
)

average_trips_per_day = (
    daily["trip_count"].mean()
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🔥 Peak Hour",
        f"{peak_hour:02d}:00",
    )


with col2:

    st.metric(
        "🚕 Peak Hour Trips",
        f"{peak_hour_trips:,}",
    )


with col3:

    st.metric(
        "📅 Busiest Day",
        peak_weekday,
    )


with col4:

    st.metric(
        "📊 Avg Trips / Day",
        f"{average_trips_per_day:,.0f}",
    )


st.divider()


# ============================================================
# AUTOMATIC INSIGHT
# ============================================================

st.subheader("💡 Key Insight")

st.info(
    f"Taxi demand reaches its highest hourly level around "
    f"**{peak_hour:02d}:00**, with approximately "
    f"**{peak_hour_trips:,} trips** in the aggregated dataset. "
    f"The lowest hourly demand occurs around "
    f"**{lowest_hour:02d}:00**, with approximately "
    f"**{lowest_hour_trips:,} trips**."
)


# ============================================================
# HOURLY DEMAND
# ============================================================

st.subheader("🕐 Demand by Hour")

fig_hourly = px.bar(
    hourly,
    x="pickup_hour",
    y="trip_count",
    labels={
        "pickup_hour": "Pickup Hour",
        "trip_count": "Number of Trips",
    },
    title="Taxi Demand Throughout the Day",
)

fig_hourly.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_hourly,
    use_container_width=True,
)


# ============================================================
# WEEKDAY DEMAND
# ============================================================

st.subheader("📅 Demand by Day of Week")

fig_weekday = px.bar(
    weekday,
    x="day_name",
    y="trip_count",
    labels={
        "day_name": "Day",
        "trip_count": "Number of Trips",
    },
    title="Taxi Demand by Weekday",
)

st.plotly_chart(
    fig_weekday,
    use_container_width=True,
)


# ============================================================
# DAILY TREND
# ============================================================

st.subheader("📈 Daily Demand Trend")

fig_daily = px.line(
    daily,
    x="pickup_date",
    y="trip_count",
    labels={
        "pickup_date": "Date",
        "trip_count": "Number of Trips",
    },
    title="Daily Taxi Demand",
)

fig_daily.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_daily,
    use_container_width=True,
)


# ============================================================
# SUMMARY TABLE
# ============================================================

st.subheader("📊 Hourly Demand Summary")

hourly_display = hourly.copy()

hourly_display["pickup_hour"] = (
    hourly_display["pickup_hour"]
    .apply(lambda x: f"{int(x):02d}:00")
)

hourly_display.columns = [
    "Pickup Hour",
    "Trip Count",
]

st.dataframe(
    hourly_display,
    use_container_width=True,
    hide_index=True,
)