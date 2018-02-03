#!/usr/bin/env python
__author__ = "Vijay Anand RP"
__status__ = "Development"

import os
import sys
import fnmatch
from etc.config import project_name, json_credential, file_format
from lib.logger import Logger

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json_credential

from lib.api.bigquery import list_projects, list_datasets, list_tables, export_table_to_gcs
from lib.api.storage import create_bucket, list_bucket, list_blobs

log = Logger(stream_output=True, level='INFO').defaults(name_class='BigQuery-to-GCS')

if __name__ == '__main__':
    log.info('****' * 9)
    log.info('*** BIG QUERY TO CLOUD STORAGE ***')
    log.info('*** Process Started ***')
    log.info('****' * 9)

    # 1. List all projects
    all_projects = list_projects()

    # 2. Check for project name
    if project_name not in all_projects:
        log.error('Oops this is written to do software-advice jobs not other projects.')
        sys.exit(-1)

    log.info('The project name is {}'.format(project_name))

    # 2. Get all datasets from big query
    all_datasets = list_datasets(project=project_name)

    if not all_datasets:
        log.error('No datasets in this project.')
        sys.exit(-1)

    log.info('There are {} datasets so far.'.format(len(all_datasets)))
    log.info('Following are the datasets in software advice,')

    buckets_list = list_bucket()
    # 3. Remove Adwords as its  not useful
    if 'Adwords' in all_datasets:
        all_datasets.remove('Adwords')

    # 4. all datasets from big query and creating the bucket name in cloud storage
    for index, dataset in enumerate(all_datasets):
        log.info('{} - {}'.format(index + 1, dataset))
        new_bucket_name = '{}-{}'.format(project_name, dataset)

        if new_bucket_name not in buckets_list:
            log.info('Also, Creating bucket-name as {}'.format(new_bucket_name))
            create_bucket(bucket_name=new_bucket_name)

    # 5. get all new buckets
    buckets_list = list_bucket()
    buckets_list.sort()

    log.info('New bucket list - {}'.format(', '.join(buckets_list)))
    log.info('Ok. Lets see what is inside each datasets :)')

    # 6. get all files list in bucket if anything is missing it will exported
    for index, dataset in enumerate(all_datasets):
        gcs_bucket_name = '{}-{}'.format(project_name, dataset)
        all_tables = list_tables(dataset_id=dataset)

        log.info('[[{}]] {} - ({}) - {}'.format(index + 1, dataset, len(all_tables), all_tables))
        blobs_list = list_blobs(bucket_name=gcs_bucket_name)
        log.info('List of tables already in bucket - {}'.format(blobs_list))
        for num, table in enumerate(all_tables):
            num = num + 1
            if table + file_format not in blobs_list:
                log.info('{} - Moving {} - {} to gs://{}/{}{}'.format(num, dataset, table, gcs_bucket_name,
                                                                      table, file_format))

                try:
                    destination_file = 'gs://{}/{}{}'.format(gcs_bucket_name, table, file_format)
                    export_table_to_gcs(dataset_id=dataset, table_id=table, destination=destination_file,
                                        file_format=file_format)
                except Exception as error:
                    log.exception('Exception while exporting from big query to GCS')

                    pattern = '{}*{}'.format(table, file_format)
                    matching = fnmatch.filter(blobs_list, pattern)
                    log.info('Matching wild card files - {}'.format(matching))
                    if len(matching) < 4:
                        destination_file = 'gs://{}/{}*{}'.format(gcs_bucket_name, table, file_format)
                        log.info('{} - Moving {} - {} to (wild card URIs) gs://{}/{}*{}'.format(num, dataset, table,
                                                                                                gcs_bucket_name,
                                                                                                table, file_format))
                        export_table_to_gcs(dataset_id=dataset, table_id=table, destination=destination_file,
                                            file_format=file_format)
                    else:
                        log.info('{} - Skipping {} - {} to (wild card URIs) gs://{}/{}*{}'.format(num, dataset, table,
                                                                                                  gcs_bucket_name,
                                                                                                  table, file_format))

            else:
                log.info('{} - Skipping {} - {} to gs://{}/{}{}'.format(num, dataset, table, gcs_bucket_name,
                                                                        table, file_format))

