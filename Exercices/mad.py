#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as N


def mad(a, axis=None):
    """
    Compute *Median Absolute Deviation* of an array along given axis.
    """

    # Median along given axis, but *keeping* the reduced axis so that
    # result can still broadcast against a.
    med = N.median(a, axis=axis, keepdims=True) 
    mad = N.median(N.absolute(a - med), axis=axis)  # MAD along given axis

    return mad

if __name__ == '__main__':

    x = N.arange(5 * 7, dtype=float).reshape(5, 7)

    print "x =\n", x
    print "MAD(x, axis=None)   =", mad(x)
    print "MAD(x, axis=0)      =", mad(x, axis=0)
    print "MAD(x, axis=1)      =", mad(x, axis=1)
    print "MAD(x, axis=(0, 1)) =", mad(x, axis=(0, 1))
