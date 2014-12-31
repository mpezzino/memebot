__author__ = 'jonathan'

import memebot_config
import utils
import sys
from boto.s3.connection import Location

def creds_prop(key,val):
    return key + "=" + val + "\n";

def setup_s3_buckets():
    s3 = utils.get_s3_connection()
    s3.create_bucket(memebot_config.S3_CORPUS_BUCKET,location=Location.USWest2)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 's3':
        setup_s3_buckets();
        exit()
    else:
        print sys.argv[1]

    bot_username = raw_input("Bot username: /u/")
    bot_pw = raw_input("Bot password: ")
    access_key = raw_input("AWS Access Key: ")
    secret_key = raw_input("AWS Secret Key: ")
    s3_corpus_bucket = raw_input( "S3 Corpus Bucket: ")

    credentials_file_text = \
    creds_prop("bot.username", bot_username) \
    + creds_prop("bot.password", bot_pw) \
    + creds_prop("access.key", access_key) \
    + creds_prop("secret.key", secret_key) \
    + creds_prop("s3_corpus_bucket", s3_corpus_bucket);

    utils.ensure_dir(utils.CREDENTIALS_FILE)
    f = open( utils.CREDENTIALS_FILE, 'w' )
    f.write(credentials_file_text)
    f.close()


    setup_s3_buckets()



