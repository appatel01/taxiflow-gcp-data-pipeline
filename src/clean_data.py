import pandas as pd
from pathlib import Path


INPUT_FILE = Path("data/raw/bengaluru_uber_trips.csv")
OUTPUT_FILE = Path("data/processed/cleaned_trips.parquet")

CHUNK_SIZE = 100_000


def clean_chunk(df):
    # -----------------------------
    # Convert datetime columns
    # -----------------------------
    df["tpep_pickup_datetime"] = pd.to_datetime(
        df["tpep_pickup_datetime"],
        errors="coerce"
    )

    df["tpep_dropoff_datetime"] = pd.to_datetime(
        df["tpep_dropoff_datetime"],
        errors="coerce"
    )

    # -----------------------------
    # Remove invalid distances
    # -----------------------------
    df = df[
        (df["trip_distance"] > 0)
    ]

    # -----------------------------
    # Remove invalid fares
    # -----------------------------
    df = df[
        (df["fare_amount"] >= 0)
    ]

    # -----------------------------
    # Remove impossible passenger counts
    # -----------------------------
    df.loc[
        (df["passenger_count"] <= 0),
        "passenger_count"
    ] = pd.NA

    # -----------------------------
    # Calculate trip duration
    # -----------------------------
    df["trip_duration_minutes"] = (
        df["tpep_dropoff_datetime"]
        - df["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60

    # Keep reasonable trip durations
    df = df[
        (df["trip_duration_minutes"] > 0)
        & (df["trip_duration_minutes"] <= 300)
    ]

    # -----------------------------
    # Feature engineering
    # -----------------------------
    df["pickup_hour"] = (
        df["tpep_pickup_datetime"].dt.hour
    )

    df["dropoff_hour"] = (
        df["tpep_dropoff_datetime"].dt.hour
    )

    df["day_of_week"] = (
        df["tpep_pickup_datetime"].dt.day_name()
    )

    df["is_weekend"] = (
        df["tpep_pickup_datetime"]
        .dt.dayofweek >= 5
    )

    df["pickup_date"] = (
        df["tpep_pickup_datetime"].dt.date
    )

    # -----------------------------
    # Revenue metrics
    # -----------------------------
    df["revenue_per_mile"] = (
        df["total_amount"] /
        df["trip_distance"].replace(0, pd.NA)
    )

    return df


def main():

    print("=" * 60)
    print("TAXIFLOW DATA CLEANING PIPELINE")
    print("=" * 60)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    first_chunk = True
    total_input = 0
    total_output = 0

    for chunk in pd.read_csv(
        INPUT_FILE,
        chunksize=CHUNK_SIZE
    ):

        total_input += len(chunk)

        cleaned = clean_chunk(chunk)

        total_output += len(cleaned)

        if first_chunk:
            cleaned.to_parquet(
                OUTPUT_FILE,
                index=False
            )
            first_chunk = False

        else:
            existing = pd.read_parquet(
                OUTPUT_FILE
            )

            combined = pd.concat(
                [existing, cleaned],
                ignore_index=True
            )

            combined.to_parquet(
                OUTPUT_FILE,
                index=False
            )

        print(
            f"Processed: {total_input:,} | "
            f"Cleaned: {total_output:,}"
        )

    print("\n" + "=" * 60)
    print("CLEANING COMPLETE")
    print("=" * 60)

    print(f"Input records : {total_input:,}")
    print(f"Output records: {total_output:,}")

    removed = total_input - total_output

    print(f"Removed       : {removed:,}")

    print(f"\nOutput file:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()