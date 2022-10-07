import os
import re
from collections import Counter

import numpy as np
from numpy.testing import assert_array_equal

from ..lcs import LongestCommonSubsequence
from ..verbosity import Verbosity


def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))


path, filename = '/tmp', 'test_lcs'
fullname = path + '/' + filename


def assert_true_count(actual, desired_count, err_percentage=.05):
    if not abs(Counter(actual)[True] - desired_count) < len(actual) * err_percentage:
        msg = 'true count (' + str(Counter(actual)[True]) + ') is too far from desired'
        raise AssertionError(msg)


def test_mat_gsa():
    X = ['banana', 'ananan', 'anana', 'hanoi', 'banas']
    purge(path, filename)
    estimator = LongestCommonSubsequence(out_path=fullname, verbosity=Verbosity.FILE_EXTENDED)
    estimator.fit(X)
    res = np.genfromtxt(fullname + '.mat', delimiter=',', skip_header=0, names=True, dtype="i4,i4,i4,i4,|U10")
    assert_array_equal(res['num_texts'], [2, 3, 4, 5])
    assert_array_equal(res['length'], [5, 5, 3, 2])
    assert_array_equal(res['begin'], [12, 11, 11, 11])
    assert_array_equal(res['end'], [13, 13, 14, 15])
    assert_array_equal(res['subsequence'], ['anana', 'anana', 'ana', 'an'])
    res = np.genfromtxt(fullname + '.gsa', delimiter=',', skip_header=0, names=True, dtype="i4")
    purge(path, filename)
    assert_array_equal(res['wordindex'],
                       [1, 2, 3, 4, 5, 1, 3, 2, 1, 3, 2, 1, 3, 2, 5, 4, 5, 1, 5, 4, 4, 2, 1, 3, 2, 1, 3, 2, 5, 4, 4, 5])


def test_1000():
    purge(path, filename)
    alphabet = [chr(i) for i in range(48, 51)]
    np_alphabet = np.array(alphabet, dtype="|S1")
    codes_len = 1000
    codes_size = 500
    nrep = 500
    X = np.random.choice(np_alphabet, [codes_size, codes_len])
    X = [b"".join(X[i]).decode('utf-8') for i in range(codes_size)]
    nrep_arr = [nrep if i == 0 else 1 for i in range(len(X))]
    X = np.repeat(X, nrep_arr, axis=0)
    estimator = LongestCommonSubsequence(out_path=fullname, verbosity=Verbosity.FILE, window=10)
    y = estimator.fit_predict(X)
    purge(path, filename)
    assert_true_count(y, nrep)
