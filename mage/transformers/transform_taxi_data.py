if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd


@transformer
def transform(data, *args, **kwargs):

    df = data.copy()

    input_count = len(df)

    # Convert datetime columns
    df['tpep_pickup_datetime'] = pd.to_datetime(
        df['tpep_pickup_datetime'],
        errors='coerce'
    )

    df['tpep_dropoff_datetime'] = pd.to_datetime(
        df['tpep_dropoff_datetime'],
        errors='coerce'
    )

    # Remove invalid distances
    df = df[df['trip_distance'] > 0]

    # Remove negative fares
    df = df[df['fare_amount'] >= 0]

    # Handle invalid passenger counts
    df.loc[
        df['passenger_count'] <= 0,
        'passenger_count'
    ] = pd.NA

    # Calculate trip duration
    df['trip_duration_minutes'] = (
        df['tpep_dropoff_datetime']
        - df['tpep_pickup_datetime']
    ).dt.total_seconds() / 60

    # Keep realistic trip durations
    df = df[
        (df['trip_duration_minutes'] > 0) &
        (df['trip_duration_minutes'] <= 300)
    ]

    # Analytics columns
    df['pickup_hour'] = (
        df['tpep_pickup_datetime'].dt.hour
    )

    df['dropoff_hour'] = (
        df['tpep_dropoff_datetime'].dt.hour
    )

    df['day_of_week'] = (
        df['tpep_pickup_datetime'].dt.day_name()
    )

    df['is_weekend'] = (
        df['tpep_pickup_datetime'].dt.dayofweek >= 5
    )

    df['pickup_date'] = (
        df['tpep_pickup_datetime']
        .dt.date
        .astype(str)
    )

    # Revenue efficiency
    df['revenue_per_mile'] = (
        df['total_amount'] /
        df['trip_distance']
    )

    output_count = len(df)

    print(f"Input records: {input_count:,}")
    print(f"Output records: {output_count:,}")
    print(
        f"Removed records: "
        f"{input_count - output_count:,}"
    )
    print(f"Columns: {len(df.columns)}")

    return df


@test
def test_output(output, *args) -> None:
    assert output is not None
    assert len(output) > 0