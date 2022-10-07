from collections import Counter
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.utils.validation import check_array
from .twitter_sequencer import ENTITY, HASHTAG, MEDIA, MENTION, NONE, MIXED, REPLY, RETWEET, TWEET, URL, UNKNOWN

plt.rcParams['image.cmap'] = 'spring'


class SequencePlots():
    """ The Digital DNA plots utility class.

        Parameters
        ----------
        alphabet : string, optional
            The sequences' alphabet, used to show prettier labels, possible values are:\n
            - 'b3_type'
            - 'b3_content'
            - 'b6_content'
            - None
            Default: None

        """

    def __init__(self, alphabet=None):
        import warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
        if alphabet == 'b3_type':
            self.alphabet = {TWEET: 'tweet', RETWEET: 'retweet', REPLY: 'reply'}
        elif alphabet == 'b3_content':
            self.alphabet = {NONE: 'no entity', MIXED: 'mixed', ENTITY: 'entity'}
        elif alphabet == 'b6_content':
            self.alphabet = {NONE: 'no entity', MIXED: 'mixed', URL: 'url',
                             HASHTAG: 'hashtag', MENTION: 'mention', MEDIA: 'media',
                             UNKNOWN: 'unknown entity'}
        else:
            self.alphabet = None

    def plot_alphabet_distribution(self, X):
        """ This function produces a box plot where each box represents the distribution of a letter
            in the sequences. The alphabet is inferred from the sequences.
            
            Parameters
            ----------
            X : array-like, shape (n_samples, 1), mandatory
                The input sequences of digital dna
                
            Returns
            -------
            y : an instance of self
            """
        check_array(X, ensure_2d=False, dtype=np.unicode_)
        length = len(X)
        freq = pd.DataFrame(index=range(length), columns=self._find_alphabet(X))
        for i in range(length):
            freq.at[i] = dict(Counter(X[i]))
        freq = freq.dropna(axis='columns', how='all').fillna(0).astype(int)
        sns.boxplot(data=freq, color='cyan').set_ylabel('# of occurrences')
        sns.swarmplot(data=freq, color='red').set_xlabel('alphabet')
        return self

    def plot_sequences_color(self, X):
        """ This function produces a matrix image where each row is a digital dna sequence and each
            letter is represented by a different color.
            
            Parameters
            ----------
            X : array-like, shape (n_samples, 1), mandatory
                The input sequences of digital dna
                
            Returns
            -------
            y : an instance of self
            """
        check_array(X, ensure_2d=False, dtype=np.unicode_)
        X = np.array(sorted(X, key=len, reverse=True))
        matrix = self._string_arr_to_int_matrix(X)
        remap = dict((k, i) for i, k in enumerate(np.unique(matrix)))
        cmap = ListedColormap(
            [plt.get_cmap("tab10")(i) if i > 0 or len(remap) == 1 else 'white' for i in remap.values()])
        mat = plt.matshow(np.vectorize(remap.get)(matrix), cmap=cmap, aspect='auto')
        cbar = plt.colorbar(mat)
        if self.alphabet is None:
            labels = [chr(k) if k > 0 else 'no-data' for k in remap.keys()]
        else:
            labels = [chr(k) + ' (' + self.alphabet[chr(k)] + ')' if k > 0 else 'no-data' for k in remap.keys()]
        locs = np.arange(1 / (2 * len(labels)), 1, 1 / len(labels))
        cbar.ax.get_yaxis().set(ticks=locs, ticklabels=labels)
        plt.show()
        return self

    def plot_intrasequence_entropy(self, X):
        """ This function produces a box plot with a single box representing the distribution of
            the intra-sequence entropies (the Shannon Entropy computed over a single digital dna sequence).
            
            Parameters
            ----------
            X : array-like, shape (n_samples, 1), mandatory
                The input sequences of digital dna
                
            Returns
            -------
            y : an instance of self
            """
        check_array(X, ensure_2d=False, dtype=np.unicode_)
        entropy = self._compute_entropy(X)
        ax = sns.boxplot(data=entropy, color="white")
        ax = sns.swarmplot(data=entropy, color="red")
        ax.set_ylabel("Intraseq Shannon Entropy")
        ax.set_yticks(np.arange(.0, 1.8, .2))
        ax.set_xticklabels([])
        ax.set_aspect(1.)
        return plt

    def plot_intersequence_entropy(self, X):
        """ This function produces a composite plot. On the left a boxplot representing the distribution
            of the inter-sequence entropy (Shannon's Entropy of the letters in the same with same sequence
            index but in different sequences). On the right a scatterplot of the entropies ordered by sequence index.
            
            Parameters
            ----------
            X : array-like, shape (n_samples, 1), mandatory
                The input sequences of digital dna
                
            Returns
            -------
            y : an instance of self
            """
        check_array(X, ensure_2d=False, dtype=np.unicode_)
        entropy = self._compute_entropy(self._string_arr_to_int_matrix(X).T)
        f, axes = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 3]})
        unique = np.unique(entropy)
        ax = sns.boxplot(data=unique, color="white", ax=axes[0])
        ax = sns.swarmplot(data=unique, color="red", ax=axes[0])
        ax.set_ylabel("Interseq Shannon Entropy")
        ax.set_yticks(np.arange(.0, 1.8, .2))
        ax.set_xticklabels([])
        plt.plot(range(len(entropy)), entropy, '-x')
        plt.subplots_adjust(wspace=.5)
        return plt

    def _compute_entropy(self, X):
        arr_size = len(X)
        entropies = np.zeros((arr_size, 1), dtype=np.float32)
        for i in range(arr_size):
            non_zero_X = np.trim_zeros(X[i])
            d = Counter(non_zero_X)
            # when sequences are trasposed, 0 means empty, so it's dropped
            curr_len = len(non_zero_X)
            prob_list = [count / curr_len for key, count in d.items()]
            entropies[i] = -sum(prob_list * np.log2(prob_list))
        return entropies.flatten()

    def _string_arr_to_int_matrix(self, X):
        rowsize = len(X)
        colsize = len(max(X, key=len))
        matrix = np.zeros((rowsize, colsize), dtype=np.int8)
        for i in range(rowsize):
            s = list(X[i])
            length = len(s)
            for j in range(length):
                matrix[i, j] = ord(s[j])
        return matrix

    def _find_alphabet(self, X):
        letters = [list(set(s)) for s in X]
        return list(set(item for sublist in letters for item in sublist))
