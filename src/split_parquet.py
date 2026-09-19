import pandas as pd
from pathlib import Path


INPUT_FILE = Path("data/processed/cleaned_trips.parquet")
OUTPUT_DIR = Path("data/processed/parts")

ROWS_PER_FILE = 100_000


def main():

    print("=" * 60)
    print("TAXIFLOW PARQUET SPLITTER")
    print("=" * 60)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print(f"\nReading: {INPUT_FILE}")
    print(f"Splitting into files of {ROWS_PER_FILE:,} rows...\n")

    df = pd.read_parquet(INPUT_FILE)

    total_rows = len(df)

    print(f"Total rows: {total_rows:,}")

    file_number = 1

    for start in range(0, total_rows, ROWS_PER_FILE):

        end = min(
            start + ROWS_PER_FILE,
            total_rows
        )

        part = df.iloc[start:end]

        output_file = (
            OUTPUT_DIR /
            f"taxi_trips_part_{file_number:03d}.parquet"
        )

        part.to_parquet(
            output_file,
            index=False
        )

        size_mb = output_file.stat().st_size / (1024 * 1024)

        print(
            f"Created {output_file.name} | "
            f"{len(part):,} rows | "
            f"{size_mb:.2f} MB"
        )

        file_number += 1

    print("\n" + "=" * 60)
    print("SPLITTING COMPLETE")
    print("=" * 60)

    print(f"Files created: {file_number - 1}")
    print(f"Output folder: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()