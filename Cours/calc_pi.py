#!/usr/bin/env python3
# https://cython.readthedocs.io/en/latest/src/tutorial/profiling_tutorial.html


def recip_square(i):

    return 1. / i ** 2


def approx_pi(n=10000000):

    val = 0.
    for k in range(1, n + 1):
        val += recip_square(k)

    return (6 * val) ** .5


if __name__ == '__main__':

    print(approx_pi())
