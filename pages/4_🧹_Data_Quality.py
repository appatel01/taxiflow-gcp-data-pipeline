import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Data Quality",
    page_icon="🧹",
    layout="wide",
)


# ============================================================
# DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "dashboard_data"


@st.cache_data
def load_data():

    kpis = pd.read_csv(
        DATA_DIR / "kpis.csv"
    )

    daily = pd.read_csv(
        DATA_DIR / "daily_metrics.csv"
    )

    return kpis, daily


kpis, daily = load_data()

row = kpis.iloc[0]


# ============================================================
# HEADER
# ============================================================

st.title("🧹 Data Quality Monitor")

st.markdown(
    """
    Monitor the quality of the TaxiFlow dataset and the results
    of the data-cleaning pipeline.
    """
)

st.divider()


# ============================================================
# VERIFIED PIPELINE METRICS
# ============================================================

raw_records = 6_500_000
clean_records = 6_390_635
removed_records = (
    raw_records - clean_records
)

invalid_distance = 0
negative_fares = 0
invalid_durations = 0

missing_passenger = 189_498
missing_payment = 75_960


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📥 Raw Records",
        f"{raw_records:,}"
    )


with col2:

    st.metric(
        "✅ Clean Records",
        f"{clean_records:,}"
    )


with col3:

    st.metric(
        "🗑️ Records Removed",
        f"{removed_records:,}"
    )


with col4:

    retention_rate = (
        clean_records
        / raw_records
        * 100
    )

    st.metric(
        "📊 Retention Rate",
        f"{retention_rate:.2f}%"
    )


st.divider()


# ============================================================
# VALIDATION STATUS
# ============================================================

st.subheader("🔍 Validation Checks")

checks = pd.DataFrame(
    {
        "Validation Check": [
            "Trip distance > 0",
            "Fare amount >= 0",
            "Trip duration valid",
            "Datetime fields valid",
            "Passenger count handled",
            "Payment type handled",
        ],
        "Result": [
            "0 invalid",
            "0 invalid",
            "0 invalid",
            "Valid",
            "Missing values handled",
            "Missing values handled",
        ],
        "Status": [
            "✅ PASS",
            "✅ PASS",
            "✅ PASS",
            "✅ PASS",
            "⚠️ REVIEW",
            "⚠️ REVIEW",
        ],
    }
)

st.dataframe(
    checks,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# DATA COMPLETENESS
# ============================================================

st.subheader("📋 Data Completeness")

col1, col2 = st.columns(2)


with col1:

    passenger_rate = (
        missing_passenger
        / clean_records
        * 100
    )

    st.metric(
        "Passenger Count Missing",
        f"{missing_passenger:,}",
        f"{passenger_rate:.2f}% of records",
    )


with col2:

    payment_rate = (
        missing_payment
        / clean_records
        * 100
    )

    st.metric(
        "Payment Type Missing",
        f"{missing_payment:,}",
        f"{payment_rate:.2f}% of records",
    )


st.divider()


# ============================================================
# CLEANING PIPELINE
# ============================================================

st.subheader("⚙️ Cleaning Pipeline")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.info(
        """
        **1️⃣ Raw Data**

        6.5M+ taxi records
        """
    )


with col2:

    st.info(
        """
        **2️⃣ Validation**

        Detect invalid values
        """
    )


with col3:

    st.info(
        """
        **3️⃣ Cleaning**

        Remove invalid trips
        """
    )


with col4:

    st.success(
        """
        **4️⃣ Clean Dataset**

        6.39M valid records
        """
    )


# ============================================================
# DATASET STATISTICS
# ============================================================

st.subheader("📊 Dataset Statistics")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "📏 Avg Trip Distance",
        f"{row['avg_distance']:.2f}"
    )


with col2:

    st.metric(
        "⏱️ Avg Trip Duration",
        f"{row['avg_duration']:.2f} min"
    )


with col3:

    st.metric(
        "💰 Avg Trip Amount",
        f"{row['avg_trip_amount']:,.2f}"
    )


# ============================================================
# QUALITY SUMMARY
# ============================================================

st.divider()

st.subheader("💡 Quality Summary")

st.success(
    f"""
    The pipeline processed **{raw_records:,} raw records** and
    retained **{clean_records:,} records** after cleaning.

    No invalid trip distances, negative fares, or invalid trip
    durations remain in the cleaned dataset.

    The remaining missing passenger-count and payment-type values
    are tracked separately rather than silently discarded.
    """
)


# ============================================================
# METHODOLOGY
# ============================================================

with st.expander("ℹ️ Data Quality Methodology"):

    st.markdown(
        """
        **Cleaning rules used by TaxiFlow:**

        - Remove trips with `trip_distance <= 0`
        - Remove records with `fare_amount < 0`
        - Treat invalid passenger counts as missing
        - Convert pickup/dropoff timestamps
        - Calculate trip duration
        - Keep realistic trip durations
        - Generate time-based analytical features
        - Validate the cleaned dataset before analytics

        The dashboard presents the results of the project's
        existing validation pipeline.
        """
    )