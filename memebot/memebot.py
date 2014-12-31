__author__ = 'jonathan'

import re

import praw

import memebot_config
import utils


BUCKET_THRESHOLDS=[-10,   \
                   -9,   \
                   -1,   \
                    1,   \
                    2,   \
                    11,  \
                    51,  \
                    101, \
                    251, \
                    501, \
                    1001
    ];
BUCKET_THRESHOLDS.sort();


bot = praw.Reddit( 'memebot by /u/mr_jim_lahey' );
bot.login(username=memebot_config.BOT_USERNAME, password=memebot_config.BOT_LOGIN_PASSWORD);

def get_bucket_path( karma, corpus_root=memebot_config.CORPUS_PATH ):
    if karma <= BUCKET_THRESHOLDS[0]:
        return get_thresholds_path( BUCKET_THRESHOLDS[0], None, corpus_root=corpus_root );

    for i in range( 1, len( BUCKET_THRESHOLDS ) - 2):
        threshold_lower = BUCKET_THRESHOLDS[i];
        threshold_upper = BUCKET_THRESHOLDS[i+1];
        if karma >= threshold_lower and karma < threshold_upper:
            return get_thresholds_path(threshold_lower, threshold_upper, corpus_root=corpus_root)

    return get_thresholds_path( None, BUCKET_THRESHOLDS[-1], corpus_root=corpus_root );

def get_thresholds_path( threshold_value_lower, threshold_value_upper, corpus_root=memebot_config.CORPUS_PATH ):
    bucket_path = corpus_root + "/";

    if threshold_value_lower is not None:
        bucket_path +=  str( threshold_value_lower ).replace( "-", "_neg_");

    if threshold_value_lower is threshold_value_upper:
        return bucket_path;
    elif threshold_value_lower is not None:
        bucket_path += "-"

    if threshold_value_upper is not None:
        bucket_path += str( threshold_value_upper - 1 ).replace( "-", "_neg_")

    if threshold_value_lower is None:
        bucket_path += "+"

    return bucket_path;

def write_comment_to_corpus_s3( flattened_comment ):
    write_comment_to_corpus(flattened_comment, corpus_root=memebot_config.S3_CORPUS_BUCKET, write_method=write_to_corpus_s3);

def write_to_corpus_local( fname, comment_text):
    utils.ensure_dir(fname)
    f = open(fname, 'w')
    f.write( comment_text )
    f.close();

def write_to_corpus_s3( fname, comment_text ):
    utils.write_to_s3(fname, comment_text)


def write_comment_to_corpus( flattened_comment, corpus_root=memebot_config.CORPUS_PATH, write_method=write_to_corpus_local ):
    cdir = get_bucket_path( flattened_comment.ups - flattened_comment.downs, corpus_root=corpus_root );
    fname = cdir + "/" + comment.id;

    comment_text = comment.body.encode('ascii', 'ignore');
    comment_text = re.sub("&gt;.*?(\n|$)", "", comment_text) # remove quoted content
    comment_text = comment_text.replace("\n"," ")
    if len(comment_text) > 0:
        write_method(fname, comment_text)



if __name__ == '__main__':
    news_subreddit = bot.get_subreddit('news');
    for submission in news_subreddit.get_hot(limit=3):
        if len(submission.comments) > 0:
            for comment in praw.helpers.flatten_tree(submission.comments):
                #pprint( vars(comment) )
                if not isinstance(comment, praw.objects.MoreComments):
                    karma = comment.ups - comment.downs;
                    print comment.body.replace( "\n", " ")
                    print '\t' + str(karma)
                    print '\t' + get_bucket_path(karma, corpus_root=memebot_config.S3_CORPUS_BUCKET) + "\n"
                    write_comment_to_corpus_s3( comment )