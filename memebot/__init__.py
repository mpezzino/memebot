from boto.s3.connection import Location

from memebot import utils, memebot_config


def init_s3_connection():
    access, secret = memebot_config.get_aws_credentials()
    return S3Connection(access, secret)