from secrets import randbelow
from sys import argv


def split_n(n: int) -> tuple((int, int)):
    """
    Utility function for Miller-Rabin Primality test

    Write n = 2^s * t + 1 with t odd
    Returns s and t
    """
    n_1 = n - 1
    s = 0
    while n_1 % 2 == 0 and n_1 != 0:
        s += 1
        n_1 = n_1 >> 1

    t = n_1

    return s, t


def is_prime(k: int, n: int) -> bool:
    """
    Implementation of Miller-Rabin Primality Test (as seen in COM-401)

    Pr[output maybe prime | n composite] ≤ 4 ^ -k
    With k = 5, our probability of failure is around 0.001
    With k = 16, this probability is around 0,000000000232831
    """

    if n == 2:
        return True
    if n % 2 == 0:
        return False
    s, t = split_n(n)
    for _ in range(k):
        b = randbelow(n - 1) + 1
        x = (b**t) % n
        i = 0
        if x != 1:
            while x != (n - 1):
                x = (x * x) % n
                i += 1
                if i == s or x == 1:
                    return False
    return True


def gen_prime(min: int = 2 << 15, max: int = 2 << 16, k: int = 16) -> int:
    """The default parameters return a number of 16 bits that is prime:
    - With a probability of log(n)*4^-k = 16*4^-16 = 0,00000000372529
    - In asymptotic time O(k*log(n)^4)"""

    n = randbelow(max - min + 1) + min
    tested = set()
    while not is_prime(k=k, n=n):
        tested.add(n)
        while n in tested:
            n = randbelow(max - min + 1) + min
    return n


if __name__ == "__main__":
    """give the number of bits as argument"""
    if len(argv) > 1:
        print(gen_prime(2 << (int(argv[1]) - 1), 2 << int(argv[1])))
    else:
        print(gen_prime())
