from os.path import expanduser

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

def get_aws_credentials():
    return get_credentials_property("access.key"), get_credentials_property("secret.key")



