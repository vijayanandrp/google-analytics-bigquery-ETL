# -*- coding:utf-8 -*-
__author__ = "Vijay Anand RP"
__status__ = "Development"

from google.cloud import storage
from lib.logger import Logger


log = Logger().defaults(name_class='STORAGE API')


def create_bucket(bucket_name):
    """Creates a new bucket."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    log.info('Bucket {} created'.format(bucket.name))


def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()
    log.info('Bucket {} deleted'.format(bucket.name))


def list_bucket():
    """Creates a new bucket."""
    log.info('Fetching all bucket names in GCS.')
    storage_client = storage.Client()
    buckets_list = list()
    for bucket in storage_client.list_buckets():
        buckets_list.append(bucket.name)
        # log.info(bucket.name)
    return buckets_list


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    blobs_list = list()
    for blob in blobs:
        blobs_list.append(blob.name)
        # log.info(blob.name)
    return blobs_list


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    log.info('Blob {} downloaded to {}.'.format(source_blob_name, destination_file_name))


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    log.info('Blob {} deleted.'.format(blob_name))


