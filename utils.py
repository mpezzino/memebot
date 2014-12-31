__author__ = 'jonathan'

from memebot_config import *
import os

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

ensure_dir(CORPUS_PATH)
