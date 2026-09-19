if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

from google.cloud import bigquery


@data_exporter
def export_data(df, *args, **kwargs):

    project_id = "taxiflow-analytics"
    dataset_id = "taxiflow"
    table_id = "mage_taxi_trips"

    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    print(f"Exporting {len(df):,} records to {table_ref}")

    # Create BigQuery client
    client = bigquery.Client(project=project_id)

    # Configure load job
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True
    )

    # Convert date column for BigQuery compatibility
    if "pickup_date" in df.columns:
        df["pickup_date"] = df["pickup_date"].astype(str)

    # Upload DataFrame to BigQuery
    job = client.load_table_from_dataframe(
        df,
        table_ref,
        job_config=job_config
    )

    # Wait for upload to finish
    job.result()

    print(f"Successfully exported {len(df):,} records")
    print(f"BigQuery table: {table_ref}")