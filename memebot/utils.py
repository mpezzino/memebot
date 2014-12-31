__author__ = 'jonathan'

import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from memebot_config import *


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

ensure_dir(CORPUS_PATH)

def init_s3_connection():
    access, secret = get_aws_credentials()
    return S3Connection(access, secret)

S3_CONNECTION=init_s3_connection()

def get_s3_connection():
    return S3_CONNECTION;

def write_to_s3( obj_name, content ):
    s3 = get_s3_connection()
    bucket_name = obj_name.split("/")[0]
    obj_bucket_path = obj_name.replace( bucket_name+"/","")
    bucket = s3.get_bucket(bucket_name)
    k = Key( bucket )
    k.key = obj_bucket_path
    k.set_contents_from_string(content)


