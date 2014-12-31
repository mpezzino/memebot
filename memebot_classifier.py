# http://nbviewer.ipython.org/github/carljv/Will_it_Python/blob/master/MLFH/CH3/ch3_nltk.ipynb
__author__ = 'jonathan'

from pandas import *
import numpy as np
import os
import re
from nltk import NaiveBayesClassifier
import nltk.classify
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from pprint import *

from memebot_config import CORPUS_PATH


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

    if len(sw) is 0:
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


def get_training_set():
    data_path = CORPUS_PATH;
    comments_by_bucket = {}
    for cdir in os.listdir(data_path):
        comments_by_bucket[cdir] = get_msgdir(os.path.join(data_path, cdir))

    train_set = []
    for bucket in comments_by_bucket:
        train_set.extend(features_from_messages(comments_by_bucket[bucket], bucket,
                                                word_indicator))

    return train_set


if __name__ == '__main__':
    classifier = NaiveBayesClassifier.train(get_training_set())
    classifier.show_most_informative_features(50)
    pprint(classifier.classify(word_indicator("Summonses for low-level offenses like public drinking and urination also plunged 94 percent  from 4,831 to 300. Even parking violations are way down, dropping by 92 percent, from 14,699 to 1,241. Drug arrests by cops assigned to the NYPDs Organized Crime Control Bureau  which are part of the overall number  dropped by 84 percent, from 382 to 63.          Not really seeing the downside ")))




