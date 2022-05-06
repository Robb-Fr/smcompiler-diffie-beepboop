"""
Unit tests for the secret sharing scheme.
Testing secret sharing is not obligatory.

MODIFY THIS FILE.
"""

from secret_sharing import *


def test():
    raise NotImplementedError("You can create some tests.")


def test_split():
    assert split_n(21) == (2,5)
    assert split_n(17) == (1,7)
    assert split_n(553) == (3,69)
    assert split_n(3) == (1,1)
    assert split_n(2) == (0,1)


