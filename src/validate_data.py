import pandas as pd
from pathlib import Path


FILE_PATH = Path("data/processed/cleaned_trips.parquet")


def main():

    print("=" * 60)
    print("TAXIFLOW DATA VALIDATION")
    print("=" * 60)

    df = pd.read_parquet(FILE_PATH)

    print(f"\nTotal records: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")

    print("\n--- Columns ---")
    for column in df.columns:
        print(f"  ✓ {column}")

    print("\n--- Missing Values ---")

    missing = df.isnull().sum()

    for column, count in missing.items():

        if count > 0:
            percentage = (count / len(df)) * 100

            print(
                f"  {column}: "
                f"{count:,} "
                f"({percentage:.2f}%)"
            )

    print("\n--- Data Quality Checks ---")

    print(
        "Negative trip distances:",
        (df["trip_distance"] < 0).sum()
    )

    print(
        "Zero trip distances:",
        (df["trip_distance"] <= 0).sum()
    )

    print(
        "Negative fares:",
        (df["fare_amount"] < 0).sum()
    )

    print(
        "Invalid trip durations:",
        (
            (df["trip_duration_minutes"] <= 0)
            |
            (df["trip_duration_minutes"] > 300)
        ).sum()
    )

    print("\n--- Date Range ---")

    print(
        "Earliest pickup:",
        df["tpep_pickup_datetime"].min()
    )

    print(
        "Latest pickup:",
        df["tpep_pickup_datetime"].max()
    )

    print("\n--- Basic Statistics ---")

    print(
        f"Average trip distance: "
        f"{df['trip_distance'].mean():.2f}"
    )

    print(
        f"Average trip duration: "
        f"{df['trip_duration_minutes'].mean():.2f} minutes"
    )

    print(
        f"Average total amount: "
        f"${df['total_amount'].mean():.2f}"
    )

    print("\n--- Validation Status ---")

    problems = 0

    if (df["trip_distance"] <= 0).any():
        problems += 1

    if (df["fare_amount"] < 0).any():
        problems += 1

    if (
        (df["trip_duration_minutes"] <= 0)
        |
        (df["trip_duration_minutes"] > 300)
    ).any():
        problems += 1

    if problems == 0:
        print("✓ ALL CRITICAL VALIDATION CHECKS PASSED")
    else:
        print(
            f"⚠ {problems} validation issue(s) found"
        )

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()