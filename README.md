# 🚕 TaxiFlow — GCP Taxi Data Engineering Pipeline

<p align="center">
  <b>End-to-End Data Engineering & Analytics Pipeline</b>
</p>

<p align="center">
  Python • Pandas • PyArrow • Mage • Google BigQuery • SQL • Streamlit • GitHub Actions
</p>

<p align="center">

[![TaxiFlow CI](https://github.com/appatel01/taxiflow-gcp-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/appatel01/taxiflow-gcp-data-pipeline/actions/workflows/ci.yml)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/appatel01/taxiflow-gcp-data-pipeline)
[![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://taxiflow-gcp-data-pipeline-doj33o6qqhy9xmwtgrmoak.streamlit.app/)

</p>

---

## 🚕 Live Dashboard

Explore the deployed TaxiFlow analytics platform:

### 👉 [Open TaxiFlow Dashboard](https://taxiflow-gcp-data-pipeline-doj33o6qqhy9xmwtgrmoak.streamlit.app/)

The dashboard includes:

- 📊 Interactive taxi-trip KPIs
- 🧠 Demand Intelligence
- 🚨 Anomaly Detection
- 🔮 Demand Forecasting
- 🧹 Data Quality Monitoring
- ⚙️ Pipeline Health Monitoring
- 📈 Hourly and daily demand analysis
- 📍 Pickup-location analysis
- 📉 Interactive analytics visualizations

---

# 📌 Overview

**TaxiFlow** is an end-to-end data engineering and analytics project that processes and analyzes **6.5 million taxi-trip records** using Python, Apache Parquet, Mage, Google BigQuery, SQL, and Streamlit.

The project demonstrates a complete data engineering workflow covering:

- Data ingestion
- Data cleaning
- Data validation
- Feature engineering
- ETL orchestration
- Cloud data warehousing
- Analytical SQL
- Automated testing
- Interactive visualization

The final pipeline transforms raw taxi-trip data into a validated, analytics-ready dataset and exposes the results through an interactive Streamlit dashboard.

---

# 🏗️ Architecture

TaxiFlow follows this end-to-end architecture:

```text
                         ┌─────────────────────┐
                         │   Raw Taxi Dataset  │
                         │    6.5M Records     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Python Processing │
                         │                     │
                         │ • Cleaning          │
                         │ • Validation        │
                         │ • Feature Engineering│
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Apache Parquet    │
                         │   Columnar Storage  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Mage Pipeline    │
                         │                     │
                         │ • Load              │
                         │ • Transform         │
                         │ • Export            │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Google BigQuery   │
                         │                     │
                         │ • Cleaned Data      │
                         │ • Analytical Views  │
                         │ • SQL Analytics     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Streamlit Dashboard│
                         │                     │
                         │ • KPIs              │
                         │ • Demand Analysis   │
                         │ • Anomalies         │
                         │ • Forecasting       │
                         │ • Data Quality      │
                         │ • Pipeline Health   │
                         └─────────────────────┘