"""
Digital DNA Sequencer for Twitter
"""
import json
import numpy as np

ENTITY = 'E'
HASHTAG = 'T'
MEDIA = 'G'
MENTION = 'C'
NONE = 'N'
MIXED = 'X'
REPLY = 'T'
RETWEET = 'C'
TWEET = 'A'
URL = 'A'
UNKNOWN = 'U'


class TwitterDDNASequencer():
    """ Twitter Digital DNA Sequencer.
    Compute sequences of digital DNA from twitter timelines (check out
    https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html)

    Parameters
    ----------
    alphabet :  string or callable, default ‘b3_type’
        mapping between the column value and the corresponding base.
        If alphabet_ is a callable function, it is called on each
        pair of instances (rows) and the resulting value recorded.
        The callable should take two arrays as input and return
        one value indicating the distance between them.
        Prebuild alphabets are the following:

        - 'b3_type',  where the correspondence  is
                - 'A' for tweet
                - 'C' for reply
                - 'T' for retweet
        - 'b3_content', where the correspondence  is
                - 'N' tweet contains no entities (plain text)
                - 'E' tweet contains entities of one type
                - 'X' tweet contains entities of mixed types
        - 'b6_content', where the correspondence  is
                - 'N' tweet contains no entities (plain text)
                - 'U' tweet contains one or more URLs
                - 'H' tweet contains one or more hashtags
                - 'M' tweet contains one or more mentions
                - 'D' tweet contains one or more medias
                - 'X' tweet contains entities of mixed types

    Attributes
    ----------
    input_shape : tuple
        The shape the data passed to :meth:`fit`


    References
    ----------
    S. Cresci, R. D. Pietro, M. Petrocchi, A. Spognardi and M. Tesconi,
    "Social Fingerprinting: Detection of Spambot Groups Through DNA-Inspired Behavioral Modeling",
    IEEE Transactions on Dependable and Secure Computing, vol. 15, no. 4, pp. 561-576, 1 July-Aug. 2018,
    https://ieeexplore.ieee.org/document/7876716

    S. Cresci, R. di Pietro, M. Petrocchi, A. Spognardi and M. Tesconi,
    "Exploiting Digital DNA for the Analysis of Similarities in Twitter Behaviours",
    2017 IEEE International Conference on Data Science and Advanced Analytics (DSAA),
    Tokyo, 2017, pp. 686-695, https://ieeexplore.ieee.org/document/8259831
    """

    def __init__(self, alphabet='b3_type', input_file=''):
        import warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
        self.alphabet = alphabet
        self.input_file = input_file

    def fit(self, X=None, y=None):
        """Simply assigns the right alphabet mapper function to remap_

        Parameters
        ----------
        X : None
            The pipeline API requires this parameter.

        y : None
            There is no need of a target in a transformer, yet the pipeline API
            requires this parameter.

        Attributes
        ----------
        remap_ : function that takes a tweet with the same format retrieved from
                GET statuses/user_timeline call and retrieves the corresponding character
                given the alphabet parameter.

        Returns
        -------
        self : object
            Returns an instance of self.
        """
        if self.alphabet == 'b3_type':
            self.remap_ = self._tweet2char_b3_type
        elif self.alphabet == 'b3_content':
            self.remap_ = self._tweet2char_b3_content
        elif self.alphabet == 'b6_content':
            self.remap_ = self._tweet2char_b6_content
        else:
            self.remap_ = None

        return self

    def transform(self, X=None):
        """ The function that transform the array of timelines to digital dna sequences given the alphabet.

        Parameters
        ----------
        X : array-like of shape = [# of tweets, 1]
            The input samples, each sample is a python dict of a tweet as retrieved
            from twitter user timelines API (check out
            https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html)

        Returns
        -------
        X_transformed : array of string of shape = [# of users, 1]
            The array containing the digital dna sequences
            """
        if self.input_file != '':
            f = open(self.input_file, "r")
            X = json.loads(f.read())
        elif X == None:
            raise ValueError('X cannot be None if input_file is not specified')

        ddna_size = 0
        res = {}
        for row in X:
            uid = self._nested_get(row, 'user.id')
            code = self.remap_(row)
            if uid in res:
                res[uid] += code
            else:
                res[uid] = code
            ddna_size = max(ddna_size, len(res[uid]))
        # dtype = [('uid', 'i8'), ('ddna', 'U' + str(ddna_size))]
        res = np.array(list(res.items()))  # , dtype=dtype)
        return res

    def fit_transform(self, X=None, y=None):
        """ Fit and transform

        Parameters
        ----------
        X : array-like of shape = [# of tweets, 1]
            The input samples, each sample is a python dict of a tweet as retrieved
            from twitter user timelines API (check out
            https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html)

        y: ignored parameter needed to mantain a standard pattern

        Returns
        -------
        X_transformed : array of shape = [n_samples, 2]
            The resulting array where the first column is the user id and the second is the translated sequence
        """
        return self.fit(X, y).transform(X)

    def get_params(self):
        """Get parameters for this estimator.

        Returns
        -------
        params : mapping of string to any
            Parameter names mapped to their values.
        """
        return {'alphabet': self.alphabet,
                'input_file': self.input_file}

    def set_params(self, alphabet, input_file):
        """Set the parameters of this estimator. The method works on simple estimators as well as on nested objects
        (such as pipelines). The latter have parameters of the form ``<component>__<parameter>`` so that it's possible
        to update each component of a nested object.

        Returns
        -------
        self
        """
        self.alphabet = alphabet
        self.input_file = input_file

    def _nested_get(self, dct, keys):
        for key in keys.split('.'):
            try:
                dct = dct[key]
            except KeyError:
                return None
        return dct

    def _tweet2char_b3_type(self, tweet):
        reply_id = tweet['in_reply_to_user_id']
        is_reply = reply_id != 0 and reply_id is not None
        retweet_id = self._nested_get(tweet, 'retweeted_status.id')
        is_retweet = retweet_id != 0 and retweet_id is not None

        if not is_reply and not is_retweet:
            return TWEET
        elif is_reply and not is_retweet:
            return REPLY
        return RETWEET

    def _tweet2char_b3_content(self, tweet):
        # sums not empty lists within entities dict
        n_entities = sum([1 for k, v in tweet['entities'].items() if v])

        if n_entities == 0:
            return NONE
        elif n_entities > 1:
            return MIXED
        return ENTITY

    def _tweet2char_b6_content(self, tweet):
        # sums not empty lists within entities dict
        n_entities = sum([1 for k, v in tweet['entities'].items() if v])

        if n_entities == 0:
            return NONE
        elif n_entities > 1:
            return MIXED
        else:
            type = [k for k, v in tweet['entities'].items() if v][0]
            if type == 'url':
                return URL
            elif type == 'hashtags':
                return HASHTAG
            elif type == 'user_mentions':
                return MENTION
            elif 'extended_entities' in tweet:
                return MEDIA
            return UNKNOWN
