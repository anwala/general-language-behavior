from numpy.testing import assert_equal

from ..twitter_sequencer import *


# TODO fit transform from input_file


def dummy_data_gen_():
    X = []
    in_reply_to_user_id = [0, None, 2, 3, None, None]
    retweeted_status = [0, 1, 2, None, 5, None]
    uid = [111, 111, 111, 222, 222, 222]
    entities = [{}, {'url': '123'}, {'hashtags': '123'}, {'user_mentions': '123'}, {'extended_entities': '123'},
                {'user_mentions': '123', 'url': '123'}]
    for i in range(len(in_reply_to_user_id)):
        tweet = {'in_reply_to_user_id': retweeted_status[i], 'retweeted_status': {'id': retweeted_status[i]},
                 'user': {'id': uid[i]}, 'entities': entities[i]}
        X.append(tweet)
    Y_b3t = [[111, TWEET + RETWEET + RETWEET], [222, TWEET + RETWEET + TWEET]]
    Y_b3c = [[111, NONE + ENTITY + ENTITY], [222, ENTITY + ENTITY + MIXED]]
    Y_b6c = [[111, NONE + URL + HASHTAG], [222, MENTION + UNKNOWN + MIXED]]
    return X, Y_b3t, Y_b3c, Y_b6c


X, Y_b3t, Y_b3c, Y_b6c = dummy_data_gen_()


def test_b3_type():
    estimator = TwitterDDNASequencer(alphabet='b3_type')
    X_transformed = estimator.fit_transform(X)
    assert_equal(X_transformed, Y_b3t)


def test_b3_content():
    estimator = TwitterDDNASequencer(alphabet='b3_content')
    X_transformed = estimator.fit_transform(X)
    assert_equal(X_transformed, Y_b3c)


def test_b6_content():
    estimator = TwitterDDNASequencer(alphabet='b6_content')
    X_transformed = estimator.fit_transform(X)
    assert_equal(X_transformed, Y_b6c)
