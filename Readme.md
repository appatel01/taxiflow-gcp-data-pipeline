# 🚕 TaxiFlow — GCP Taxi Data Engineering Pipeline
[![TaxiFlow CI](https://github.com/appatel01/taxiflow-gcp-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/appatel01/taxiflow-gcp-data-pipeline/actions/workflows/ci.yml)
A production-style data engineering project that processes and analyzes **6.39 million taxi trip records** using Python, Apache Parquet, Mage, and Google BigQuery.

The project demonstrates an end-to-end ETL workflow covering data ingestion, cleaning, transformation, orchestration, cloud warehousing, data validation, and analytics.

---

## 🏗️ Architecture

TaxiFlow follows an end-to-end data engineering workflow:

```text
Raw Taxi Data
      │
      ▼
Python Data Processing
      │
      ├── Cleaning
      ├── Validation
      └── Feature Engineering
      │
      ▼
Mage Pipeline
      │
      ├── Load
      ├── Transform
      └── Export
      │
      ▼
Google BigQuery
      │
      ├── Cleaned Data
      ├── Analytical Views
      └── SQL Analytics
      │
      ▼
Insights & Visualization

## 📊 Project Results

| Metric | Result |
|---|---:|
| Raw records processed | 6,500,000 |
| Clean records | 6,390,635 |
| Records removed | 109,365 |
| Final columns | 23 |
| Average trip distance | 4.78 |
| Average trip duration | 13.19 min |
| Invalid distances after cleaning | 0 |
| Negative fares after cleaning | 0 |
| Invalid durations after cleaning | 0 |


### Data Quality

The pipeline performs validation checks after transformation to ensure that:

- Trip distances are positive
- Fare amounts are non-negative
- Trip durations are realistic
- Datetime fields are valid
- Invalid passenger counts are handled
- Analytical features are generated consistently


### 3. Save and push

Run:

```powershell
git add docs/taxiflow-architecture.png README.md

## 🚀 Project Overview

TaxiFlow transforms a large taxi trip dataset into an analytics-ready BigQuery data warehouse.

### Pipeline

Raw Taxi Data
      ↓
Python Data Cleaning
      ↓
Apache Parquet
      ↓
Mage ETL Pipeline
      ↓
BigQuery
      ↓
Analytics Views
      ↓
Insights & Dashboards

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Data processing and cleaning |
| Pandas | Data transformation |
| PyArrow | Parquet processing |
| Apache Parquet | Columnar data storage |
| Mage | ETL pipeline orchestration |
| Google BigQuery | Cloud data warehouse |
| Google Cloud | Cloud infrastructure |
| SQL | Analytics and validation |
| Git & GitHub | Version control |

---

## 📊 Dataset

The project processes a large taxi-trip dataset containing:

- **6,500,000 raw records**
- **16 original columns**
- **6,390,635 cleaned records**
- **23 analytics-ready columns**

The dataset contains taxi-trip fields such as:

- Pickup and dropoff timestamps
- Passenger count
- Trip distance
- Pickup and dropoff location IDs
- Fare amount
- Tip amount
- Tolls
- Total amount
- Payment information

> Note: The source dataset's original third-party description and its observed schema/date range are not fully consistent. Therefore, this project refers to it generically as a **taxi-trip benchmark dataset** rather than making an unsupported claim that it represents Bengaluru/Uber trips.

---

## 🧹 Data Cleaning

The Python preprocessing pipeline performs:

- Datetime conversion
- Invalid distance removal
- Negative fare removal
- Invalid passenger-count handling
- Trip-duration calculation
- Unrealistic trip-duration filtering
- Pickup-hour extraction
- Dropoff-hour extraction
- Day-of-week extraction
- Weekend identification
- Pickup-date generation
- Revenue-per-mile calculation

### Cleaning Results

| Metric | Result |
|--------|--------:|
| Raw records | 6,500,000 |
| Clean records | 6,390,635 |
| Removed records | 109,365 |
| Final columns | 23 |

---

## 🔍 Data Quality

The cleaned dataset was validated before loading into BigQuery.

Validation checks include:

- Negative trip distances
- Zero trip distances
- Negative fares
- Invalid trip durations
- Missing values
- Date-range validation
- Record-count validation

### Final validation

```text
Total records:       6,390,635
Negative distance:   0
Zero distance:       0
Negative fares:      0
Invalid duration:    0