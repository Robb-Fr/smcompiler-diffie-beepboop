"""
Secret sharing scheme.
"""

from typing import List
import random as rd


class Share:
    """
    A secret share in a finite field.
    """

    def __init__(self, *args, **kwargs):
        # Adapt constructor arguments as you wish
        raise NotImplementedError("You need to implement this method.")

    def __repr__(self):
        # Helps with debugging.
        raise NotImplementedError("You need to implement this method.")

    def __add__(self, other):
        raise NotImplementedError("You need to implement this method.")

    def __sub__(self, other):
        raise NotImplementedError("You need to implement this method.")

    def __mul__(self, other):
        raise NotImplementedError("You need to implement this method.")


def share_secret(secret: int, num_shares: int) -> List[Share]:
    """Generate secret shares."""
    q = 23099 # TODO: Change this lol

    shares = rd.sample(range(0,q),num_shares)

    share_0 = secret - (sum(shares) mod % q)

    shares.insert(0,share_0)

    return shares


def reconstruct_secret(shares: List[Share]) -> int:
    """Reconstruct the secret from shares."""
    raise NotImplementedError("You need to implement this method.")


def gen_prime(min: int, max: int) -> int:
    n = randint(min, max)
    while not isPrime(n):
        n = randint(min , max)


# Feel free to add as many methods as you want.
