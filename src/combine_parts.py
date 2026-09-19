import pandas as pd
from pathlib import Path


INPUT_DIR = Path("data/processed/parts")
OUTPUT_DIR = Path("data/processed/upload_batches")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def combine_parts(start_part, end_part, output_name):

    output_file = OUTPUT_DIR / output_name

    print("\n" + "=" * 60)
    print(f"Creating {output_name}")
    print(f"Parts {start_part:03d} → {end_part:03d}")
    print("=" * 60)

    first = True
    total_rows = 0

    for part_number in range(start_part, end_part + 1):

        input_file = (
            INPUT_DIR /
            f"taxi_trips_part_{part_number:03d}.parquet"
        )

        df = pd.read_parquet(input_file)

        total_rows += len(df)

        if first:
            df.to_parquet(
                output_file,
                index=False
            )
            first = False
        else:
            existing = pd.read_parquet(output_file)

            combined = pd.concat(
                [existing, df],
                ignore_index=True
            )

            combined.to_parquet(
                output_file,
                index=False
            )

        print(
            f"Part {part_number:03d} | "
            f"{len(df):,} rows | "
            f"Total: {total_rows:,}"
        )

    size_mb = output_file.stat().st_size / (1024 * 1024)

    print(
        f"\nCreated: {output_file}"
    )
    print(f"Rows: {total_rows:,}")
    print(f"Size: {size_mb:.2f} MB")


def main():

    # Parts 003-032 = 3,000,000 rows
    combine_parts(
        3,
        32,
        "taxi_trips_batch_01.parquet"
    )

    # Parts 033-064 = 3,190,635 rows
    combine_parts(
        33,
        64,
        "taxi_trips_batch_02.parquet"
    )

    print("\n" + "=" * 60)
    print("ALL BATCHES CREATED")
    print("=" * 60)


if __name__ == "__main__":
    main()