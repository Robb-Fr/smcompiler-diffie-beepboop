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
    q = gen_prime(10000, 100000)

    shares = rd.sample(range(0,q),num_shares)

    share_0 = secret - (sum(shares) % q)

    shares.insert(0,share_0)

    return shares


def reconstruct_secret(shares: List[Share]) -> int:
    return sum(shares) % q


def gen_prime(min: int, max: int) -> int:
    n = rd.randint(min, max)
    while not is_prime(5, n):
        n = rd.randint(min , max)

def is_prime(k: int, n: int) -> bool:
    """
    Implementation of Miller-Rabin Primality Test (as seen in COM-401)

    Pr[output maybe prime | n composite] ≤ 4 ^ -k 
    With k = 5, our probability of failure is around 0.001
    """

    if n == 2:
        return True 
    if n % 2 == 0:
        return False

    s, t = split_n(n)

    for i in range(k):
        b = rd.randint(1,n-1)
        x = (b ** t) % n

        j = 0

        if x != 1:
            while(x != n-1):
                x = (x ** 2) % n 
                j += 1 
                if(i == (s-1) or x == 1):
                    return False

    return True
    
def split_n(n: int) -> (int, int):
    """
    Utility function for Miller-Rabin Primality test 

    Write n = 2^s * t + 1 with t odd 
    Returns s and t 
    """
    n_1 = n - 1 
    s = 0 
    while(n_1 % 2 == 0 or n_1 == 0):
        s += 1 
        n_1 = n_1 / 2 
    
    t = int((n-1) / (2 ** s))

    return s, t



# Feel free to add as many methods as you want.
