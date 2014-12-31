__author__ = 'jonathan'

from pprint import pprint
from memebot_config import *
import praw
import utils
import re



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
bot.login(username="the_memebot", password=BOT_LOGIN_PASSWORD);

def get_bucket_path( karma ):
    if karma <= BUCKET_THRESHOLDS[0]:
        return get_thresholds_path( BUCKET_THRESHOLDS[0], None );

    for i in range( 1, len( BUCKET_THRESHOLDS ) - 2):
        threshold_lower = BUCKET_THRESHOLDS[i];
        threshold_upper = BUCKET_THRESHOLDS[i+1];
        if karma >= threshold_lower and karma < threshold_upper:
            return get_thresholds_path(threshold_lower, threshold_upper)

    return get_thresholds_path( None, BUCKET_THRESHOLDS[-1] );

def get_thresholds_path( threshold_value_lower, threshold_value_upper ):
    bucket_path = CORPUS_PATH + "/";

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

def write_comment_to_corpus( flattened_comment ):
    cdir = get_bucket_path( flattened_comment.ups - flattened_comment.downs );
    fname = cdir + "/" + comment.id;

    comment_text = comment.body.encode('ascii', 'ignore');
    comment_text = re.sub("&gt;.*?(\n|$)", "", comment_text) # remove quoted content
    comment_text = comment_text.replace("\n"," ")
    if len(comment_text) > 0:
        utils.ensure_dir(fname)
        f = open(fname, 'w')
        f.write( comment_text )
        f.close();


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
                    print '\t' + get_bucket_path(karma) + "\n"
                    write_comment_to_corpus( comment )