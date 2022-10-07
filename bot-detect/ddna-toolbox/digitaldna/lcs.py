"""
This is a module to be used as a reference for building other modules
"""
import warnings
from glcr import longest_common_subsequence
from multiprocessing import Process

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_array

from .verbosity import Verbosity


# noinspection PyIncorrectDocstring
class LongestCommonSubsequence(BaseEstimator):
    """ The Digital DNA Python implementation.

    Parameters
    ----------
    in_path : str, optional
        The name with absolute path of a file containing the sequences you want to process.
        The input file must be a txt file and the first row must contain the number of sequences to read.
        Default: ''

    out_path : str, optional
        The output file name with absolute path of the file where the algorithm will save result in case of
        verbosity equals to `Verbosity.FILE` or `Verbosity.FILE_EXTENDED`.
        Default: '/tmp/glcr_cache'

    overwrite : boolean, optional
        It must be False to use the LCS files produced in a previous fit call, in this case the file names are
        the ones specified in the out_path parameter. If True, recomputes the LCS files.
        Default: False

    threshold : boolean, optional
        It must be False to use the LCS files produced in a previous fit call, in this case the file names are
        the ones specified in the out_path parameter. If True, recomputes the LCS files.
        Default: False

    window : str, optional
        The size of the window used to compute the cutting threshold between bot and not bot. The cutting point is
        computed by smoothing the curve, deriving the result and taking the first (l.h.s.) local maxima. The window
        parameter influences both smoothing and finding the local maxima.
        It must be 2 < window < n_accounts.
        Default: 10

    verbosity : str, optional
        The verbosity parameter is used to specify whether to save results to files or not. It must be:\n
        - TEST              does not write anything, used for benchmarking
        - MEMORY_ONLY       retrieves only the couples (sequence length, # of accounts), used for plots
        - FILE              produces 2 files, a file named out_path + '.gsa' where each row contains the identifier of the sequence. In the other file, named out_path + '.mat', each row contains:\n
                            - sequence length
                            - # of accounts
                            - range of indexes (begin and end)
        - FILE_EXTENDED     as FILE but the in_path + '.mat' file contains also the column of the common subsequence

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

    M. Arnold, E. Ohlebusch, "Linear Time Algorithms for Generalizations of the Longest Common Substring Problem",
    Algorithmica, vol 60, pp. 806-818, 4 August 2011, https://link.springer.com/article/10.1007/s00453-009-9369-1
    """
    def __init__(self, in_path='', out_path='/tmp/glcr_cache', overwrite=False, threshold='auto', window=10, verbosity=Verbosity.FILE):
        self.in_path = in_path
        self.out_path = out_path
        self.overwrite = overwrite
        self.threshold = threshold
        self.window = window
        if self.window < 2:
            raise ValueError('window parameter cannot be less than 2.')
        self.verbosity = verbosity

    def fit(self, X, y=None):
        """Computes the longest common subsequence

        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samples, n_features]
            The training input samples.

        y : None
            There is no need of a target in a transformer, yet the pipeline API
            requires this parameter.

        Attributes
        ----------
        lcs_index_ : pandas dataframe, shape (distinct couples (lcs, n_of_accounts), 2), default=None
            The dataframe containing the distict couples lcs, n_of_accounts). Only if:
            verbosity == Verbosity.MEMORY_ONLY

        Returns
        -------
        self : object
            Returns self.
        """
        warnings.simplefilter(action='ignore', category=FutureWarning)
        self.gsa_ = '.gsa'
        self.mat_ = '.mat'

        if self.in_path == '':
            X = self._unicode_to_ascii(X)
            X = check_array(X, ensure_2d=False)

        print("fitting...")
        if self.verbosity == Verbosity.MEMORY_ONLY:
            self.lcs_ = longest_common_subsequence(self._unicode_to_ascii(X), self.in_path, self.out_path,
                                                   self.verbosity)
        elif self.verbosity > Verbosity.MEMORY_ONLY:
            if self.in_path == '' or self.overwrite:
                p = Process(target=longest_common_subsequence, args=(X, self.in_path, self.out_path, self.verbosity))
                p.start()
                p.join()
        return self

    def predict(self, X=None):
        """ Predict the labels (True bot, False Not Bot) of X according to lcs and window parameter:.
        If X is None, returns the same as fit_predict(X_train).
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features), default=None
            The query sample or samples to identify bot groups. If None,
            makes prediction on the training data.
        Returns
        -------
        y : array, shape (n_samples,)
            Returns True for bots and False for real timeline.
        """
        y = None
        if self.verbosity > Verbosity.MEMORY_ONLY:
            y = np.full(len(X), False)
            mat_ix = set()
            if self.threshold == 'auto':
                print('finding cut...')
                lengths = pd.read_csv(self.out_path+self.mat_, usecols=['length']).length.values
                self.cut_ = self._decision_function(lengths)
            else:
                self.cut_ = self.threshold
            print('predicting...')

            class BreakIt(Exception):
                pass
            try:
                for df in pd.read_csv(self.out_path + self.mat_, chunksize=500000):
                    for ix, row in df.iterrows():
                        curr_set = mat_ix.union(set(range(int(row.begin), int(row.end) + 1)))
                        if row.num_texts >= self.cut_:  # not bot, exit
                            raise BreakIt
                        mat_ix = curr_set
            except BreakIt:
                pass
            ix_size = len(mat_ix)
            ix_count = 0
            bot_ix = np.empty(ix_size, dtype=int)
            try:
                for df in pd.read_csv(self.out_path + self.gsa_, header=0, usecols=['wordindex'], squeeze=True,
                                      chunksize=500000):
                    for ix, wordindex in df.items():
                        if ix in mat_ix:
                            # TODO delete the -1 when fix the gsa file
                            bot_ix[ix_count] = wordindex - 1
                            ix_count += 1
                            if ix_count == ix_size:
                                raise BreakIt
                            mat_ix.remove(ix)
            except BreakIt:
                y[bot_ix] = True
        else:
            warnings.warn("Cannot predict with verbosity level lower than FILE", Warning)
        print('done.')
        return y

    def fit_predict(self, X, y=None):
        """"Fits the model to the training set X and returns the labels
        (True for bot, False for non bot) on the training set according to the window parameter.
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features), default=None
            The query sample or samples to compute the Local Outlier Factor
            w.r.t. to the training samples.

        Attributes
        ----------
        lcs_index_ : pandas dataframe, shape (distinct couples (lcs, n_of_accounts), 2), default=None
            The dataframe containing the distict couples lcs, n_of_accounts)

        Returns
        -------
        y : array, shape (n_samples,)
            Returns True for bots and False for real timeline.
        """
        return self.fit(X).predict(X)

    def plot_LCS(self):
        """"Plots the longest common subsequence curve as (number of accounts, sequence length)

        Attributes
        ----------
        lcs_index_ : pandas dataframe, shape (distinct couples (lcs, n_of_accounts), 2), default=None
            The dataframe containing the distict couples lcs, n_of_accounts)

        Returns
        -------
        self : returns an instance of self.
        """
        plt.xlabel('# of accounts')
        plt.ylabel('LCS')
        if self.verbosity > Verbosity.MEMORY_ONLY and not hasattr(self, 'lcs_'):
            self.lcs_ = pd.read_csv(self.out_path + self.mat_, usecols=['length', 'num_texts']) \
                .drop_duplicates().reset_index().drop(['index'], axis=1)
        plt.plot(self.lcs_.num_texts, self.lcs_.length, marker='x')
        if hasattr(self, 'cut_'):
            plt.plot([self.cut_, self.cut_], [0, max(self.lcs_.length)], linestyle='--')
        #plt.show()
        return plt

    def plot_LCS_log(self):
        """"Plots the longest common subsequence curve as (log(number of accounts), log(sequence length))

        Attributes
        ----------
        lcs_index_ : pandas dataframe, shape (distinct couples (lcs, n_of_accounts), 2), default=None
            The dataframe containing the distict couples lcs, n_of_accounts)

        Returns
        -------
        self : returns an instance of self.
        """
        plt.xlabel('log(# of accounts)')
        plt.ylabel('log(LCS)')
        if self.verbosity > Verbosity.MEMORY_ONLY and not hasattr(self, 'lcs_'):
            self.lcs_ = pd.read_csv(self.out_path + self.mat_, usecols=['length', 'num_texts']) \
                .drop_duplicates().reset_index().drop(['index'], axis=1)
        plt.loglog(self.lcs_.num_texts, self.lcs_.length, marker='x')
        if hasattr(self, 'cut_'):
            plt.plot([self.cut_, self.cut_], [0, max(self.lcs_.length)], linestyle='--')
        # plt.show()
        return plt

    def _decision_function(self, X):
        ''' Finds the first relative maximum on the smoothed LCS vector'''
        length = len(X)
        w_size = self.window
        X_avg_diff = np.diff(self._running_mean(X, w_size))
        i = 0
        max_index = length - w_size
        for i in range(max_index):
            if X_avg_diff[i] < np.mean(X_avg_diff[i:i+w_size]):
                break
        t = np.argmax(X_avg_diff[i:])
        return t + i - 1

    def _running_mean(self, x, winsize):
        for i in range(len(x)):
            x[i] = x[max(0, i):min(i + winsize, len(x))].mean()
        return x

    def _unicode_to_ascii(self, array):
        def f(item):
            return str(item) + '\0'

        def v(x):
            return np.vectorize(f)(x)

        return v(array).astype('S')
