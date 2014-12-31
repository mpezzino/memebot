# http://nbviewer.ipython.org/github/carljv/Will_it_Python/blob/master/MLFH/CH3/ch3_nltk.ipynb
__author__ = 'jonathan'

import os
import sys
import re
from collections import defaultdict

from nltk import NaiveBayesClassifier
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from boto.s3.key import Key

from memebot_config import *
from memebot import utils


def get_msgdir(path):
    '''
    Read all messages from files in a directory into
    a list where each item is the text of a message.

    Simply gets a list of e-mail files in a directory,
    and iterates get_msg() over them.

    Returns a list of strings.
    '''
    filelist = os.listdir(path)
    filelist = filter(lambda x: x != 'cmds', filelist)
    all_msgs = [get_msg(os.path.join(path, f)) for f in filelist]
    return all_msgs


def get_msg(path):
    '''
    Read in the 'message' portion of an e-mail, given
    its file path. The 'message' text begins after the first
    blank line; above is header information.

    Returns a string.
    '''
    with open(path, 'rU') as con:
        msg = con.readlines()
        return ''.join(msg)


def get_msg_words(msg, sw=[], strip_html=False):
    '''
    Returns the set of unique words contained in an e-mail message. Excludes
    any that are in an optionally-provided list.

    NLTK's 'wordpunct' tokenizer is used, and this will break contractions.
    For example, don't -> (don, ', t). Therefore, it's advisable to supply
    a stopwords list that includes contraction parts, like 'don' and 't'.
    '''

    if sw is None:
        sw = []
    elif len(sw) is 0:
        sw = stopwords.words('english')

    # Strip out weird '3D' artefacts.
    msg = re.sub('3D', '', msg)

    # Strip out html tags and attributes and html character codes,
    # like &nbsp; and &lt;.
    if strip_html:
        msg = re.sub('<(.|\n)*?>', ' ', msg)
        msg = re.sub('&\w+;', ' ', msg)

    # wordpunct_tokenize doesn't split on underscores. We don't
    # want to strip them, since the token first_name may be informative
    # moreso than 'first' and 'name' apart. But there are tokens with long
    # underscore strings (e.g. 'name_________'). We'll just replace the
    # multiple underscores with a single one, since 'name_____' is probably
    # not distinct from 'name___' or 'name_' in identifying spam.
    msg = re.sub('_+', '_', msg)

    # Note, remove '=' symbols before tokenizing, since these are
    # sometimes occur within words to indicate, e.g., line-wrapping.
    msg_words = set(wordpunct_tokenize(msg.replace('=\n', '').lower()))

    # Get rid of stopwords
    msg_words = msg_words.difference(sw)

    # Get rid of punctuation tokens, numbers, and single letters.
    msg_words = [w for w in msg_words if re.search('[a-zA-Z]', w) and len(w) > 1]
    #msg_words = [(w,True) for w in msg_words if re.search('[a-zA-Z]', w) and len(w) > 1]

    return msg_words


def features_from_messages(messages, label, feature_extractor, **kwargs):
    '''
    Make a (features, label) tuple for each message in a list of a certain,
    label of e-mails ('spam', 'ham') and return a list of these tuples.

    Note every e-mail in 'messages' should have the same label.
    '''
    features_labels = []
    for msg in messages:
        features = feature_extractor(msg, **kwargs)
        features_labels.append((features, label))
    return features_labels

def word_indicator(msg, **kwargs):
    '''
    Create a dictionary of entries {word: True} for every unique
    word in a message.

    Note **kwargs are options to the word-set creator,
    get_msg_words().
    '''
    features = defaultdict(list)
    msg_words = get_msg_words(msg, **kwargs)
    for w in msg_words:
        features[w] = True
    return features

def get_training_set_s3():
    threshold_bucket = utils.get_s3_connection().get_bucket(S3_CORPUS_BUCKET)
    k = Key( threshold_bucket )

    comments_by_bucket = {}

    comment_objs = threshold_bucket.list()
    print "Found ", len(comment_objs), "comments"
    for comment_obj in comment_objs:
        k.key = comment_obj
        comment_text = k.get_contents_as_string()
        threshold_bucket = comment_obj.name.split("/")[0]
        if not comments_by_bucket.has_key(threshold_bucket):
            comments_by_bucket[threshold_bucket] = []
        comments_by_bucket[threshold_bucket].append( comment_text )


    train_set = []
    for threshold_bucket in comments_by_bucket:
        print len( comments_by_bucket[threshold_bucket] ) + "\tcomments with karma\t" + threshold_bucket
        train_set.extend(features_from_messages(comments_by_bucket[threshold_bucket], threshold_bucket,
                                                word_indicator))

    return train_set


def get_training_set():
    data_path = CORPUS_PATH;
    comments_by_bucket = {}
    for cdir in os.listdir(data_path):
        cdir_path = os.path.join(data_path, cdir)
        if os.path.isdir( cdir_path ):
            comments_by_bucket[cdir] = get_msgdir(cdir_path)

    train_set = []
    for bucket in comments_by_bucket:
        train_set.extend(features_from_messages(comments_by_bucket[bucket], bucket,
                                                word_indicator))

    return train_set

classifier = NaiveBayesClassifier.train(get_training_set_s3())

def karma_classify( text ):
    return classifier.classify(word_indicator(text))

if __name__ == '__main__':
    classifier.show_most_informative_features(50)
    while True:
        sys.stdout.write("Comment: ")
        print classifier.classify(word_indicator(raw_input()))




