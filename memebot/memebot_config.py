from os.path import expanduser
import utils
from boto.s3.connection import Location, S3Connection

CREDENTIALS_FILE= expanduser("~") + "/memebot_credentials.properties"

def get_credentials_property(prop):
    f = open( CREDENTIALS_FILE )
    for line in f.readlines():
        if line.startswith(prop):
            f.close()
            return line.replace(prop+"=","").lstrip().rstrip()
    f.close()
    raise Exception( "Error: credentials property not found: " + prop + ". Add to " + CREDENTIALS_FILE + " or run setup.py")

def get_bot_login_password():
    return get_credentials_property("bot.password")

BOT_LOGIN_PASSWORD=get_bot_login_password()
BOT_USERNAME = get_credentials_property("bot.username")

CORPUS_PATH= "/var/lib/memebot"
S3_CORPUS_BUCKET=get_credentials_property("s3_corpus_bucket")

CLASSIFIER_FILE_PATH=CORPUS_PATH+"/memebot_classifier.pkl"


def get_aws_credentials():
    return get_credentials_property("access.key"), get_credentials_property("secret.key")

def creds_prop(key,val):
    return key + "=" + val + "\n";

def setup_s3_buckets():
    s3 = utils.get_s3_connection()
    s3.create_bucket(S3_CORPUS_BUCKET,location=Location.USWest2)

def setup_credentials_file():
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

if __name__ == "__main__":
    setup_credentials_file()


def init_s3_connection():
    access, secret = get_aws_credentials()
    return S3Connection(access, secret)

S3_CONNECTION=init_s3_connection()