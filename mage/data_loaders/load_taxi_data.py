if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from pathlib import Path
import pyarrow.parquet as pq


@data_loader
def load_data(*args, **kwargs):

    file_path = Path(
        "data/processed/cleaned_trips.parquet"
    ).resolve()

    print(f"Reading file: {file_path}")

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {file_path}"
        )

    parquet_file = pq.ParquetFile(file_path)

    # Current test batch
    batch = next(
        parquet_file.iter_batches(
            batch_size=100_000
        )
    )

    df = batch.to_pandas()

    print(f"Loaded {len(df):,} records")
    print(f"Columns: {len(df.columns)}")

    return df


@test
def test_output(output, *args) -> None:
    assert output is not None
    assert len(output) > 0