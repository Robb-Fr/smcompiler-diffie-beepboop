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

    # We could use gen_prime() at runtime statically to have different q values,
    # but for efficiency of tests we prefered having a pre-computed prime number.
    # 3525679 is a 20 bits number computed with gen_prime method and k=32
    FIELD_Q = 3525679

    def __init__(self, value, *args, **kwargs):
        # Adapt constructor arguments as you wish
        self.bn = value % self.FIELD_Q

    def __repr__(self):
        # Helps with debugging.
        return "<Share - {} mod {}>".format(self.bn, self.FIELD_Q)

    def __add__(self, other):
        if not isinstance(other, Share):
            raise TypeError("Can only operate between shares")
        return Share((self.bn + other.bn) % self.FIELD_Q)

    def __sub__(self, other):
        if not isinstance(other, Share):
            raise TypeError("Can only operate between shares")
        return Share((self.bn - other.bn) % self.FIELD_Q)

    def __mul__(self, other):
        if not isinstance(other, Share):
            raise TypeError("Can only operate between shares")
        return Share((self.bn * other.bn) % self.FIELD_Q)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Share):
            raise TypeError("Can only operate between shares")
        return self.bn == other.bn


def share_secret(secret: int, num_shares: int) -> List[Share]:
    """Generate secret shares as seen in class"""
    FIELD_Q = Share.FIELD_Q
    shares_values = rd.sample(range(0, FIELD_Q), num_shares - 1)

    share_0 = secret - (sum(shares_values) % FIELD_Q)

    shares_values = [share_0] + shares_values

    return [Share(val) for val in shares_values]


def reconstruct_secret(shares: List[Share]) -> int:
    """Reconstructs secret shares as seen in class"""
    # important to give a start value as we did not define addition between share and int
    return sum(shares, start=Share(0)).bn
