#!/usr/bin/env python
# Copyright 2016 Google Inc. All Rights Reserved.
__author__ = "Vijay Anand RP"
__status__ = "Development"

from google.cloud import bigquery
from google.cloud.bigquery.job import DestinationFormat, ExtractJobConfig, Compression
from lib.logger import Logger
from etc.config import project_name

log = Logger().defaults(name_class='BIG QUERY API')

bigquery_client = bigquery.Client(project=project_name)


def list_projects():
    all_projects = list()
    for project in bigquery_client.list_projects():
        all_projects.append(project.project_id)
    log.info(' List of projects are {}'.format(', '.join(all_projects)))
    return all_projects


def list_datasets(project=None):
    """
    Lists all datasets in a given project.
    If no project is specified, then the currently active project is used.
    """
    all_datasets = list()
    for dataset in bigquery_client.list_datasets():
        all_datasets.append(dataset.dataset_id)
    log.info(' List of datasets in {} are {}'.format(project, ', '.join(all_datasets)))
    return all_datasets


def list_tables(dataset_id):
    """
    Lists all of the tables in a given dataset.
    If no project is specified, then the currently active project is used.
    """
    dataset_ref = bigquery_client.dataset(dataset_id)
    all_tables = list()
    for table in bigquery_client.list_tables(dataset_ref):
        all_tables.append(table.table_id)
    log.info(' List of tables in {} are {}'.format(dataset_id, ', '.join(all_tables)))
    return all_tables


def list_rows(dataset_id, table_id, project=None):
    """
    Prints rows in the given table.
    Will print 25 rows at most for brevity as tables can contain large amounts
    of rows.
    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Get the table from the API so that the schema is available.
    table = bigquery_client.get_table(table_ref)

    # Load at most 25 results.
    rows = bigquery_client.list_rows(table, max_results=25)

    # Use format to create a simple table.
    format_string = '{!s:<16} ' * len(table.schema)

    # Print schema field names
    field_names = [field.name for field in table.schema]
    print(format_string.format(*field_names))

    for row in rows:
        print(format_string.format(*row))


def copy_table(dataset_id, table_id, new_table_id, project=None):
    """
    Copies a table.If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # This sample shows the destination table in the same dataset and project,
    # however, it's possible to copy across datasets and projects. You can
    # also copy multiple source tables into a single destination table by
    # providing addtional arguments to `copy_table`.
    destination_table_ref = dataset_ref.table(new_table_id)

    # Create a job to copy the table to the destination table.
    # Start by creating a job configuration
    job_config = bigquery.CopyJobConfig()

    # Configure the job to create the table if it doesn't exist.
    job_config.create_disposition = (
        bigquery.job.CreateDisposition.CREATE_IF_NEEDED)

    copy_job = bigquery_client.copy_table(
        table_ref, destination_table_ref, job_config=job_config)

    log.info('Waiting for job to finish...')
    copy_job.result()
    log.info('Table {} copied to {}.'.format(table_id, new_table_id))


def export_table_to_gcs(dataset_id, table_id, destination, file_format='.json', compression=True):
    """
    Exports data from BigQuery to an object in Google Cloud Storage.
    For more information, see the README.rst.
    Example invocation:
        $ python export_data_to_gcs.py example_dataset example_table \\
            gs://example-bucket/example-data.csv
    The dataset and table should already exist.
    """
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = ExtractJobConfig()
    if file_format == '.json':
        job_config.destination_format = DestinationFormat.NEWLINE_DELIMITED_JSON
        if compression:
            job_config.compression = Compression.GZIP
    elif file_format == '.avro':
        job_config.destination_format = DestinationFormat.AVRO
    else:
        job_config.destination_format = DestinationFormat.CSV
        if compression:
            job_config.compression = Compression.GZIP

    job = bigquery_client.extract_table(table_ref, destination, job_config=job_config)
    job.result(timeout=500)  # Waits for job to complete
    log.info('Exported {}:{} to {}'.format(dataset_id, table_id, destination))



