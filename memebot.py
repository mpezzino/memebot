__author__ = 'jonathan'

from pprint import pprint

from memebot_config import BOT_LOGIN_PASSWORD

import praw


CORPUS_PATH= "/var/memebot"

BUCKET_THRESHOLDS=[-10,   \
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
        bucket_path +=  str( threshold_value_lower ).replace( "-", "neg_");

    if threshold_value_lower is not None and threshold_value_upper is not None:
        bucket_path += "-";

    if threshold_value_upper is not None:
        bucket_path += str( threshold_value_upper ).replace( "-", "neg_")

    return bucket_path;

if __name__ == '__main__':
    news_subreddit = bot.get_subreddit('news');
    for submission in news_subreddit.get_hot(limit=3):
        if len(submission.comments) > 0:
            for comment in praw.helpers.flatten_tree(submission.comments)[0:1]:
                #pprint( vars(comment) )
                karma = comment.ups - comment.downs;
                print comment.body
                print '\t' + str(karma)
                print '\t' + get_bucket_path(karma)