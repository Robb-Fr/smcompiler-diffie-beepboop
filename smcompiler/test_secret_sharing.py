"""
Unit tests for the secret sharing scheme.
Testing secret sharing is not obligatory.

MODIFY THIS FILE.
"""
from prime_gen import *
from secret_sharing import *


def test_split():
    s, t = split_n(21)
    assert (2**s) * t + 1 == 21
    s, t = split_n(17)
    assert (2**s) * t + 1 == 17
    s, t = split_n(987)
    assert (2**s) * t + 1 == 987
    s, t = split_n(6327819)
    assert (2**s) * t + 1 == 6327819
    s, t = split_n(2)
    assert (2**s) * t + 1 == 2
    s, t = split_n(3)
    assert (2**s) * t + 1 == 3
    s, t = split_n(1)
    assert (2**s) * t + 1 == 1
    s, t = split_n(0)
    assert (2**s) * t + 1 == 0


def test_prime_generation():
    p = Share(3)
    assert p.value == 3
    q = Share(6)
    assert p + q == Share(9)
