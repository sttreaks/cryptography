#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import typing
import math

SIZE = 64  # 128 counting to long


def is_prime(num: int, k: int) -> bool:
    """The Miller–Rabin primality test: an algorithm which determines whether a given number is prime

    :param num: an odd integer to be tested for primality
    :param k: the number of rounds of testing to perform
    :return: bool, False if n is found to be composite, True otherwise
    """
    if num < 2:
        return False

    d = num - 1
    r = 0

    while not (d & 1):
        r += 1
        d >>= 1

    for _ in range(k):
        tries = 0
        bit_size = SIZE

        while True:  # generating 1 <= a <= num - 2
            a = getrandom(bit_size)
            if a <= num - 3:
                break

            if tries % 10 == 0 and tries:
                bit_size -= 1
            tries += 1

        a += 1

        x = pow(a, d, num)
        if x == 1 or x == num - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, num)
            if x == 1:
                return False
            if x == num - 1:
                break
        else:
            return False

    return True


def getrandom(nbits: int) -> int:
    """Function which generate random int < 2 ^ nbits

    :param nbits: int, size
    :return: int, random integer
    """
    return int.from_bytes(os.urandom(nbits), 'big', signed=False)


def getprime(nbits: int) -> int:
    """Returns a prime number that can be stored in 'nbits' bits.

    :param nbits: number of bits to generate
    :return: int, prime number
    """

    while True:
        random_int = getrandom(nbits)
        if is_prime(random_int, 10):  # Recomendated number of rounds ~10
            return random_int


def gcd(a: int, b: int) -> int:
    """The function that returns the gcd

    :param a: int
    :param b: int
    :return: int, gcd
    """
    while b != 0:
        a, b = b, a % b
    return a


def coprime(a: int, b: int) -> bool:
    """Function which check whether a and b is coprime

    :param a: int
    :param b: int
    :return: bool, whether a and b is coprime
    """
    return gcd(a, b) == 1


def getcoprime(num: int, nbits: int) -> int:
    """Function which find coprime int to num

    :param num: int, number to which needed to find coprime
    :param nbits: int, number of bits to generate random
    :return: int, coprime to num
    """
    while True:
        cop = getrandom(nbits)
        if cop < num and coprime(num, cop):
            return cop


def extended_gcd(a: int, b: int) -> typing.Tuple[int, int, int]:
    """Function which returns a tuple (r, i, j) such that r = gcd(a, b) = ia + jb

    :param a: int
    :param b: int
    :return: tuple(int, int, int), a, i, j
    """
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a
    ob = b
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob
    if ly < 0:
        ly += oa

    return a, lx, ly


def inverse(e: int, phi: int) -> int:
    """Function which returns the inverse of x % n under multiplication, a.k.a x^-1 (mod n)

    :param e: int, open exponent
    :param phi: int, Eilor's number
    :return: int, d inversed to e
    """

    (divider, inv, _) = extended_gcd(e, phi)

    return inv


def to_bytes(s: str) -> bytes:
    """Function which transform string to bytes

    :param s: str, string which needed to transform
    :return: bytes, string converted to bytes
    """
    return bytes(s, 'utf-8')


def read_data(filename: str) -> bytes:
    """Function which read data from file, byte format

    :param filename: str, filename
    :return: bytes, data converted to bytes
    """
    with open(filename, 'rb') as file:
        return file.read()


def write_data(filename: str, data: bytes) -> None:
    """Function which write data to file

    :param filename: str, file to which you want write
    :param data: bytes, data to write
    :return: None
    """
    with open(filename, 'wb') as file:
        file.write(data)


class RSA:
    """
    Public key cryptographic algorithm based on the computational complexity of the factorization of large integers.
    """

    def __init__(self, p=None, q=None):
        """Initialization of RAS algorithm, creating p and q, counting phi(n), creating e, counting d
        pair (e, n) -- open key
        pair (d, n) -- secret key

        :param p: int, prime number
        :param q: int, prime number
        """
        if p is None:
            self.__p = getprime(SIZE)
        if q is None:
            self.__q = getprime(SIZE)

        self.__n = self.__p * self.__q
        self.__phi = (self.__p - 1) * (self.__q - 1)
        self.__e = getcoprime(self.__phi, SIZE)
        self.__d = inverse(self.__e, self.__phi)

    def encode(self, message: bytes) -> bytes:
        """Function which encode message

        :param message: bytes, message which needed to encode
        :return: bytes, encoded message
        """
        encoded = int.from_bytes(message, 'big', signed=False)

        encoded = pow(encoded, self.__e, self.__n)

        bytes_required = max(1, math.ceil(encoded.bit_length() / 8))

        encoded = encoded.to_bytes(bytes_required, 'big')

        return encoded

    def decode(self, message: bytes) -> bytes:
        """Function which decode message

        :param message: bytes, message which needed to decode
        :return: bytes, decoded message
        """
        decoded = int.from_bytes(message, 'big', signed=False)

        decoded = pow(decoded, self.__d, self.__n)

        bytes_required = max(1, math.ceil(decoded.bit_length() / 8))

        decoded = decoded.to_bytes(bytes_required, 'big')

        return decoded


def test_primality_function() -> None:
    """Miller–Rabin primality algorithm quality test"""

    print(f"prime(num={400}, k={50}) -> {is_prime(num=400, k=50)}")
    print(f"prime(num={60701}, k={300}) -> {is_prime(num=60701, k=1000)}")  # Pseudoprime 60701 = 101 * 601
    print(f"prime(num={1125899839733759}, k={10000}) -> {is_prime(num=1125899839733759, k=10000)}")


if __name__ == '__main__':
    # test_primality_function()
    # rsa = RSA()
    # mes = read_data("message.txt")
    # c = rsa.encode(mes)
    # write_data("encoded.txt", c)
    # m = rsa.decode(c)
    # write_data("decoded.txt", m)

    print(inverse(922, 60))
