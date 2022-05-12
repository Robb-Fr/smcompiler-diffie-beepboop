from secrets import randbelow


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


def gen_prime(min: int = 2 << 15, max: int = 2 << 16, k: int = 32) -> int:
    n = randbelow(max - min + 1) + min
    while not is_prime(k=k, n=n):
        n = randbelow(max - min + 1) + min
    return n
