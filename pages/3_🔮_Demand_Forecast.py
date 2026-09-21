import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Demand Forecast",
    page_icon="🔮",
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

    daily = (
        daily
        .sort_values("pickup_date")
        .reset_index(drop=True)
    )

    return daily


daily = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🔮 Demand Forecast")

st.markdown(
    """
    Forecast future taxi demand using historical daily demand,
    recent trend, and weekly seasonality.
    """
)

st.caption(
    "Forecast method: seasonal baseline + recent trend. "
    "This is an analytical forecast, not a production prediction service."
)

st.divider()


# ============================================================
# FORECAST SETTINGS
# ============================================================

forecast_days = st.selectbox(
    "🔮 Forecast Horizon",
    [7, 14, 30],
    index=0,
)


# ============================================================
# PREPARE DATA
# ============================================================

series = (
    daily[
        [
            "pickup_date",
            "trip_count",
        ]
    ]
    .copy()
)

series["trip_count"] = (
    series["trip_count"]
    .astype(float)
)


# ============================================================
# HOLDOUT / MODEL WINDOW
# ============================================================

season_length = 7

recent_days = min(
    56,
    len(series)
)

recent = series.tail(
    recent_days
).copy()


# ============================================================
# WEEKLY SEASONAL BASELINE
# ============================================================

recent["day_of_week"] = (
    recent["pickup_date"]
    .dt.dayofweek
)


seasonal_profile = (
    recent
    .groupby("day_of_week")["trip_count"]
    .mean()
)


# ============================================================
# RECENT TREND
# ============================================================

trend_window = min(
    28,
    len(recent)
)

trend_data = recent.tail(
    trend_window
).copy()

x = np.arange(
    len(trend_data)
)

y = trend_data["trip_count"].values


if len(trend_data) >= 2:

    slope, intercept = np.polyfit(
        x,
        y,
        1
    )

else:

    slope = 0
    intercept = y[0] if len(y) else 0


# ============================================================
# CREATE FORECAST
# ============================================================

last_date = series["pickup_date"].max()

future_dates = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=forecast_days,
    freq="D",
)


future = pd.DataFrame(
    {
        "pickup_date": future_dates
    }
)

future["day_of_week"] = (
    future["pickup_date"]
    .dt.dayofweek
)


# Seasonal component
future["seasonal_prediction"] = (
    future["day_of_week"]
    .map(seasonal_profile)
)


# Recent level
recent_mean = (
    recent["trip_count"]
    .mean()
)


# Trend adjustment
future["trend_index"] = np.arange(
    len(trend_data),
    len(trend_data) + forecast_days
)

future["trend_prediction"] = (
    intercept
    + slope * future["trend_index"]
)


# Blend seasonal pattern and trend
future["predicted_trips"] = (
    0.65 * future["seasonal_prediction"]
    + 0.35 * future["trend_prediction"]
)


# Protect against negative predictions
future["predicted_trips"] = (
    future["predicted_trips"]
    .clip(lower=0)
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

average_forecast = (
    future["predicted_trips"]
    .mean()
)

peak_forecast = future.loc[
    future["predicted_trips"].idxmax()
]

lowest_forecast = future.loc[
    future["predicted_trips"].idxmin()
]


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🔮 Forecast Days",
        f"{forecast_days}",
    )


with col2:

    st.metric(
        "📊 Avg Predicted Trips",
        f"{average_forecast:,.0f}",
    )


with col3:

    st.metric(
        "🔥 Peak Forecast",
        f"{peak_forecast['predicted_trips']:,.0f}",
    )


with col4:

    st.metric(
        "📉 Lowest Forecast",
        f"{lowest_forecast['predicted_trips']:,.0f}",
    )


st.divider()


# ============================================================
# INSIGHT
# ============================================================

st.subheader("💡 Forecast Insight")

st.info(
    f"""
    Based on the historical demand pattern, the next
    **{forecast_days} days** have an average predicted demand
    of approximately **{average_forecast:,.0f} trips per day**.

    The highest predicted demand is approximately
    **{peak_forecast['predicted_trips']:,.0f} trips** on
    **{peak_forecast['pickup_date'].date()}**.
    """
)


# ============================================================
# HISTORICAL + FORECAST CHART
# ============================================================

st.subheader("📈 Historical Demand vs Forecast")


# Show recent historical period for readability
history_display = series.tail(90)


fig = go.Figure()


# Historical demand
fig.add_trace(
    go.Scatter(
        x=history_display["pickup_date"],
        y=history_display["trip_count"],
        mode="lines",
        name="Historical Demand",
    )
)


# Forecast
fig.add_trace(
    go.Scatter(
        x=future["pickup_date"],
        y=future["predicted_trips"],
        mode="lines+markers",
        name="Forecast",
        line=dict(
            dash="dash"
        ),
    )
)


fig.update_layout(
    title="Historical Demand and Future Forecast",
    xaxis_title="Date",
    yaxis_title="Number of Trips",
    hovermode="x unified",
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


# ============================================================
# FORECAST TABLE
# ============================================================

st.subheader("📋 Forecast Details")

forecast_display = future[
    [
        "pickup_date",
        "predicted_trips",
    ]
].copy()


forecast_display["predicted_trips"] = (
    forecast_display["predicted_trips"]
    .round(0)
    .astype(int)
)


forecast_display.columns = [
    "Date",
    "Predicted Trips",
]


st.dataframe(
    forecast_display,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# METHODOLOGY
# ============================================================

with st.expander("ℹ️ Forecast Methodology"):

    st.markdown(
        """
        **How the forecast works:**

        1. Historical daily taxi demand is loaded from the
           processed dashboard dataset.

        2. A weekly seasonal profile is calculated using the
           day of week.

        3. A recent 28-day linear trend is estimated.

        4. The forecast combines:
           - 65% weekly seasonal pattern
           - 35% recent trend

        5. Negative predictions are clipped to zero.

        This approach is intentionally lightweight and transparent
        for portfolio demonstration purposes.
        """
    )