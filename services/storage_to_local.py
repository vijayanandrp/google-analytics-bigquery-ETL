#!/usr/bin/env python
__author__ = "Vijay Anand RP"
__status__ = "Development"

import os
import sys
from etc.config import project_name, json_credential, file_format
from lib.logger import Logger

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json_credential

from lib.api.storage import list_bucket, list_blobs, delete_bucket, delete_blob, download_blob

log = Logger(stream_output=True, level='INFO').defaults(name_class='GCS-to-Local')

if __name__ == '__main__':
    buckets_list = list_bucket()
    for bl in buckets_list:
        if 'website-traffic' in bl:
            # try:
            #     delete_bucket(bl)
            # except:
            #     pass
            log.info('*'*10 + bl + '*'*10)
            for bn in list_blobs(bl):
                log.info(bn)
                # delete_blob(bucket_name=bl, blob_name=bn)

    # download_blob(bucket_name='test_todd', source_blob_name='test_allie.csv', destination_file_name='test.csv')


