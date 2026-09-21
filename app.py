import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TaxiFlow Analytics",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.75;
        margin-top: 5px;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    [data-testid="stMetric"] {
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        padding: 18px;
        background: rgba(128, 128, 128, 0.05);
    }

    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dashboard_data"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_dashboard_data():

    kpis = pd.read_csv(
        DATA_DIR / "kpis.csv"
    )

    daily = pd.read_csv(
        DATA_DIR / "daily_metrics.csv"
    )

    hourly = pd.read_csv(
        DATA_DIR / "hourly_metrics.csv"
    )

    hourly_daily = pd.read_csv(
        DATA_DIR / "hourly_daily_metrics.csv"
    )

    weekday = pd.read_csv(
        DATA_DIR / "weekday_metrics.csv"
    )

    distance = pd.read_csv(
        DATA_DIR / "distance_distribution.csv"
    )

    locations = pd.read_csv(
        DATA_DIR / "top_locations.csv"
    )

    daily["pickup_date"] = pd.to_datetime(
        daily["pickup_date"]
    )

    hourly_daily["pickup_date"] = pd.to_datetime(
        hourly_daily["pickup_date"]
    )

    return (
        kpis,
        daily,
        hourly,
        hourly_daily,
        weekday,
        distance,
        locations,
    )


try:

    (
        kpis,
        daily,
        hourly,
        hourly_daily,
        weekday,
        distance,
        locations,
    ) = load_dashboard_data()

except Exception as e:

    st.error(
        "Dashboard data could not be loaded."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚕 TaxiFlow")

st.sidebar.markdown(
    "### Dashboard Filters"
)

st.sidebar.caption(
    "Use the controls below to explore the dataset."
)


# ------------------------------------------------------------
# DATE FILTER
# ------------------------------------------------------------

min_date = daily["pickup_date"].min().date()
max_date = daily["pickup_date"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Pickup Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(
        selected_dates[0]
    )

    end_date = pd.Timestamp(
        selected_dates[1]
    )

else:

    start_date = pd.Timestamp(min_date)
    end_date = pd.Timestamp(max_date)


# ------------------------------------------------------------
# HOUR FILTER
# ------------------------------------------------------------

selected_hour = st.sidebar.selectbox(
    "🕐 Pickup Hour",
    ["All Hours"] + list(range(24))
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_daily = daily[
    (daily["pickup_date"] >= start_date)
    &
    (daily["pickup_date"] <= end_date)
].copy()


filtered_hourly_daily = hourly_daily[
    (hourly_daily["pickup_date"] >= start_date)
    &
    (hourly_daily["pickup_date"] <= end_date)
].copy()


if selected_hour != "All Hours":

    filtered_hourly_daily = filtered_hourly_daily[
        filtered_hourly_daily["pickup_hour"]
        == selected_hour
    ]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div>
        <div class="hero-title">🚕 TaxiFlow Analytics</div>
        <div class="hero-subtitle">Interactive Taxi Trip Analytics Dashboard</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    f"Showing data from {start_date.date()} "
    f"to {end_date.date()} • "
    "Python • Mage • BigQuery • Streamlit"
)

st.divider()


# ============================================================
# KPI CARDS
# ============================================================

row = kpis.iloc[0]

total_trips = filtered_daily["trip_count"].sum()

total_revenue = filtered_daily["amount_sum"].sum()

if total_trips > 0:

    avg_trip_amount = (
        total_revenue / total_trips
    )

else:

    avg_trip_amount = 0


avg_distance = (
    filtered_daily["distance_sum"].sum()
    / total_trips
    if total_trips > 0
    else 0
)

avg_duration = row["avg_duration"]



col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "🚕 Total Trips",
        f"{int(total_trips):,}"
    )


with col2:

    st.metric(
        "📏 Avg Distance",
        f"{avg_distance:.2f}"
    )


with col3:

    st.metric(
        "⏱️ Avg Duration",
        f"{avg_duration:.2f} min"
    )


with col4:

    st.metric(
        "💰 Avg Trip Amount",
        f"{avg_trip_amount:,.2f}"
    )


with col5:

    revenue_display = (
        f"{total_revenue / 1_000_000_000:.2f}B"
        if total_revenue >= 1_000_000_000
        else f"{total_revenue / 1_000_000:.2f}M"
        if total_revenue >= 1_000_000
        else f"{total_revenue:,.2f}"
    )

    st.metric(
        "💵 Total Revenue",
        revenue_display
    )


st.divider()


# ============================================================
# DEMAND ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📈 Demand Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# HOURLY DEMAND
# ------------------------------------------------------------

with col1:

    hourly_display = hourly.copy()

    if selected_hour != "All Hours":

        hourly_display = hourly_display[
            hourly_display["pickup_hour"]
            == selected_hour
        ]

    fig_hourly = px.line(
        hourly_display,
        x="pickup_hour",
        y="trip_count",
        markers=True,
        title="Trips by Hour of Day",
        labels={
            "pickup_hour": "Pickup Hour",
            "trip_count": "Number of Trips",
        },
    )

    fig_hourly.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_hourly,
        use_container_width=True
    )


# ------------------------------------------------------------
# DAILY DEMAND
# ------------------------------------------------------------

with col2:

    fig_daily = px.line(
        filtered_daily,
        x="pickup_date",
        y="trip_count",
        title="Daily Trip Demand",
        labels={
            "pickup_date": "Date",
            "trip_count": "Number of Trips",
        },
    )

    fig_daily.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_daily,
        use_container_width=True
    )


# ============================================================
# REVENUE
# ============================================================

st.markdown(
    '<div class="section-title">💰 Revenue Analysis</div>',
    unsafe_allow_html=True
)

fig_revenue = px.area(
    filtered_daily,
    x="pickup_date",
    y="amount_sum",
    title="Daily Revenue Trend",
    labels={
        "pickup_date": "Date",
        "amount_sum": "Revenue",
    },
)

fig_revenue.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)


# ============================================================
# WEEKDAY + DISTANCE
# ============================================================

col1, col2 = st.columns(2)


with col1:

    fig_weekday = px.bar(
        weekday,
        x="day_name",
        y="trip_count",
        title="Trips by Day of Week",
        labels={
            "day_name": "Day",
            "trip_count": "Number of Trips",
        },
    )

    st.plotly_chart(
        fig_weekday,
        use_container_width=True
    )


with col2:

    fig_distance = px.bar(
        distance,
        x="distance_range",
        y="trip_count",
        title="Trip Distance Distribution",
        labels={
            "distance_range": "Distance",
            "trip_count": "Number of Trips",
        },
    )

    st.plotly_chart(
        fig_distance,
        use_container_width=True
    )


# ============================================================
# PICKUP LOCATIONS
# ============================================================

st.markdown(
    '<div class="section-title">📍 Pickup Location Analysis</div>',
    unsafe_allow_html=True
)

location_display = locations.sort_values(
    "trip_count",
    ascending=True
)

fig_location = px.bar(
    location_display,
    x="trip_count",
    y="PULocationID",
    orientation="h",
    title="Top 15 Pickup Locations",
    labels={
        "PULocationID": "Pickup Location ID",
        "trip_count": "Number of Trips",
    },
)

st.plotly_chart(
    fig_location,
    use_container_width=True
)


# ============================================================
# LOCATION TABLE
# ============================================================

with st.expander("📊 View Pickup Location Details"):

    display_locations = locations.copy()

    display_locations["avg_amount"] = (
        display_locations["avg_amount"]
        .round(2)
    )

    display_locations.columns = [
        "Pickup Location ID",
        "Trip Count",
        "Total Amount",
        "Average Trip Amount",
    ]

    st.dataframe(
        display_locations,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PIPELINE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">⚙️ TaxiFlow Data Pipeline</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(
        "🐍 **Python**\n\n"
        "Cleaning & Feature Engineering"
    )

with col2:
    st.info(
        "⚙️ **Mage**\n\n"
        "ETL Orchestration"
    )

with col3:
    st.info(
        "☁️ **BigQuery**\n\n"
        "Data Warehouse & SQL"
    )

with col4:
    st.info(
        "📊 **Streamlit**\n\n"
        "Analytics Dashboard"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "TaxiFlow — End-to-End Taxi Data Engineering & Analytics"
)

st.caption(
    "Dataset: Generic taxi-trip benchmark dataset • "
    "6.39M+ cleaned records"
)