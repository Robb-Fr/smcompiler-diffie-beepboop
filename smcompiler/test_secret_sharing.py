"""
Unit tests for the secret sharing scheme.
Testing secret sharing is not obligatory.

MODIFY THIS FILE.
"""
from prime_gen import *
from secret_sharing import *


def test_split_prime_gen():
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
    from math import sqrt

    def sqrt_test_prime(n: int) -> bool:
        for i in range(2, 1 + int(sqrt(n))):
            if n % i == 0:
                return False
        return True

    p = gen_prime(182, 103821)
    assert p >= 182 and p <= 103821
    assert sqrt_test_prime(p)

    q = gen_prime()
    assert q >= 2 << 15 and q <= 2 << 16
    assert sqrt_test_prime(q)


def test_shares_operations():
    p = Share(3)
    assert p.value == 3
    q = Share(6)
    assert p + q == Share(9)
    assert p * q == Share(18)
    assert q - p == Share(3)


def test_share_spliting():
    secret = 12
    num_shares = 3
    shares = share_secret(secret, num_shares)
    assert len(shares) == num_shares
    assert shares[0] == sum(shares) % Share.FIELD_Q


def test_secret_reconstruction():
    secret = 12
    num_shares = 3
    shares = share_secret(secret, num_shares)
    assert reconstruct_secret(shares) == secret
    num_shares_2 = 5
    shares_2 = share_secret(secret, num_shares_2)
    assert reconstruct_secret(shares_2) == secret
