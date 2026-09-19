import os
import pandas as pd


FILE_PATH = "data/raw/bengaluru_uber_trips.csv"
CHUNK_SIZE = 100_000


def profile_dataset(file_path):
    print("=" * 70)
    print("              TAXIFLOW INDIA - DATA PROFILE")
    print("=" * 70)

    file_size = os.path.getsize(file_path)

    print(f"\nFile: {file_path}")
    print(f"File size: {file_size / (1024 ** 2):.2f} MB")

    # ---------------------------------------------------------
    # Read a small sample to identify columns
    # ---------------------------------------------------------

    sample = pd.read_csv(file_path, nrows=5)

    print(f"\nNumber of columns: {len(sample.columns)}")

    print("\nColumns:")
    for column in sample.columns:
        print(f"  - {column}")

    # ---------------------------------------------------------
    # Initialize statistics
    # ---------------------------------------------------------

    total_rows = 0
    missing_values = pd.Series(dtype="int64")

    min_pickup = None
    max_pickup = None

    negative_distance = 0
    negative_fare = 0
    zero_distance = 0

    # ---------------------------------------------------------
    # Process CSV in chunks
    # ---------------------------------------------------------

    print("\nProcessing dataset in chunks...")

    for chunk_number, chunk in enumerate(
        pd.read_csv(file_path, chunksize=CHUNK_SIZE),
        start=1
    ):
        total_rows += len(chunk)

        print(
            f"\rProcessed approximately "
            f"{total_rows:,} records...",
            end=""
        )

        # Missing values
        chunk_missing = chunk.isna().sum()

        if missing_values.empty:
            missing_values = chunk_missing
        else:
            missing_values = missing_values.add(
                chunk_missing,
                fill_value=0
            )

        # -----------------------------------------------------
        # Detect distance column
        # -----------------------------------------------------

        distance_columns = [
            col for col in chunk.columns
            if "distance" in col.lower()
        ]

        if distance_columns:
            distance_col = distance_columns[0]

            negative_distance += (
                chunk[distance_col] < 0
            ).sum()

            zero_distance += (
                chunk[distance_col] == 0
            ).sum()

        # -----------------------------------------------------
        # Detect fare column
        # -----------------------------------------------------

        fare_columns = [
            col for col in chunk.columns
            if "fare" in col.lower()
        ]

        if fare_columns:
            fare_col = fare_columns[0]

            negative_fare += (
                chunk[fare_col] < 0
            ).sum()

        # -----------------------------------------------------
        # Detect pickup datetime column
        # -----------------------------------------------------

        datetime_columns = [
            col for col in chunk.columns
            if "pickup" in col.lower()
            and (
                "time" in col.lower()
                or "date" in col.lower()
            )
        ]

        if datetime_columns:
            pickup_col = datetime_columns[0]

            dates = pd.to_datetime(
                chunk[pickup_col],
                errors="coerce"
            )

            chunk_min = dates.min()
            chunk_max = dates.max()

            if pd.notna(chunk_min):
                if min_pickup is None or chunk_min < min_pickup:
                    min_pickup = chunk_min

            if pd.notna(chunk_max):
                if max_pickup is None or chunk_max > max_pickup:
                    max_pickup = chunk_max

    print("\n")

    # ---------------------------------------------------------
    # Final report
    # ---------------------------------------------------------

    print("-" * 70)
    print("DATASET SUMMARY")
    print("-" * 70)

    print(f"Total records:       {total_rows:,}")
    print(f"Total columns:       {len(sample.columns)}")
    print(f"File size:           {file_size / (1024 ** 2):.2f} MB")

    print("\n" + "-" * 70)
    print("MISSING VALUES")
    print("-" * 70)

    for column, count in missing_values.items():
        percentage = (count / total_rows) * 100

        print(
            f"{column:<30} "
            f"{int(count):>10,} "
            f"({percentage:.2f}%)"
        )

    print("\n" + "-" * 70)
    print("DATA QUALITY")
    print("-" * 70)

    print(f"Negative distances: {negative_distance:,}")
    print(f"Zero distances:     {zero_distance:,}")
    print(f"Negative fares:     {negative_fare:,}")

    print("\n" + "-" * 70)
    print("DATE RANGE")
    print("-" * 70)

    print(f"Earliest pickup:    {min_pickup}")
    print(f"Latest pickup:      {max_pickup}")

    print("\n" + "=" * 70)
    print("                 PROFILE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    profile_dataset(FILE_PATH)