"""
Secret sharing scheme.
"""

from typing import List
import random as rd
from prime_gen import gen_prime


class Share:
    """
    A secret share in a finite field.
    """

    # We could use gen_prime() at runtime statically but we for efficiency of tests we prefered having a pre-computed 20 bits numbers with a k=32
    FIELD_Q = 3525679

    def __init__(self, value, *args, **kwargs):
        # Adapt constructor arguments as you wish
        self.value = value % self.FIELD_Q

    def __repr__(self):
        # Helps with debugging.
        return "<Share - {} mod {}>".format(self.value, self.FIELD_Q)

    def __add__(self, other):
        if not isinstance(other, Share):
            raise TypeError("Can only operate between shares")
        return Share((self.value + other.value) % self.FIELD_Q)

    def __sub__(self, other):
        if not isinstance(other, Share):
            raise TypeError("Can only operate between shares")
        return Share((self.value - other.value) % self.FIELD_Q)

    def __mul__(self, other):
        if not isinstance(other, Share):
            raise TypeError("Can only operate between shares")
        return Share((self.value * other.value) % self.FIELD_Q)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Share):
            raise TypeError("Can only operate between shares")
        return self.value == other.value


def share_secret(secret: int, num_shares: int) -> List[Share]:
    """Generate secret shares."""
    FIELD_Q = Share().FIELD_Q
    shares = rd.sample(range(0, FIELD_Q), num_shares)

    share_0 = secret - (sum(shares) % FIELD_Q)

    shares = [share_0] + shares

    return shares


def reconstruct_secret(shares: List[Share]) -> int:
    FIELD_Q = Share().FIELD_Q
    return sum(shares) % FIELD_Q


"""

UTILITY FUNCTIONS 

"""
