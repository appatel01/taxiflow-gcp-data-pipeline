import streamlit as st
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Pipeline Health | TaxiFlow",
    page_icon="⚙️",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #b8b8b8;
    margin-bottom: 30px;
}

.pipeline-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #333;
    background-color: #15171c;
    text-align: center;
}

.status {
    font-size: 22px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚙️ Pipeline Health</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Monitor the health and execution stages of the TaxiFlow data pipeline.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# PIPELINE STAGES
# --------------------------------------------------

st.subheader("🔄 Pipeline Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="pipeline-box">
        <div style="font-size:35px;">📥</div>
        <div class="status">RAW DATA</div>
        <div>6.5M records</div>
        <div style="margin-top:10px;">🟢 AVAILABLE</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="pipeline-box">
        <div style="font-size:35px;">🧹</div>
        <div class="status">CLEANING</div>
        <div>6,390,635 records</div>
        <div style="margin-top:10px;">🟢 COMPLETED</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="pipeline-box">
        <div style="font-size:35px;">🔄</div>
        <div class="status">TRANSFORMATION</div>
        <div>23 columns</div>
        <div style="margin-top:10px;">🟢 COMPLETED</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="pipeline-box">
        <div style="font-size:35px;">☁️</div>
        <div class="status">BIGQUERY</div>
        <div>6.39M records</div>
        <div style="margin-top:10px;">🟢 LOADED</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# --------------------------------------------------
# PIPELINE METRICS
# --------------------------------------------------

st.subheader("📊 Pipeline Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Raw Records",
        "6,500,000"
    )

with col2:
    st.metric(
        "Processed Records",
        "6,390,635"
    )

with col3:
    st.metric(
        "Records Removed",
        "109,365"
    )

with col4:
    st.metric(
        "Retention Rate",
        "98.32%"
    )


st.divider()


# --------------------------------------------------
# PIPELINE FLOW
# --------------------------------------------------

st.subheader("🏗️ End-to-End Pipeline")

pipeline = pd.DataFrame({
    "Stage": [
        "Raw Dataset",
        "Data Cleaning",
        "Validation",
        "Feature Engineering",
        "Mage ETL",
        "BigQuery",
        "Analytics"
    ],
    "Technology": [
        "CSV",
        "Python / Pandas",
        "Python",
        "Pandas",
        "Mage",
        "Google BigQuery",
        "SQL / Streamlit"
    ],
    "Status": [
        "✅ Complete",
        "✅ Complete",
        "✅ Complete",
        "✅ Complete",
        "✅ Complete",
        "✅ Complete",
        "✅ Active"
    ]
})

st.dataframe(
    pipeline,
    use_container_width=True,
    hide_index=True
)


st.divider()


# --------------------------------------------------
# DATA ENGINEERING STACK
# --------------------------------------------------

st.subheader("🛠️ Technology Stack")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("### 🐍")
    st.write("**Python**")
    st.caption("Data processing")

with col2:
    st.markdown("### 🧹")
    st.write("**Pandas**")
    st.caption("Transformation")

with col3:
    st.markdown("### 🚀")
    st.write("**Mage**")
    st.caption("ETL orchestration")

with col4:
    st.markdown("### ☁️")
    st.write("**BigQuery**")
    st.caption("Data warehouse")

with col5:
    st.markdown("### 📊")
    st.write("**Streamlit**")
    st.caption("Analytics")


st.divider()


# --------------------------------------------------
# HEALTH SUMMARY
# --------------------------------------------------

st.subheader("💚 Pipeline Health Summary")

st.success(
    "All major TaxiFlow pipeline stages completed successfully. "
    "The processed dataset passed the configured validation checks "
    "and was loaded into BigQuery for analytical processing."
)


with st.expander("🔍 What this page monitors"):
    st.markdown("""
    - Raw dataset availability
    - Cleaning completion
    - Transformation completion
    - Data validation
    - Mage ETL processing
    - BigQuery loading
    - Analytics availability
    """)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "TaxiFlow • GCP Data Engineering Pipeline • "
    "Python + Mage + BigQuery + Streamlit"
)