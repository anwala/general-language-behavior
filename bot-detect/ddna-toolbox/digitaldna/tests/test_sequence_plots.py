from numpy.testing import assert_equal, assert_array_almost_equal, assert_array_equal
from ..sequence_plots import *


def test_compute_entropy():
    # entropy values are computed here: http://www.shannonentropy.netmark.pl/calculate
    X = [list('123123123123121212'), list('absfdvebavdgabsavgasb'), list('1111111111111111111111'),
         list('123456789'), list('00000000000000'),
         list('123456789gsadfvop8u4w3hji0as7drfpiw3o4htfya’0sdfgphi0arepgiaudfgt’8piuhagv')]
    entropies = [1.54198, 2.81520, .0, 3.16993, .0, 4.58138]
    assert_array_almost_equal(entropies, SequencePlots()._compute_entropy(X), 5, 'Entropy of X is wrong')


def test_string_arr_to_int_matrix_():
    X = np.array(['AAABB', 'AAABBBB', 'CDACCBBA', 'CDACCBB'])
    X_ascii = [[65, 65, 65, 66, 66, 0, 0, 0],  # 0 padding
               [65, 65, 65, 66, 66, 66, 66, 0],
               [67, 68, 65, 67, 67, 66, 66, 65],
               [67, 68, 65, 67, 67, 66, 66, 0]]
    assert_equal(SequencePlots()._string_arr_to_int_matrix(X), X_ascii)


def test_find_alphabet_():
    X = ['aabbcder', 'saefs']
    alphabet = list('abcdefrs')
    assert_array_equal(np.sort(SequencePlots()._find_alphabet(X)), np.sort(alphabet))
