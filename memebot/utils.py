__author__ = 'jonathan'

import os
import simplejson
from boto.s3.key import Key

import memebot_config


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def get_s3_connection():
    return memebot_config.S3_CONNECTION;

def write_to_s3( obj_name, content ):
    s3 = get_s3_connection()
    bucket_name = obj_name.split("/")[0]
    obj_bucket_path = obj_name.replace( bucket_name+"/","")
    bucket = s3.get_bucket(bucket_name)
    k = Key( bucket )
    k.key = obj_bucket_path
    k.set_contents_from_string(content)


def jsonp(func):
    def foo(self, *args, **kwargs):
        callback, _ = None, None
        if 'callback' in kwargs and '_' in kwargs:
            callback, _ = kwargs['callback'], kwargs['_']
            del kwargs['callback'], kwargs['_']
        ret = func(self, *args, **kwargs)
        if callback is not None:
            ret = '%s(%s)' % (callback, simplejson.dumps(ret))
        return ret
    return foo


